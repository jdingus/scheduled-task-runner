# Scheduled Task Runner

This Python script is designed to run tasks on a list of specified recurring day of the month and time. The task parameters are stored in a human-readable and easily configurable JSON file. Additionally, it records task executions in a JSON file that can be checked for historical records.

## Files in this project

1. scheduled_task_runner.py: The main script that runs tasks based on the config.json file.
2. backup_now.py: A script that can be manually run to execute the default task specified in the config.json file.
3. task_utils.py: A utility module containing functions used by scheduled_task_runner.py and backup_now.py.
4. config.json: The configuration file containing tasks and their parameters.
5. executed_tasks.json: A file storing successful task executions.
6. scheduled_task_runner.log: A log file that records task execution information and errors.
7. scheduled_task_runner.bat: A Windows batch file to run scheduled_task_runner.py.
8. backup_now.bat: A Windows batch file to run backup_now.py.

## How to set up the config.json file

The config.json file contains an array of tasks, where each task is an object with the following properties:

1. "day_of_month": The day of the month on which the task should be executed (1-31).
2. "time": The time of the day when the task should be executed, formatted as "HH:MM".
3. "src": The source directory to be backed up.
4. "dest": The destination directory where the backup will be stored.
5. "default": (Optional) A boolean value indicating if the task is the default task to be executed by backup_now.py.

Example of config.json:

{
  "tasks": [
    {
      "day_of_month": 1,
      "time": "23:56",
      "src": "C:/source_directory_1",
      "dest": "C:/destination_directory_1"
    },
    {
      "day_of_month": 15,
      "time": "12:00",
      "src": "C:/source_directory_2",
      "dest": "C:/destination_directory_2",
      "default": true
    }
  ]
}

## How to run the scripts

1. scheduled_task_runner.py: Double-click the scheduled_task_runner.bat file or run it from the command prompt.
2. backup_now.py: Double-click the backup_now.bat file or run it from the command prompt.
