from os import listdir, remove
from datetime import datetime, timedelta


def log_to_file(log_message, log_location):
    with open(f"{log_location}{datetime.now().date()}.txt", "a+") as f:
        print(f"{datetime.now().isoformat(sep=' ', timespec='milliseconds')} | " +
              log_message, file=f)


def remove_old_logs(last_days_logging, logs_directory):
    list_of_days = [(datetime.now().date() - timedelta(days=day)).strftime('%Y-%m-%d')
                    for day in range(last_days_logging)]

    directory_files = listdir(logs_directory)
    directory_files = [file[:-4] for file in directory_files]

    files_to_delete = list(set(directory_files) - set(list_of_days))

    for file in files_to_delete:
        remove(f"{logs_directory}{file}.txt")


def get_logs_directory():
    log_dir = "logs/"
    return log_dir
