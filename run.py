# monthly_task_scheduler.py

import os
import sys
import json
import shutil
import zipfile
from datetime import datetime
import time
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("scheduled_task_runner.log", maxBytes=10*1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def copy_directory(src, dest):
    try:
        shutil.copytree(src, dest)
        logger.info(f"Successfully copied directory from {src} to {dest}")
    except shutil.Error as e:
        logger.error(f"Error copying directory from {src} to {dest}: {e}")
    except OSError as e:
        logger.error(f"Error copying directory from {src} to {dest}: {e}")

def zip_directory(src, dest):
    try:
        with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(src):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), src))
        logger.info(f"Successfully zipped directory {src} to {dest}")
    except Exception as e:
        logger.error(f"Error zipping directory {src} to {dest}: {e}")

def main():
    while True:
        now = datetime.now()
        current_time_str = now.strftime("%Y-%m-%d_%H-%M-%S")

        config = load_config()

        for task in config["tasks"]:
            src = task["src"]
            dest = task["dest"]
            timestamp = task["timestamp"]

            if current_time_str == timestamp:
                temp_dir = os.path.join(dest, f"{current_time_str}_temp")
                copy_directory(src, temp_dir)
                zip_directory(temp_dir, os.path.join(dest, f"{current_time_str}.zip"))
                shutil.rmtree(temp_dir)
        
        time.sleep(60)

if __name__ == "__main__":
    main()
