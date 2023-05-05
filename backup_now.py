import os
import sys
from datetime import datetime
import time
import logging
from logging.handlers import RotatingFileHandler
import json
import shutil

from task_utils import copy_directory, zip_directory, load_config, read_executed_tasks, save_executed_tasks

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("backup_now.log", maxBytes=10*1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def main():
    logger.info("Backup Now started")
    config = load_config()

    # Find the default task
    default_task = None
    for task in config["tasks"]:
        if task.get("default", False):
            default_task = task
            break

    if default_task:
        src = default_task["src"]
        dest = default_task["dest"]
        task_name = default_task.get("name", "")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        temp_dir = os.path.join(dest, f"{timestamp}_temp")
        copy_directory(src, temp_dir)
        zip_directory(temp_dir, os.path.join(dest, f"{timestamp} {task_name}.zip"))
        shutil.rmtree(temp_dir)

        executed_tasks = read_executed_tasks()
        executed_tasks["executed"].append({"task": default_task, "timestamp": timestamp})  # Fix here
        save_executed_tasks(executed_tasks)
    else:
        logger.warning("No default task found")

if __name__ == "__main__":
    main()
