import os
import shutil
import zipfile
import json
import logging
from logger_config import main_logger as logger

from datetime import datetime, timedelta
import time

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

def get_missed_tasks(config, executed_tasks_data):
    now = datetime.now()
    missed_task_threshold = config.get("missed_task_threshold", 0)
    missed_tasks = []

    # Sort the executed_tasks list based on the timestamp
    executed_tasks_sorted = sorted(
        executed_tasks_data["executed"], key=lambda x: x["timestamp"], reverse=True
    )

    executed_task_dict = {}
    for executed_task in executed_tasks_sorted:
        task_id = executed_task["task_id"]
        executed_time = datetime.strptime(executed_task["timestamp"], "%Y-%m-%d_%H-%M-%S")
        if task_id not in executed_task_dict:
            executed_task_dict[task_id] = executed_time

    for task in config["tasks"]:
        task_id = task["id"]
        last_executed = executed_task_dict.get(task_id, None)

        if last_executed is None or (now - last_executed).days > missed_task_threshold:
            missed_tasks.append(task)

    return missed_tasks






