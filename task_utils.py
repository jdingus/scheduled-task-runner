import os
import shutil
import zipfile
import json
import logging
from datetime import datetime, timedelta
import time

logger = logging.getLogger(__name__)

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
    with open('executed_tasks.json', 'r') as f:
        return json.load(f)

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

def check_missed_tasks(config):
    executed_tasks = read_executed_tasks()
    executed_task_ids = [task["id"] for task in executed_tasks]

    for task in config["tasks"]:
        task_id = task["id"]

        if task_id not in executed_task_ids:
            task_time = datetime.strptime(task["timestamp"], "%Y-%m-%d_%H-%M-%S")
            now = datetime.now()

            if (now - task_time).days <= config["missed_task_threshold"]:
                logger.warning(f"Missed task '{task.get('name', '')}', executing now")

                src = task["src"]
                dest = task["dest"]
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                temp_dir = os.path.join(dest, f"{timestamp}_temp")
                copy_directory(src, temp_dir)
                zip_directory(temp_dir, os.path.join(dest, f"{timestamp} {task.get('name', '')}.zip"))
                shutil.rmtree(temp_dir)

                executed_tasks.append({"task": task, "timestamp": timestamp})
                save_executed_tasks(executed_tasks)
