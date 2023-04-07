import os
import sys
from datetime import datetime
import time
import logging
from logging.handlers import RotatingFileHandler
from task_utils import copy_directory, zip_directory, load_config
import json

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
    config = load_config()

    while True:
        current_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        for task_id, task in enumerate(config["tasks"]):
            task_timestamp = f'{task["day_of_month"]} {task["time"]}'
            if task_timestamp == current_timestamp:
                src = task["src"]
                dest = task["dest"]
                temp_dir = os.path.join(dest, f"{current_timestamp}_temp")
                copy_directory(src, temp_dir)
                zip_directory(temp_dir, os.path.join(dest, f"{current_timestamp}.zip"))
                shutil.rmtree(temp_dir)
                log_execution(task_id, current_timestamp)

        time.sleep(30)

if __name__ == "__main__":
    main()
