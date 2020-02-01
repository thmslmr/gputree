from blessings import Terminal


class View:
    def __init__(self):
        self._term = Terminal()
        self._n_lines = 0

    def clear(self):
        for i in range(self._n_lines):
            self._term.stream.write(self._term.clear_eol)
            self._term.stream.write(self._term.move_up)
            self._term.stream.write(self._term.clear_eol)

    def display(self, sessions):
        output = ""

        for sess in sessions:
            sess_str = str(sess).format(t=self._term)

            for i, gpu in enumerate(sess.gpus):
                is_last_gpu = i == len(sess.gpus) - 1
                gpu_prefix = "└── " if is_last_gpu else "├── "
                sess_str += (
                    "\t"
                    + self._term.bright_black(gpu_prefix)
                    + str(gpu).format(t=self._term)
                )

                for i, process in enumerate(gpu.processes):
                    proc_prefix = "├── " if i < len(gpu.processes) - 1 else "└── "
                    tab_prefix = "\t\t" if is_last_gpu else "\t│\t"

                    sess_str += self._term.bright_black(tab_prefix + proc_prefix) + str(
                        process
                    ).format(t=self._term)

            output += sess_str

        self._term.stream.write(output)
        self._n_lines = output.count("\n")
