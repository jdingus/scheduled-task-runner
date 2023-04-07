import os
import shutil
import zipfile
import json
import logging

logger = logging.getLogger(__name__)

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
