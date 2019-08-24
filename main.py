import asyncio

from openapi_spec_validator import validate_v3_spec
import yaml
from openapi_core import create_spec

from config import ApiConfig
from spec import SpecConstructor

from jinja2 import Template, FileSystemLoader, Environment

from users_api import UsersApi


api = UsersApi(config=ApiConfig())
loop = asyncio.get_event_loop()
loop.run_until_complete(api.get_google())

file_loader = FileSystemLoader('python/templates/')
env = Environment(loader=file_loader)
env.trim_blocks = True
env.lstrip_blocks = True
env.rstrip_blocks = True

attrs = [
    {'name': 'id', 'type': 'int'},
    {'name': 'first_name', 'type': 'str', 'required': True},
    {'name': 'second_name', 'type': 'str', 'required': True}
]
api = {'name': 'UsersApi'}

funcs = [
    {'name': 'get_kanzburo', 'path': '/', 'method': 'GET'},
    {'name': 'get_google', 'path': '/', 'method': 'GET'}
]
tm = env.get_template('model.html')
msg = tm.render(model_name='BaseUser', attrs=attrs, funcs=funcs)
print(msg)


api_tm = env.get_template('api.html')
msg = api_tm.render(api=api, funcs=funcs)
print(msg)

wrt = open('python/client/text.py', 'w')
wrt.write(msg)
wrt.close()

# f = open('api.yaml', 'r')
# swagger_yaml = f.read()
# json_ = yaml.safe_load(swagger_yaml)
# spec = create_spec(json_)
#
# result = validate_v3_spec(json_)

spec_constructor = SpecConstructor('api.yaml')

pass


