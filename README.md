# `gputree`

Hosts configuration
---

**PATH**

If no host is provided through the command line interface, `gputree` will look for a configuration file. By default, it looks for `gputree/config.yml` file in `$XDG_CONFIG_HOME` or `~/.config` directory. You can define a custom path to find the gputree configuration file by setting the `$GPUTREE_CONFIG_FILE` environement variable.

```bash
export GPUTREE_CONFIG_FILE=/path/to/gputree/config.yml`
```

**CONTENT**

In the configuration file, list your default hosts to look at under the `hosts` key. You can specify hosts in two ways :

1. Define a host with a unique name as key, and set its address with a user name as follows:
```yml
my-gpu:
    hostname: 0.0.0.0
    user: my.username
```

2. Refer to a host defined in your `~/.ssh/config` file if exists:
```yml
from-ssh-config:
    - gpu-1
    - gpu-2
```

**EXAMPLE**

Full `gputree` configuration file example:

```yml
hosts:
  my-gpu:
    hostname: 0.0.0.0
    user: my.username

  from-ssh-config:
    - gpu-1
    - gpu-2
```
