from codegen.config.config import BaseConfig
from enum import Enum


class PythonHttpLibrary(Enum):
    requests = 'requests'
    aiohttp = 'aiohttp'

    @property
    def raw(self) -> str:
        return str(self.value)

    @staticmethod
    def description() -> str:
        return 'Library for making request: requests, aiohttp'


class PythonConfig(BaseConfig):

    package_name: str = 'hematogen_client'
    package_version: str = '1.0.0'
    package_description: str = ''
    package_author_email: str = ''
    package_url: str = ''
    package_keywords: list = ['HematoGen']

    library: PythonHttpLibrary = PythonHttpLibrary.requests


@PythonConfig.parser(PythonHttpLibrary)
def parse_library(value: str) -> PythonHttpLibrary:
    return PythonHttpLibrary(value)
