from api_client import ApiClient


class UsersApi:

    def __init__(self, api_client=None, **kwargs):

        if api_client is None:
            api_client = ApiClient(**kwargs)

        self.api_client = api_client

    async def get_kanzburo(self, resource_path, method, path_params=None, query_params=None, post_params=None, files=None, timeout=60):

        return await self.api_client.call_api(resource_path, method, path_params, query_params, post_params, files, timeout)

    async def get_google(self, resource_path, method, path_params=None, query_params=None, post_params=None, files=None, timeout=60):

        return await self.api_client.call_api(resource_path, method, path_params, query_params, post_params, files, timeout)

