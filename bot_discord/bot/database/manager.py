import json
from typing import Any, List, Dict, Optional, Union

import aiofiles

from bot.constants import DEFAULT_LANG

users_type = List[Dict[str, str]]
user_type = Dict[str, str]
servers_type = List[Dict[str, Union[int, str]]]
server_type = Dict[str, Union[int, str]]
response_content_type = Optional[Dict[str, Any]]


class DatabaseManager:

    def __init__(self, filename: str, rootme_challenges: Dict[str, response_content_type]):
        self.filename = filename
        self.rootme_challenges = rootme_challenges

    async def read_data(self):
        async with aiofiles.open(self.filename, mode='r') as f:
            content = await f.read()
        return json.loads(content)

    async def write_data(self, content):
        content = json.dumps(content)
        async with aiofiles.open(self.filename, mode='w') as f:
            await f.write(content)

    async def is_server_registered(self, id_discord_server: int):
        data = await self.read_data()
        discord_servers = data['discord_servers']
        discord_servers_id = [server['id'] for server in discord_servers]
        return id_discord_server in discord_servers_id

    async def register_server(self, id_discord_server: int):
        data = await self.read_data()
        data['discord_servers'].append({'id': id_discord_server, 'lang': DEFAULT_LANG})
        await self.write_data(data)

    @staticmethod
    def find_server(servers: servers_type, id_discord_server: int) -> Optional[server_type]:
        for server in servers:
            if server['id'] == id_discord_server:
                return server

    async def get_server_language(self, id_discord_server: int):
        data = await self.read_data()
        servers = data['discord_servers']
        server = self.find_server(servers, id_discord_server)
        return server['lang']

    async def update_server_language(self, id_discord_server: int, lang: str):
        data = await self.read_data()
        servers = data['discord_servers']
        server = self.find_server(servers, id_discord_server)
        server['lang'] = lang
        await self.write_data(data)

    @staticmethod
    def find_user(users: users_type, id_discord_server: int, username: str) -> Optional[user_type]:
        for user in users:
            if user['id_discord_server'] == id_discord_server and user['rootme_username'] == username:
                return user

    async def user_exists(self, id_discord_server: int, username: str) -> bool:
        data = await self.read_data()
        users = data['users']
        return self.find_user(users, id_discord_server, username) is not None

    async def create_user(self, id_discord_server: int, username: str, last_challenge_solved: Optional[str] = None):
        new_user = dict(id_discord_server=id_discord_server, rootme_username=username,
                        last_challenge_solve=last_challenge_solved)
        data = await self.read_data()
        data['users'].append(new_user)
        await self.write_data(data)

    async def delete_user(self, id_discord_server, username: str):
        data = await self.read_data()
        users = data['users']
        user = self.find_user(users, id_discord_server, username)
        users.remove(user)
        await self.write_data(data)

    async def update_user_last_challenge(self, id_discord_server: int, username: str, challenge_name: str):
        data = await self.read_data()
        users = data['users']
        user = self.find_user(users, id_discord_server, username)
        user['last_challenge_solve'] = challenge_name
        await self.write_data(data)

    async def select_users(self, id_discord_server: int):
        data = await self.read_data()
        return [user for user in data['users'] if user['id_discord_server'] == id_discord_server]

    async def get_last_challenge_solved(self, id_discord_server: int, username: str) -> str:
        data = await self.read_data()
        users = data['users']
        user = self.find_user(users, id_discord_server, username)
        return user['last_challenge_solve']
