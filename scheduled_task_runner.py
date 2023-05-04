import os
import sys
from datetime import datetime
import time
import logging
from logging.handlers import RotatingFileHandler
import json

from task_utils import copy_directory, zip_directory, load_config, read_executed_tasks, save_executed_tasks, check_missed_tasks


# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("scheduled_task_runner.log", maxBytes=10*1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_execution(task_id, timestamp):
    if not os.path.exists("executed_tasks.json"):
        with open("executed_tasks.json", "w") as f:
            json.dump([], f)

    with open("executed_tasks.json", "r") as f:
        executed_tasks = json.load(f)

    executed_tasks.append({"task_id": task_id, "timestamp": timestamp})

    with open("executed_tasks.json", "w") as f:
        json.dump(executed_tasks, f)

def main():
    logger.info("Program started")
    config = load_config()

    while True:
        now = datetime.now()
        current_day_of_month = now.day
        current_time = now.strftime("%H:%M")

        for task in config["tasks"]:
            task_day_of_month = task["day_of_month"]
            task_time = task["time"]

            if task_day_of_month == current_day_of_month and task_time == current_time:
                task_name = task.get("name", "")
                logger.info(f"Waiting for next task '{task_name}' at {task['time']}")
                
                src = task["src"]
                dest = task["dest"]
                task_name = task.get("name", "")
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"{timestamp} {task_name}.zip
