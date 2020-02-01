import asyncio
import xml.etree.ElementTree as ET

import asyncssh

COMMAND = "nvidia-smi -x -q"


class Session:
    def __init__(self, hostname: str, user: str, name: str):
        self.hostname = hostname
        self.user = user
        self.name = name

        self.gpus = []
        self.error = ""
        self.status = "WAITING"

    async def fetch(self, timeout):
        try:
            conn = await asyncio.wait_for(
                asyncssh.connect(self.hostname, username=self.user, password=None),
                timeout=timeout,
            )
            return await conn.run(COMMAND)

        except Exception as e:
            return e

    def update(self, output):
        if isinstance(output, Exception):
            self.status = "SSH_ERROR"
            error_message = str(output)
            self.error = (
                "\t"
                + (error_message if error_message else type(output).__name__)
                + "\n"
            )

        elif output.exit_status != 0:
            self.status = "COMMAND_ERROR"
            self.error = output.stderr

        else:
            self.status = "OK"
            stats = ET.fromstring(output.stdout)
            gpus = stats.findall("gpu")
            self.gpus = [GPU(gpu) for gpu in gpus]

    def __str__(self):
        status_color = {
            "WAITING": "{{t.yellow}}",
            "OK": "{{t.green}}",
            "SSH_ERROR": "{{t.red}}",
            "COMMAND_ERROR": "{{t.red}}",
        }.get(self.status, "{{t.normal}}")
        return (
            "[" + status_color + "{self.status}{{t.normal}}] "
            "{{t.bold}}{self.name}{{t.normal}} "
            "{{t.bright_black}}({self.user}@{self.hostname}){{t.normal}}\n"
            "{self.error}"
        ).format(self=self)


class GPU:
    def __init__(self, element):
        self._e = element
        self.processes = [
            Process(process)
            for process in element.find("processes").findall("process_info")
        ]

    @property
    def id(self):
        return self._e.findtext("minor_number")

    @property
    def name(self):
        return self._e.findtext("product_name")

    @property
    def temperature(self):
        return self._e.find("temperature").findtext("gpu_temp")

    @property
    def fan(self):
        return self._e.findtext("fan_speed")

    @property
    def memory_used(self):
        return self._e.find("fb_memory_usage").findtext("used").replace(" MiB", "")

    @property
    def memory_total(self):
        return self._e.find("fb_memory_usage").findtext("total").replace(" MiB", "")

    def __str__(self):
        return (
            "({{t.bold}}{self.id}{{t.normal}}) {self.name} | "
            "{self.memory_used} / {self.memory_total} MiB\n"
        ).format(self=self)


class Process:
    def __init__(self, element):
        self._e = element

    @property
    def pid(self):
        return self._e.findtext("pid")

    @property
    def name(self):
        return self._e.findtext("process_name")

    @property
    def memory(self):
        return self._e.findtext("used_memory")

    def __str__(self):
        return "{self.pid} : {self.name} - {self.memory}\n".format(self=self)
