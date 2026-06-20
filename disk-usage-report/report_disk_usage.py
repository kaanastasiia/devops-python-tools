import sys,os, math

def report_disk_usage(dir_name, extension=None):
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    size_list = []
    for parent_dirs, subdirs, files in os.walk(dir_name):
        for file in files:
            file_path = os.path.join(parent_dirs, file)
            if not os.path.islink(file_path):
                if extension is None or file.endswith(extension):
                    size = os.path.getsize(file_path)
                    size_list.append((size, file_path))
    temp_list = sorted(size_list, reverse=True)
    top_list = temp_list[:10]
    for item, path in top_list:
        if item == 0:
            human_readable_size = 0.00
            i = 0
        elif item == 1024:
            human_readable_size = 1.00
            i = 1
        else:
            i = math.floor(math.log(item, 1024))
            p = math.pow(1024, i)
            human_readable_size = item / p
        
        print(f"{path} {human_readable_size:.2f} {units[i]}")

if __name__=="__main__":
    if len(sys.argv) == 2: 
        dir=sys.argv[1]
        report_disk_usage(dir)
    elif len(sys.argv) == 3:
        dir=sys.argv[1]
        ext=sys.argv[2]
        report_disk_usage(dir,ext)
    else:
        print("Invalid number of arguments, the script takes only 1 or 2 arguments")
        sys.exit(1)
