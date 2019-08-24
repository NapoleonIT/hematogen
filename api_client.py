import asyncio
import aiohttp
from aiohttp import ClientTimeout

from config import ApiConfig


class ApiClient(object):
    def __init__(self, config: ApiConfig, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        self.config = config

    async def call_api(self, resource_path, method, path_params=None, query_params=None, post_params=None, files=None, timeout=60):
        resource_path = f'{self.config.host}:{self.config.post}{resource_path}'
        if path_params is not None:
            resource_path = self.__prepare_path_params(resource_path, path_params)

        timeout = ClientTimeout(total=20)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            result = await session.request(method, resource_path, params=query_params)

            if result.status == 200:
                content = await result.text()
                return content

        return await self.__async_call_api(resource_path, method)

    async def __async_call_api(self, resource_path, method):
        return f'{resource_path} {method}'

    @staticmethod
    def __prepare_path_params(resource_path: str, path_params: dict) -> str:
        for k, v in path_params:
            resource_path.replace('{%s}' % k, str(v))
        return resource_path
