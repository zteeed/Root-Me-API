import aiofiles
import json
from typing import List, Dict, Optional


class DatabaseManager:

    def __init__(self, filename: str):
        self.filename = filename

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
        return id_discord_server in discord_servers

    async def register_server(self, id_discord_server: int):
        data = await self.read_data()
        data['discord_servers'].append(id_discord_server)
        await self.write_data(data)

    @staticmethod
    def find_user(users: List[Dict[str, str]], id_discord_server: int, username: str) -> Optional[Dict[str, str]]:
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
