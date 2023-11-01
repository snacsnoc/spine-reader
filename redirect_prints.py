import io
import sys


class RedirectPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._captured_output = io.StringIO()
        sys.stdout = self._captured_output
        return self

    def __exit__(self, *args):
        sys.stdout = self._original_stdout

    def get_output(self):
        return self._captured_output.getvalue()
