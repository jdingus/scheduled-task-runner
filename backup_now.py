import os
import sys
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from task_utils import copy_directory, zip_directory, load_config, read_executed_tasks, save_executed_tasks, check_missed_tasks

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("scheduled_task_runner.log", maxBytes=10*1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def main():
    logger.info("Backup_now script started")
    config = load_config()

    for task in config["tasks"]:
        if task.get("default"):
            task_name = task.get("name", "")
            logger.info(f"Running default task '{task_name}'")

            src = task["src"]
            dest = task["dest"]
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            temp_dir = os.path.join(dest, f"{timestamp}_temp")
            copy_directory(src, temp_dir)
            zip_directory(temp_dir, os.path.join(dest, f"{timestamp} {task_name}.zip"))
            shutil.rmtree(temp_dir)

            executed_tasks = read_executed_tasks()
            executed_tasks.append({"task": task, "timestamp": timestamp})
            save_executed_tasks(executed_tasks)
            break

if __name__ == "__main__":
    main()
