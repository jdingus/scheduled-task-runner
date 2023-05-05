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

def get_missed_tasks(config):
    executed_tasks = read_executed_tasks()
    now = datetime.now()
    missed_task_threshold = config.get("missed_task_threshold", 0)
    missed_tasks = []

    for task in config["tasks"]:
        task_id = task["id"]
        task_day_of_month = task["day_of_month"]
        task_time = datetime.strptime(task["time"], "%H:%M").time()
        task_datetime = datetime(now.year, now.month, task_day_of_month, task_time.hour, task_time.minute)

        executed_task_dates = [datetime.strptime(task_exec["timestamp"], "%Y-%m-%d_%H-%M-%S") for task_exec in executed_tasks["executed"] if task_exec["task"]["id"] == task_id]

        if not executed_task_dates:
            days_since_task = (now - task_datetime).days
            if days_since_task >= missed_task_threshold:
                missed_tasks.append(task)
        else:
            latest_executed_date = max(executed_task_dates)
            days_since_last_execution = (now - latest_executed_date).days
            if days_since_last_execution >= missed_task_threshold:
                missed_tasks.append(task)

    return missed_tasks


