import sys,os, math

def report_disk_usage(dir_name):
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    for parent_dirs, subdirs, files in os.walk(dir_name):
        for file in files:
            file_path = os.path.join(parent_dirs, file)
            if os.path.islink(file_path):
                print("Skipping the symlink...")
            else: 
                size = os.path.getsize(file_path)
                if size >= 1024:
                    i = math.floor(math.log(size, 1024))
                    p = math.pow(1024, i)
                    human_readable_size = size / p
                    print(f"{file_path} {human_readable_size:.2f} {units[i]}")
                else:
                    print(f"{file_path} {size} Bytes")

if __name__=="__main__":
    dir=sys.argv[1]
    report_disk_usage(dir)