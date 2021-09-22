import websockets
import asyncio
import json
from console_logger import ConsoleLogger

class Client:
    def __init__(self):
        self.port = None
        self.host = None
        self.password = None

    def set_host(self,host):
        self.host = host

    def set_port(self,port):
        self.port = port

    def set_password(self,password):
        self.password = password

    """
    user would pass in a list of coroutines that 
    should be executed during program execution
    """
    def define_tasks():
        pass


    async def establish_connection(self):
        times_attempted = 1
        while True:
            try:
                return await websockets.connect(f'ws://{self.config.host}:{self.config.port}', ping_interval= None, max_size = 20000000)
            except:
                ConsoleLogger.log_issue_establishing_connection(times_attempted)
                times_attempted += 1
                await asyncio.sleep(6)
