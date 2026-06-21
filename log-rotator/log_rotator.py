import sys, os, time, shutil, random
from datetime import datetime

def log_rotator(dir, days, move_to):
    current_time = time.time()
    days_to_unix = int(days) * 24 * 60 * 60
    date_after = current_time - days_to_unix
    for parent_dirs, subdirs, files in os.walk(dir):
        subdirs[:] = [d for d in subdirs if d != "archive"]
        for file in files:
            file_path =  os.path.join(parent_dirs, file)
            if os.path.isfile(file_path) and file.lower().endswith(".log"):
                file_stat = os.stat(file_path)
                mofidication_time = file_stat.st_mtime
                if mofidication_time < date_after:
                    log_archivator(file, file_path, move_to)

def log_archivator(file, file_path, move_to_dir):
    now = datetime.now()
    year_month = now.strftime("%Y-%m")
    archive_path = os.path.join(move_to_dir, "archive", year_month)
    os.makedirs(archive_path, exist_ok=True)
    file_in_archive_path = os.path.join(archive_path, file)
    while os.path.isfile(file_in_archive_path):
        random_num = random.randint(1000, 9999)
        #rename the file to keep it
        os.rename(file_in_archive_path, file_in_archive_path + "_"+ str(random_num))
    shutil.move(file_path, file_in_archive_path)
        

if __name__=="__main__":
    directory = sys.argv[1]
    days_old = sys.argv[2]
    move_to = sys.argv[3]
    log_rotator(directory, days_old, move_to)