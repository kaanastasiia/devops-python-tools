import re, sys
from pathlib import Path

def config_auditor(conf_path_arg):
    conf_path = Path(conf_path_arg)
    if conf_path.is_file() and conf_path.suffix == ".conf":
        with open(conf_path) as conf:
            for line in conf:
                search_through_config(line)

    #elif conf_path.is_dir():
    #    for file in Path(conf_path).rglob("*.conf"):
    #        with open(file) as log:

def search_through_config(config_line):
    search_pattern=r"(?P<directive>listen)\s+(?:[\w\.\:\[\]]+\:)?(?P<port>\d+)"
    match = re.search(search_pattern, config_line)
    if match:
        directive = match.group("directive")
        port = match.group("port")
        combined = f"{directive} {port}"
        print (combined)

if __name__=="__main__":
    config_file=sys.argv[1]
    config_auditor(config_file)

