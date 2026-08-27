import re, sys
from pathlib import Path

def config_auditor(conf_path_arg):
    conf_path = Path(conf_path_arg)
    listen_port_pattern = re.compile(r"(?P<directive>listen)\s+(?:(?P<ip>[\w\.\:\[\]]+):)?(?P<port>\d+)")
    ip_line_pattern = re.compile(r"^\s*(?P<directive>\S+)\s+.*?(?P<ip>\d{1,3}(?:\.\d{1,3}){3})(?::(?P<port>\d+))?")
    server_name_pattern = re.compile(r"(?P<directive>server_name)\s+(?P<domains>[^;]+);")
    search_pattern = [listen_port_pattern, server_name_pattern, ip_line_pattern]
    
    if conf_path.is_file() and conf_path.suffix == ".conf":
        with open(conf_path) as conf:
            for line_num, line in enumerate(conf, start=1):
                for pattern in search_pattern:
                    if search_through_config(conf_path, line_num, line, pattern):
                        break

    elif conf_path.is_dir():
        for config in Path(conf_path).rglob("*.conf"):
            with open(config) as conf:
                for line_num, line in enumerate(conf, start=1):
                    for pattern in search_pattern:
                        if search_through_config(config, line_num, line, pattern):
                            break

def search_through_config(conf, line_num, config_line, pattern):
    match = re.search(pattern, config_line)
    if not match:
        return
    groups = match.groupdict()
    directive = groups.get("directive")
    if directive == "listen":
        ip = groups.get("ip")
        port = groups.get("port")
        ip_str = f"{ip}:" if ip else ""
        combined = f"{conf} {line_num} {directive} {ip_str}{port}"
        print(combined)
        return True

    elif directive == "server_name":
        domains = groups.get("domains", "").strip()
        combined = f"{conf} {line_num} {directive} {domains}"
        print(combined)
        return True

    else:
        ip = groups.get("ip")
        port = groups.get("port")
        ip_str = f"{ip}:{port}" if ip and port else (f"{ip}" if ip else "")
        combined = f"{conf} {line_num} {directive} {ip_str}"
        print(combined)
        return True

if __name__=="__main__":
    config_file=sys.argv[1]
    config_auditor(config_file)
