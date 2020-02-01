from blessings import Terminal


class View:
    """View class to display informations.

    Attributes:
        _term (Terminal): blessings.Terminal object.
        _n_lines (int): Number of line currently displayed.

    """

    def __init__(self):
        """Create terminal object and set nb of line displayed to 0."""
        self._term = Terminal()
        self._n_lines = 0

    def clear(self):
        """Clear the last view output."""
        for i in range(self._n_lines):
            self._term.stream.write(self._term.clear_eol)
            self._term.stream.write(self._term.move_up)
            self._term.stream.write(self._term.clear_eol)

        self._n_lines = 0

    def display(self, sessions: list):
        """Display informations from a list of session object.

        Args:
            sessions (list): The list of session object.

        """
        output = ""

        for sess in sessions:
            sess_str = str(sess).format(t=self._term) + "\n"
            if sess.error:
                sess_str += "\t└── {}\n".format(sess.error)

            for i, gpu in enumerate(sess.gpus):
                is_last_gpu = i == len(sess.gpus) - 1
                gpu_prefix = "└── " if is_last_gpu else "├── "
                sess_str += (
                    "\t"
                    + self._term.bright_black(gpu_prefix)
                    + str(gpu).format(t=self._term)
                    + "\n"
                )

                for i, process in enumerate(gpu.processes):
                    proc_prefix = "├── " if i < len(gpu.processes) - 1 else "└── "
                    tab_prefix = "\t\t" if is_last_gpu else "\t│\t"

                    sess_str += (
                        self._term.bright_black(tab_prefix + proc_prefix)
                        + str(process).format(t=self._term)
                        + "\n"
                    )

            output += sess_str

        self._term.stream.write(output)
        self._n_lines = output.count("\n")
