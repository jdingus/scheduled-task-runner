import os
import sys
from datetime import datetime
import time
import shutil
import json
import logging
from logging.handlers import RotatingFileHandler
from task_utils import copy_directory, zip_directory, load_config

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("scheduled_task_runner.log", maxBytes=10*1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_executed_task(task, timestamp):
    executed_tasks_file = "executed_tasks.json"

    if not os.path.exists(executed_tasks_file):
        with open(executed_tasks_file, "w") as f:
            json.dump([], f)

    with open(executed_tasks_file, "r") as f:
        executed_tasks = json.load(f)

    executed_task_data = {
        "task": task,
        "timestamp": timestamp
    }

    executed_tasks.append(executed_task_data)

    with open(executed_tasks_file, "w") as f:
        json.dump(executed_tasks, f)

def main():
    config = load_config()

    while True:
        current_day_of_month = datetime.now().day
        current_time = datetime.now().strftime("%H:%M")

        for task in config["tasks"]:
            if task["day_of_month"] == current_day_of_month and task["time"] == current_time:
                src = task["target_file"]
                dest = task["destination"]
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                temp_dir = os.path.join(dest, f"{timestamp}_temp")
                copy_directory(src, temp_dir)
                zip_directory(temp_dir, os.path.join(dest, f"{timestamp}.zip"))
                shutil.rmtree(temp_dir)
                log_executed_task(task, timestamp)

        time.sleep(60)

if __name__ == "__main__":
    main()
