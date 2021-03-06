import os
import yaml
import shlex
import re


def get_gputree_config():
    """Fetch host config from gputree configuration file if found.

    Returns:
        dict: The configuration dictionnary.

    """
    if os.environ.get("GPUTREE_CONFIG_FILE"):
        config_path = os.environ["GPUTREE_CONFIG_FILE"]
    elif os.environ.get("XDG_CONFIG_HOME"):
        config_path = os.path.joint(os.environ["XDG_CONFIG_HOME"], "gputree/config.yml")
    else:
        config_path = "~/.config/gputree/config.yml"

    config_path = os.path.expanduser(config_path)

    if not os.path.isfile(config_path):
        return

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return config


def get_ssh_config():
    """Get configuration from SSH config file.

    Returns:
        dict: Hosts informations from ssh config file.

    Raises:
        ValueError: If a line or host name in unparsable.

    """
    PATH = "~/.ssh/config"
    ssh_config_path = os.path.expanduser(PATH)

    with open(ssh_config_path) as f:
        ssh_config = {}
        last_host = ""

        for line in f:

            line = line.strip()
            if not line or line.startswith("#"):
                continue

            match = re.match(re.compile(r"(\w+)(?:\s*=\s*|\s+)(.+)"), line)
            if not match:
                raise ValueError("Unparsable line {}".format(line))

            key = match.group(1).lower()
            value = match.group(2)

            if key == "host":
                try:
                    current_host = shlex.split(value)[0]
                except ValueError:
                    raise ValueError("Unparsable host {}".format(value))

                ssh_config[current_host] = {}
                last_host = current_host

            else:
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]

                ssh_config[last_host][key] = value

    return ssh_config


def get_hosts_infos(hosts: list):
    """Fetch hosts informations.

    If no host is provided, look at configuration file. The configuration file
    can refer to host defined in the ssh config file.

    Args:
        hosts (list): List of host with format "username@hostname".

    Returns:
        list[dict]: List of host informations.

    Raises:
        ValueError: If no host is found or host pass thru cli does not match format.

    """
    output = []

    if not hosts:
        config_hosts = get_gputree_config()

        if not config_hosts:
            raise ValueError("Unable to find hosts.")

        hosts = config_hosts["hosts"].get("from-ssh-config", [])
        output = [
            {**v, "name": k}
            for k, v in config_hosts["hosts"].items()
            if k != "from-ssh-config"
        ]

    ssh_config = get_ssh_config()
    for host in hosts:

        if host in ssh_config:
            host_infos = ssh_config[host]
            output.append(
                {
                    "name": host,
                    "user": host_infos["user"],
                    "hostname": host_infos["hostname"],
                }
            )
            continue

        match = re.match(r"^([\w|\.]+)\@([\w|\.|\-]+)$", host)
        if not match:
            raise ValueError(
                "Invalid host '{}', does not match pattern username@hostname.".format(
                    host
                )
            )

        user, hostname = match.groups()
        output.append({"name": hostname, "user": user, "hostname": hostname})

    return output
