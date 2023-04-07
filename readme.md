# Scheduled Task Runner

This Python script allows you to run specified tasks on a recurring basis at specific days of the month and times.

## Dependencies

This script uses Python 3.6 or later, and has no external dependencies.

## Configuration

The script reads its configuration from a `config.json` file located in the same directory as the script. This file should be structured as follows:

```json
{
  "tasks": [
    {
      "file": "/path/to/first/script.py",
      "timestamp": "1 23:56"
    },
    {
      "file": "/path/to/second/script.py",
      "timestamp": "15 12:00"
    }
  ]
}

Replace /path/to/first/script.py and /path/to/second/script.py with the paths to the files you want to execute. Set the corresponding day of the month and time for each task, in the format "day hour:minute". For example, "1 23:56" means the task will be executed on the 1st day of every month at 23:56.

Usage
Place the Python script and the config.json file in the same directory.
Configure the config.json file according to your requirements (see the Configuration section above).
Run the script using the command python scheduled_task_runner.py (replace scheduled_task_runner.py with the name of the script file if you've renamed it).
The script will run indefinitely and execute the specified tasks on a recurring basis at the specified days of the month and times. It will also maintain a historical record of executed tasks in a file called executed_tasks.json.

Support
If you have any questions or issues, please contact Josh Dingus : jdingus@hendrickson-intl.com

Script created 4/7/23

