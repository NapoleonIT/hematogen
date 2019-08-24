from jinja2 import FileSystemLoader, Environment
from openapi_core.schema.schemas.enums import SchemaType

from spec import SpecConstructor
from ..base_codegen import BasePythonCodegen


class ClientPythonCodegen(BasePythonCodegen):
    templates_dir = 'codegen/languages/python/templates/'
    model_template = 'model.html'
    models_name_dir = 'models'
    types_map = {
        SchemaType.INTEGER: 'int',
        SchemaType.BOOLEAN: 'bool',
        SchemaType.STRING: 'str',
        SchemaType.ARRAY: 'list',
        SchemaType.NUMBER: 'float'
    }

    def __init__(self, package_name: str, version: str, outdir: str, spec: SpecConstructor):
        self.package_name = package_name
        self.version = version
        self.outdir = outdir
        self.spec = spec

        file_loader = FileSystemLoader(self.templates_dir)
        self.env = Environment(loader=file_loader)
        self.env.trim_blocks = True
        self.env.lstrip_blocks = True
        self.env.rstrip_blocks = True

    def generate(self):
        self.generate_models()
        pass
        # out: models, api, package

    def generate_models(self):
        tm = self.env.get_template(self.model_template)

        for c_name, component in self.spec.components.items():
            imports = []
            attrs = []
            for p_name, prop in component.gathered_props.items():
                attr = {}
                if prop.type == SchemaType.OBJECT:
                    imports.append(p_name)
                    attr['name'] = p_name
                    attr['type'] = prop.name
                else:
                    attr = {'name': p_name, 'type': self.types_map[prop.type]}
                # if prop.required:
                #     attr['required'] =
                attrs.append(attr)

            m = tm.render(model_name=c_name, imports=imports, attrs=attrs)
            pass

