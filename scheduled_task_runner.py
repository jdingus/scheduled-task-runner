import os
from datetime import datetime
import time
import shutil

from task_utils import (
    copy_directory,
    zip_directory,
    load_config,
    read_executed_tasks,
    save_executed_tasks,
    check_missed_tasks,
)

from logger_config import main_logger as logger


def execute_task(task, current_timestamp):
    src = task["src"]
    dest = task["dest"]
    task_name = task.get("name", "")
    filename = (
        f"{current_timestamp} {task_name}.zip"
        if task_name
        else f"{current_timestamp}.zip"
    )
    temp_dir = os.path.join(dest, f"{current_timestamp}_temp")
    copy_directory(src, temp_dir)

    zip_directory(temp_dir, os.path.join(dest, f"{current_timestamp} {task_name}.zip"))
    shutil.rmtree(temp_dir)

    executed_tasks = read_executed_tasks()
    executed_time = current_timestamp.strftime("%Y-%m-%d_%H-%M-%S")
    executed_tasks["executed"].append({"task": task, "executed_time": executed_time})
    save_executed_tasks(executed_tasks)
    logger.info(f"Task '{task_name}' (ID: {task['id']}) executed successfully")


def run_missed_tasks(config, current_timestamp):
    executed_tasks = read_executed_tasks()
    logger.debug(f"executed_tasks : {executed_tasks}")
    missed_tasks = check_missed_tasks(config, executed_tasks)
    logger.debug(f"missed_tasks : {missed_tasks}")

    for task in missed_tasks:
        logger.info(f"Executing missed task '{task['name']}' (ID: {task['id']})")
        execute_task(task, current_timestamp)

        # Update executed_tasks with the executed missed task
        executed_time = current_timestamp.strftime("%Y-%m-%d_%H-%M-%S")
        executed_tasks["executed"].append(
            {"task": task, "executed_time": executed_time}
        )
        save_executed_tasks(executed_tasks)


def main():
    logger.info(f"****Program started****")
    config = load_config()
    logger.info("Check for and run any missed tasks...")
    run_missed_tasks(config, datetime.now())

    while True:
        current_timestamp = datetime.now()
        logger.debug(f"starting next loop: {current_timestamp}")
        current_day = current_timestamp.strftime("%d")
        current_time = current_timestamp.strftime("%H:%M")

        for task in config["tasks"]:
            if not "default" in task:
                logger.debug(
                    f"Evaluating for task time and date match....{current_day} {current_time}"
                )
                if (task["time"] == current_time) and (
                    task["day_of_month"] == int(current_day)
                ):
                    task_name = task.get("name", "")
                    logger.info(
                        f"{task_name} scheduled to run on this day at {task['time']} has been triggered to run..."
                    )
                    execute_task(task, current_timestamp)
                else:
                    logger.debug(f"No match for task : {task}")
        logger.debug("sleeping till next check for task run time check...")
        time.sleep(60)


if __name__ == "__main__":
    main()
