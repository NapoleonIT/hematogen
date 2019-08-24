from typing import Tuple, Set

import yaml
from openapi_core import create_spec
from openapi_core.schema.schemas.models import Schema
from openapi_spec_validator import validate_v3_spec


class SpecConstructor(object):

    def __init__(self, spec_yaml):
        self.spec = self.__validate_spec(spec_yaml)
        self.components = self.__construct(self.spec)
        super().__init__()

    def get_schema_properties(self, schema: Schema) -> Tuple[dict, Set]:
        properties = schema.properties
        required = set(schema.required)
        if schema.all_of:
            for all_of_schema in schema.all_of:
                props, inline_required = self.get_schema_properties(all_of_schema)
                required = required.union(inline_required)

                for name, prop in props.items():
                    exist_key = properties.get(name, None)
                    if not exist_key:
                        properties[name] = prop
                    else:
                        continue
        return properties, required

    def __construct(self, spec):

        components = spec.components.schemas

        for name, component in components.items():
            component_properties, required = self.get_schema_properties(component)
            setattr(component, 'gathered_props', component_properties)
            setattr(component, 'gathered_required', required)

        return components

    def __validate_spec(self, spec_yaml):
        f = open(spec_yaml, 'r')
        swagger_yaml = f.read()
        json_ = yaml.safe_load(swagger_yaml)
        spec = create_spec(json_)

        validate_v3_spec(json_)
        return spec



