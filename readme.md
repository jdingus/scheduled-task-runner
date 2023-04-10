# Scheduled Task Runner

This application is designed to automate the backup of directories by executing tasks according to a predefined schedule, configured in the `config.json` file.

## Dependencies
This script uses Python 3.6 or later, and has no external dependencies.

## Features

- Scheduled directory backup based on defined timestamps
- Reoccurring monthly task execution
- Backup triggered by running a separate script (backup_now.py)
- Missed task execution check on startup with configurable time limit
- JSON configuration file for easy task customization
- Execution history stored in executed_tasks.json
- Comprehensive logging with log rotation
- Remote triggering of default task via an HTTP server
- Windows batch files for easy script execution

## Configuration

The `config.json` file stores the configuration for the scheduled tasks. Each task has the following properties:

- `name`: (optional) A human-readable name for the task
- `src`: The source directory to be backed up
- `dest`: The destination directory for the backup
- `timestamp`: The timestamp for when the task should be executed (e.g., "1 23:56" for the 1st day of each month at 23:56)
- `default`: (optional) Set to `true` for tasks that should be executed when running `backup_now.py`

Example `config.json`:

```json
{
  "tasks": [
    {
      "name": "MD1",
      "src": "C:/source_directory",
      "dest": "C:/backup_directory",
      "timestamp": "1 23:56"
    },
    {
      "name": "MD15",
      "src": "C:/source_directory2",
      "dest": "C:/backup_directory2",
      "timestamp": "15 12:00"
    },
    {
      "name": "Default Task",
      "src": "C:/default_src",
      "dest": "C:/default_dest",
      "default": true
    }
  ],
  "missed_task_days": 5
}

## Usage
1. Update the config.json file with the tasks you want to schedule.
2. Run scheduled_task_runner.bat to start the scheduled task runner.
3. Run backup_now.bat to immediately execute the default task defined in the config.json file.
4. Run http_server.bat to start the HTTP server for remote triggering of the default task.
5. To remotely trigger the default task, use an HTTP client (like curl) to send a POST request to the HTTP server: curl -X POST http://IP_ADDRESS:PORT/trigger

## Logging
The application logs its actions and errors to the scheduled_task_runner.log file, which has log rotation to prevent it from growing too large.