from typing import get_type_hints, Type, List
import rapidjson

from codegen import exceptions


class BaseConfig(object):
    _parsers = {}

    def __init__(self, filename: str, *args, **kwargs):
        """
        Create `Config` object with values from file.
        Args:
            filename(str): name of file for load values
            *args:
            **kwargs:
        """
        self._values = {}
        self._values = {property: self.get(property)
                        for property in self.__dir__()
                        if self._should_wrap(property)}
        self._types = {property: get_type_hints(type(self)).get(property) for property, value in self._values.items()}

        try:
            with open(filename, 'r') as file:
                data = rapidjson.load(file)
                self._import(data)
        except rapidjson.JSONDecodeError as e:
            raise exceptions.JSONDecodeException

    def get(self, name: str):
        return self.__getattribute__(name)

    def _should_wrap(self, name: str) -> bool:
        return not name.startswith('_') and not callable(self.get(name))

    def _import(self, json):
        for key, value in json.items():
            if key in self._values:
                self._import_property(key, value)

    def _import_property(self, key: str, value):
        self._values[key] = self.__parse(key, value)

    def __parse(self, key: str, value):
        type_property = self._types.get(key)

        if type_property is None or type_property not in self._parsers:
            return value

        try:
            return self._parsers[type_property](value)
        except:
            raise AttributeError(
                f'Could not parse "{value}" of type {type(value)} as '
                f'{type_property} using parser {self._parsers[type_property]}')

    def __getattribute__(self, name):
        return super(BaseConfig, self).__getattribute__(name)

    def __setattr__(self, key, value):
        if hasattr(self, '_values') and key in self._values.keys():
            self._values[key] = value
        else:
            super(BaseConfig, self).__setattr__(key, value)

    @staticmethod
    def parser(type: Type):
        def decorator(parser):
            BaseConfig._parsers[type] = parser
            return parser

        return decorator


@BaseConfig.parser(bool)
def parse_bool(value: str) -> bool:
    return value.lower() in ('true', 'y', 'yes', '1', 'on')


@BaseConfig.parser(int)
def parse_int(value: str) -> int:
    return int(value)


@BaseConfig.parser(float)
def parse_float(value: str) -> float:
    return float(value)


@BaseConfig.parser(List[str])
def parse_list(value: str) -> List[str]:
    return value.split(',')