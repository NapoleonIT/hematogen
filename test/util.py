import sys
from io import StringIO

from cli import Cli


class Capturing(list):
    """
    usage:
    d = ''
    with Capturing() as output:
        print('asdf')
        d = output
    assert d == 'asdf'
    """

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


def _stub_handler(lang, type_, input_file, output_dir):
    print(lang, type_, input_file, output_dir)


def cli_factory(languages=None, version=None, handler=None) -> Cli:
    if languages is None:
        languages = [
            'python',
            'kotlin',
            'js'
        ]

    if version is None:
        version = '0.1.2'

    if handler is None:
        handler = _stub_handler

    return Cli(languages, version, handler)
