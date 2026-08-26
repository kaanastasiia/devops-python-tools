import re, sys
from pathlib import Path

def config_auditor(conf_path_arg):
    conf_path = Path(conf_path_arg)
    listen_port_pattern = re.compile(r"(?P<directive>listen)\s+(?:(?P<ip>[\w\.\:\[\]]+):)?(?P<port>\d+)")
    server_directive_pattern = re.compile(r"^\s*(?P<directive>server)\s+(?P<ip>[\w\.\-\[\]]+)(?::(?P<port>\d+))?")
    server_name_pattern = re.compile(r"(?P<directive>server_name)\s+(?P<domains>[^;]+);")
    search_pattern = [listen_port_pattern, server_name_pattern, server_directive_pattern]
    
    if conf_path.is_file() and conf_path.suffix == ".conf":
        with open(conf_path) as conf:
            for line_num, line in enumerate(conf, start=1):
                for pattern in search_pattern:
                    search_through_config(line_num, line, pattern)

    elif conf_path.is_dir():
        for config in Path(conf_path).rglob("*.conf"):
            with open(config) as conf:
                for line_num, line in enumerate(conf, start=1):
                    for pattern in search_pattern:
                        search_through_config(line_num, line, pattern)

def search_through_config(line_num, config_line, pattern):
    match = re.search(pattern, config_line)
    if not match:
        return
    groups = match.groupdict()
    directive = groups.get("directive")
    if directive == "listen":
        ip = groups.get("ip")
        port = groups.get("port")
        ip_str = f"{ip}:" if ip else ""
        combined = f"{line_num} {directive} {ip_str}{port}"
        print(combined)

    elif directive == "server_name":
        domains = groups.get("domains", "").strip()
        combined = f"{line_num} {directive} {domains}"
        print(combined)

    elif directive == "server":
        ip = groups.get("ip")
        ip_str = f"{ip}:" if ip else ""
        port = groups.get("port")
        combined = f"{line_num} {directive} {ip_str}{port}"
        print(combined)


if __name__=="__main__":
    config_file=sys.argv[1]
    config_auditor(config_file)
