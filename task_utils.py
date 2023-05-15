import json
import os
from datetime import datetime
import zipfile

from logger_config import main_logger as logger
import shutil
def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def copy_directory(src, dest, retries=3, wait_time=60):
    for i in range(retries):
        try:
            shutil.copytree(src, dest)
            logger.info(f"Successfully copied directory from {src} to {dest}")
            return
        except shutil.Error as e:
            logger.warning(f"Error copying directory from {src} to {dest}: {e}")
        except OSError as e:
            logger.warning(f"Error copying directory from {src} to {dest}: {e}")
        
        if i < retries - 1:
            logger.info(f"Retrying copy operation in {wait_time} seconds...")
            time.sleep(wait_time)

    logger.error(f"Failed to copy directory from {src} to {dest} after {retries} attempts")

def read_executed_tasks():
    executed_tasks_file = "executed_tasks.json"

    if not os.path.exists(executed_tasks_file):
        with open(executed_tasks_file, "w") as f:
            json.dump({"executed": []}, f)

    with open(executed_tasks_file, "r") as f:
        executed_tasks = json.load(f)
    return executed_tasks

def save_executed_tasks(executed_tasks):
    with open('executed_tasks.json', 'w') as f:
        json.dump(executed_tasks, f, indent=2)

def zip_directory(src, dest):
    try:
        with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(src):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), src))
        logger.info(f"Successfully zipped directory {src} to {dest}")
    except Exception as e:
        logger.error(f"Error zipping directory {src} to {dest}: {e}")

def check_missed_tasks(config, executed_tasks):
    missed_tasks = []
    current_timestamp = datetime.now()
    logger.debug(f"Current timestamp: {current_timestamp}")

    for task in config["tasks"]:
        logger.debug(f"Checking task with ID {task['id']}")
        if task.get("default"):
            logger.debug(f"Task {task['id']} is a default task, skipping.")
            continue

        day_of_month = int(task["day_of_month"])
        task_time = datetime.strptime(task["time"], "%H:%M").time()
        task_datetime = datetime(current_timestamp.year, current_timestamp.month, day_of_month, task_time.hour, task_time.minute)

        if task_datetime > current_timestamp:
            logger.debug(f"Task {task['id']} is scheduled for the future, skipping.")
            continue

        last_executed_timestamp = None
        for executed_task in executed_tasks["executed"]:
            if executed_task["task"]["id"] == task["id"]:
                executed_time = datetime.strptime(executed_task["executed_time"], "%Y-%m-%d_%H-%M-%S")
                last_executed_timestamp = executed_time
                logger.debug(f"Found last executed timestamp for task {task['id']}: {last_executed_timestamp}")

        time_diff = None
        if last_executed_timestamp:
            time_diff = current_timestamp - last_executed_timestamp
            time_diff_days = time_diff.days

            if time_diff_days >= config["missed_task_threshold"]:
                missed_tasks.append(task)
                logger.info(f"Task {task['id']} is missed, has not be executed for {time_diff_days} days, which is greater than the {config['missed_task_threshold']} day threshold.")
        else:
            missed_tasks.append(task)
            logger.info(f"Task {task['id']} has never been executed, adding to the list.")
    return missed_tasks
