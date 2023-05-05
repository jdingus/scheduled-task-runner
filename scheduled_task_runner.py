import os
import sys
from datetime import datetime, timedelta
import shutil
import time
import logging
from logging.handlers import RotatingFileHandler

from task_utils import (
    copy_directory,
    zip_directory,
    load_config,
    read_executed_tasks,
    save_executed_tasks,
    get_missed_tasks,
)

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("scheduled_task_runner.log", maxBytes=10 * 1024 * 1024, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def execute_task(task):
    src = task["src"]
    dest = task["dest"]
    task_name = task.get("name", "")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    temp_dir = os.path.join(dest, f"{timestamp}_temp")
    copy_directory(src, temp_dir)
    zip_directory(temp_dir, os.path.join(dest, f"{timestamp} {task_name}.zip"))
    shutil.rmtree(temp_dir)

    executed_tasks = read_executed_tasks()
    executed_tasks["executed"].append({"task_id": task["id"], "timestamp": timestamp})
    save_executed_tasks(executed_tasks)
    logger.info(f"Task '{task_name}' (ID: {task['id']}) executed successfully")


def main():
    logger.info("Program started")
    config = load_config()

    while True:
        now = datetime.now()
        current_day_of_month = now.day
        current_time = now.strftime("%H:%M")

        executed_tasks = read_executed_tasks()
        missed_tasks = get_missed_tasks(config, executed_tasks)
        

        for task in missed_tasks:
            print(task)
            logger.info(f"Executing missed task '{task['name']}' (ID: {task['id']})")
            execute_task(task)

        for task in config["tasks"]:
            task_day_of_month = task["day_of_month"]
            task_time = task["time"]

            if task_day_of_month == current_day_of_month and task_time == current_time:
                logger.info(f"Executing scheduled task '{task['name']}' (ID: {task['id']}) at {task['time']}")
                execute_task(task)

        time.sleep(60)


if __name__ == "__main__":
    main()
