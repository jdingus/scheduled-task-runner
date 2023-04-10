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
    logger.info("Program started")
    config = load_config()

    while True:
        current_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        for task in config["tasks"]:
            if task["timestamp"] == current_timestamp:
                task_name = task.get("name", "")
                logger.info(f"Waiting for next task '{task_name}' at {task['timestamp']}")
                
                src = task["src"]
                dest = task["dest"]
                temp_dir = os.path.join(dest, f"{current_timestamp}_temp")
                copy_directory(src, temp_dir)
                zip_directory(temp_dir, os.path.join(dest, f"{current_timestamp} {task_name}.zip"))
                shutil.rmtree(temp_dir)

                executed_tasks = read_executed_tasks()
                executed_tasks.append({"task": task, "timestamp": current_timestamp})
                save_executed_tasks(executed_tasks)

        time.sleep(60)

if __name__ == "__main__":
    main()
