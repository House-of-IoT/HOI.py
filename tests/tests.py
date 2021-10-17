import unittest
import websockets
from hoi_client.device_config import Config
from hoi_client.client import Client

"""The following tests assume there is a HOI-GeneralServer hosted at the below config location."""

class Tests(unittest.IsolatedAsyncioTestCase):

    async def test(self):
        self.config = Config(50223,"localhost","","test33","non-bot")
        self.websocket = await websockets.connect(f'ws://{self.config.host}:{self.config.port}', ping_interval= None, max_size = 20000000)
        self.client = Client(self.config)
        self.task_one_executed = False
        self.task_two_executed = False

        await self.authentication()
        await self.requirements_check()
        await self.task_execution()
        await self.name_and_type()

    async def successful_authentication(self):
        self.client.password = ""
        response = self.client.send_connection_credentials(self.websocket)
        self.assertEqual(response,"success")
    
    async def task_execution(self):
        await self.client.await_tasks([self.test_task_one(),self.test_task_two()])
        self.assertTrue(self.task_one_executed)
        self.assertTrue(self.task_two_executed)

    async def name_and_type(self):
        name_and_type_data = self.client.name_and_type()
        self.assertEqual(name_and_type_data["name"],self.config.name)
        self.assertEqual(name_and_type_data["type"],self.config.type)

    async def test_task_one(self):
        self.task_one_executed = True

    async def test_task_two(self):
        self.task_two_executed = True


if __name__ == "__main__":
    unittest.main()