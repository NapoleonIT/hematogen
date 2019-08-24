from api_client import ApiClient


class UsersApi:

    def __init__(self, api_client=None, **kwargs):

        if api_client is None:
            api_client = ApiClient(**kwargs)
        self.api_client = api_client

    async def get_google(self):
        print(await self.api_client.call_api('/', 'GET'))
