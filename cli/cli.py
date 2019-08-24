import argparse
import sys
import os
import os.path
from typing import List, Callable, Any


class ArgumentParsingException(Exception):
    pass


class ArgumentParser(argparse.ArgumentParser):

    def error(self, message: str):
        raise ArgumentParsingException(f"{self.prog}: error: {message}")


class Cli(object):
    """
    CLI usage:
        cli generate <language:str> <type:str[server/client]> <input_file:str> <output_dir:str>
        cli list
        cli version
        cli -h

    languages        = List[str]
    version          = str
    generate_handler = function(lang, type, input_file_absolute_path, output_dir_absolute_path)

    !Raises ArgumentParsingException when wrong arguments are given

    example:
    def generator(lang, type_, input_path, output_dir):
        pass
    cli = Cli(['python'], '0.1.2', generator)
    cli.perform()
    """

    def __init__(self, languages: List[str], version: str, generate_handler: Callable[[str, str, str, str], Any]):
        self._languages         = languages
        self._version           = version
        self._generate_handler  = generate_handler

        self._parser = ArgumentParser(
            description='List the content of a folder'
            )

        self._parser.add_argument(
            'action',
            type=str,
            help='list / generate / version'
            )

        self._parser.add_argument(
            'language',
            type=str,
            nargs='?',
            help='one of available languages'
            )

        self._parser.add_argument(
            'type',
            type=str,
            nargs='?',
            help='server / client'
            )

        self._parser.add_argument(
            'input_file',
            type=str,
            nargs='?',
            help='path to openapi specification'
            )

        self._parser.add_argument(
            'output_dir',
            type=str,
            nargs='?',
            help='path to directory for output files'
            )

    def perform(self, argv: List[str] = sys.argv[1:]):
        parsed = self._parser.parse_args(argv)
        if parsed.action == 'list':
            self._write_list()
        elif parsed.action == 'version':
            self._write_version()
        elif parsed.action == 'generate':
            try:
                self._perform_generate(parsed)
            except ArgumentParsingException as e:
                sys.stdout.write(str(e.message) + '\n')
                self._write_help()
        else:
            self._write_help()
    
    def _write_list(self):
        for item in self._languages:
            sys.stdout.write(str(item) + '\n')
        sys.exit(0)

    def _write_version(self):
        sys.stdout.write(str(self._version) + '\n')
        sys.exit(0)

    def _write_help(self):
        self._parser.print_help()
        sys.exit(0)

    def _perform_generate(self, parsed: argparse.Namespace):
        exc_required_field_message = 'the following arguments are required: %s'
        if parsed.language is None:
            error_message = exc_required_field_message % 'language'
            raise ArgumentParsingException(
                f"{self._parser.prog}: error: {error_message}"
                )

        if parsed.language not in self._languages:
            error_message = 'language is not in available languages'
            raise ArgumentParsingException(
                f"{self._parser.prog}: error: {error_message}"
                )

        language = parsed.language

        if parsed.type is None:
            error_message = exc_required_field_message % 'type'
            raise ArgumentParsingException(
                f"{self._parser.prog}: error: {error_message}"
                )

        if parsed.type not in ['client', 'server']:
            error_message = 'type should be either `client` or `server`'
            raise ArgumentParsingException(
                f"{self._parser.prog}: error: {error_message}"
                )
        type_ = parsed.type

        if parsed.input_file is None:
            error_message = exc_required_field_message % 'input_file'
            raise ArgumentParsingException(
                f"{self._parser.prog}: error: {error_message}"
                )

        input_file = os.path.join(
            os.getcwd(),
            parsed.input_file
            )

        if not os.path.isfile(input_file):
            error_message = 'input_file does not exists'
            raise ArgumentParsingException(
                f"{self._parser.prog}: error: {error_message}"
                )

        if parsed.output_dir is None:
            error_message = exc_required_field_message % 'output_dir'
            raise ArgumentParsingException(
                f"{self._parser.prog}: error: {error_message}"
                )

        output_dir = os.path.join(
            os.getcwd(),
            parsed.output_dir
            )

        if os.path.isfile(output_dir):
            error_message = 'output_dir cannot be a file'
            raise ArgumentParsingException(
                f"{self._parser.prog}: error: {error_message}"
                )

        self._generate_handler(language, type_, input_file, output_dir)
