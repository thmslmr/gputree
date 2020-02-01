import os
import yaml
import sys
import re

import paramiko


def get_config():
    if os.environ.get('GPUTREE_CONFIG_FILE'):
        config_path = os.environ['GPUTREE_CONFIG_FILE']
    elif os.environ.get('XDG_CONFIG_HOME'):
        config_path = os.path.joint(os.environ["XDG_CONFIG_HOME"], "gputree/config.yml")
    else:
        config_path = "~/.config/gputree/config.yml"

    config_path = os.path.expanduser(config_path)

    if not os.path.isfile(config_path):
        return

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    return config


def get_ssh_config(file_path="~/.ssh/config"):
    ssh_config_path = os.path.expanduser(file_path)
    ssh_config = paramiko.SSHConfig()

    with open(ssh_config_path) as f:
        ssh_config.parse(f)

    hostnames = ssh_config.get_hostnames()
    hostnames.discard("*")

    return {host: ssh_config.lookup(host)
            for host in hostnames}


def parse_hosts_option(hosts):
    output = []

    if not hosts:
        config_hosts = get_config()

        if not config_hosts:
            print("ERROR - Unable to find hosts.")
            sys.exit(1)

        hosts = config_hosts["hosts"].get("from-ssh-config", [])
        output = [{**v, "name": k} for k, v in config_hosts["hosts"].items()
                  if k != 'from-ssh-config']

    ssh_config = get_ssh_config()
    for host in hosts:

        if host in ssh_config:
            host_infos = ssh_config[host]
            output.append({"name": host,
                           "user": host_infos["user"],
                           "hostname": host_infos["hostname"]})
            continue

        match = re.match(r"^([\w|\.]+)\@([\w|\.|\-]+)$", host)
        if not match:
            print("ERROR - Invalid host '{}', does not match pattern username@hostname.".format(host))
            sys.exit(1)

        user, hostname = match.groups()
        output.append({"name": hostname, "user": user, "hostname": hostname})

    return output
