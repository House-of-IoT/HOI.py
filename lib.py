import websockets
import asyncio
import json
from console_logger import ConsoleLogger
import os

class Client:
    def __init__(self):
        self.port = None
        self.host = None
        self.password = None
        self.tasks = None
        self.name = None
        self.type = None

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
    def define_tasks(self,tasks):
        self.tasks = tasks
    
    """
    main execution 
    """
    async def main(self ,restart = False):
        self.prerequisite_check()
        if restart != True:
            self.password = os.environ.get("rpw_hoi_gs")

        websocket = await self.establish_connection()
        connection_response = await self.send_connection_credentials(websocket)

        if connection_response != "success":
            self.logger.log_failed_auth()
        else:
            self.logger.log_passed_auth()
            t1 = loop.create_task(self.test_send_periodic_data_and_listen(websocket))
            t2 = loop.create_task(self.monitor_door(self.config.door_check_interval))
            await asyncio.wait([t1,t2])

    async def establish_connection(self):
        times_attempted = 1
        while True:
            try:
                return await websockets.connect(f'ws://{self.config.host}:{self.config.port}', ping_interval= None, max_size = 20000000)
            except:
                ConsoleLogger.log_issue_establishing_connection(times_attempted)
                times_attempted += 1
                await asyncio.sleep(6)

    def prerequisite_check(self):
        if(self.port == None):
            ConsoleLogger.log_before_quitting('No port was set for the client!')
        if(self.host == None):
            ConsoleLogger.log_before_quitting("No host was set for the client!")
        if(self.tasks == None):
            ConsoleLogger.log_before_quitting("No tasks were defined for the client!")
        if(self.name == None):
            ConsoleLogger.log_before_quitting("No name was defined for the client!")
        if(self.type == None):
            ConsoleLogger.log_before_quitting("No type was defined for the client!")
