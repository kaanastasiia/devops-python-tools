import sys
from pathlib import Path

def parse_logs(keyword, log_arg):
    logfile = Path(log_arg)
    if logfile.is_file() and logfile.suffix == ".log":
        with open(logfile, 'r') as log:
            for line_num, line in enumerate(log, start=1):
                numbred_line = f"{logfile}: line {line_num}: {line}"
                if keyword.lower() in line.lower():
                    print(numbred_line)
    elif logfile.is_dir():
        for file in Path(logfile).rglob("*.log"):
            with open(file) as log:
                for line_num, line in enumerate(log, start=1):
                    numbred_line = f"{file}: line {line_num}: {line}"
                    if keyword.lower() in line.lower():
                        print(numbred_line)            

if __name__=="__main__":
    keyword=sys.argv[1]
    logfile=sys.argv[2]
    parse_logs(keyword, logfile)