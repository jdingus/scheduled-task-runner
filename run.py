# monthly_task_scheduler.py

import os
import sys
import time
import json
import subprocess
from datetime import datetime

CONFIG_FILE = 'config.json'
EXECUTED_TASKS_FILE = 'executed_tasks.json'

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    return config

def save_executed_tasks(executed_tasks):
    with open(EXECUTED_TASKS_FILE, 'w') as f:
        json.dump(executed_tasks, f)

def load_executed_tasks():
    if os.path.exists(EXECUTED_TASKS_FILE):
        with open(EXECUTED_TASKS_FILE, 'r') as f:
            executed_tasks = json.load(f)
    else:
        executed_tasks = []

    return executed_tasks

def execute_file(file_path):
    subprocess.run([sys.executable, file_path])

def main():
    config = load_config()
    executed_tasks = load_executed_tasks()

    for executed_task in executed_tasks:
        if not executed_task.get('rerun', False):
            execute_file(executed_task['file'])
            executed_task['rerun'] = True
            save_executed_tasks(executed_tasks)

    while True:
        current_time = datetime.now()

        for task in config['tasks']:
            target_day, target_time = task['timestamp'].split(' ')
            target_hour, target_minute = target_time.split(':')

            if (current_time.day == int(target_day) and
                current_time.hour == int(target_hour) and
                current_time.minute == int(target_minute) and
                not task.get('executed_today', False)):
                execute_file(task['file'])
                task['executed_today'] = True
                executed_tasks.append(task)
                save_executed_tasks(executed_tasks)
            elif current_time.day != int(target_day):
                task['executed_today'] = False

        time.sleep(60)

if __name__ == '__main__':
    main()
