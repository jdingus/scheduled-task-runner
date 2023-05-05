import os
import sys
from datetime import datetime
import time
import logging
from logger_config import main_logger as logger
import json
import shutil

from task_utils import copy_directory, zip_directory, load_config, read_executed_tasks, save_executed_tasks, check_missed_tasks



def execute_task(task):
    src = task["src"]
    dest = task["dest"]
    task_name = task.get("name", "")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    temp_dir = os.path.join(dest, f"{timestamp}_temp")
    
    if not os.path.exists(src):
        logger.error(f"Source directory '{src}' does not exist. Skipping task '{task_name}'.")
        return

    try:
        copy_directory(src, temp_dir)
        zip_directory(temp_dir, os.path.join(dest, f"{timestamp} {task_name}.zip"))
        shutil.rmtree(temp_dir)
    except Exception as e:
        logger.error(f"Failed to execute task '{task_name}': {e}")

    executed_tasks = read_executed_tasks()
    executed_tasks["executed"].append({"task": task, "timestamp": timestamp})
    save_executed_tasks(executed_tasks)


def main():
    logger.info("Program started")

    while True:
        config = load_config()  # Reload the config file in each iteration
        now = datetime.now()
        current_day_of_month = now.day
        current_time = now.strftime("%H:%M")

        for task in config["tasks"]:
            task_day_of_month = task["day_of_month"]
            task_time = task["time"]

            if task_day_of_month == current_day_of_month and task_time == current_time:
                task_name = task.get("name", "")
                logger.info(f"Executing task '{task_name}' at {task['time']}")
                execute_task(task)
                logger.info(f"Task '{task_name}' completed successfully")
                time.sleep(60)  # Wait for 1 minute to avoid executing the same task multiple times in the same minute
        time.sleep(10)

if __name__ == "__main__":
    logger.info("Checking for missed tasks")
    config = load_config()
    missed_tasks = get_missed_tasks(config)
    for task in missed_tasks:
        logger.info(f"Executing missed task '{task.get('name', '')}' scheduled for day {task['day_of_month']} at {task['time']}")
        execute_task(task)

    main()

