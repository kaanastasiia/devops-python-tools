import sys, os, time
from pathlib import Path

def log_rotator(dir, days):
    current_time = time.time()
    days_to_unix = int(days) * 24 * 60 * 60
    date_after = current_time - days_to_unix
    for file in os.listdir(dir):
        file_path =  os.path.join(dir, file) 
        if os.path.isfile(file_path):
            file_stat = os.stat(file_path)
            mofidication_time = file_stat.st_mtime
            if mofidication_time < date_after:
                print(file_path)


if __name__=="__main__":
    directory = sys.argv[1]
    days_old = sys.argv[2]
    log_rotator(directory, days_old)