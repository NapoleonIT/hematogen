import unittest
import os
import os.path

from cli import Cli
from test.util import Capturing, cli_factory     


class CliCase(unittest.TestCase):

    def test_list(self):
        cli: Cli = cli_factory()
        real = ''
        with Capturing() as out:
            try:
                cli.perform(['list'])
            except SystemExit:
                pass
            real = out
        expected = ['python','kotlin','js']
        self.assertEqual(real, expected)

    def test_generate(self):
        control_dict = {
            'lang': None,
            'type': None,
            'input_file': None,
            'output_dir': None
        }
        def _stub_handler(lang_, type__, input_file_, output_dir_):
            control_dict['lang'] = lang_
            control_dict['type'] = type__
            control_dict['input_file'] = input_file_
            control_dict['output_dir'] = output_dir_

        cli = cli_factory(handler = _stub_handler)
        try:
            cli.perform([
                'generate',
                'python',
                'client',
                'api.yaml',
                'output_dir'
                ])
        except SystemExit:
            pass
        self.assertEqual(control_dict['lang'], 'python')
        self.assertEqual(control_dict['type'], 'client')
        self.assertEqual(
            control_dict['input_file'],
            os.path.join(os.getcwd(), 'api.yaml')
            )
        self.assertEqual(
            control_dict['output_dir'],
            os.path.join(os.getcwd(), 'output_dir')
            )
