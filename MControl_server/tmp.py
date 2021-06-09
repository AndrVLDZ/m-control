from typing import Tuple, Any

from src.utils.configs import *
from src.core.db_management import populate_with_entities

from src.core.models import set_up
from src.utils.configs import DBConfig

# functionality provider ________________________________

# script validator ______________________________________
import jsonschema

# db provider ___________________________________________
class DBProvider:
    def __init__(self, config: DBConfig):
        self.conf = config
        self.sqlite_file = config.check_db_path()

    def connect_to_db(self, create_new_file: bool = True, debug_info: bool = False):
        set_up(self.sqlite_file, file_creation=create_new_file, debug=debug_info)
        if create_new_file:
            populate_with_entities()

    def update_users(self) -> bool:
        raise NotImplemented

    def update_scripts(self) -> bool:
        raise NotImplemented

    def try_get_script(self) -> Tuple[bool, Any]:
        raise NotImplemented

    def try_get_user(self) -> Tuple[bool, Any]:
        raise NotImplemented


# async server __________________________________________
import asyncio


class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info("peername")
        print(f"Connection from {peername}")
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print("Data received: {!r}".format(message))

        print("Send to client: {!r}".format(message))
        self.transport.write(data)

        if data == "closing":
            print("Close the client socket")
            self.transport.close()


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()
    print("\nStarted server...")

    server = await loop.create_server(lambda: EchoServerProtocol(), "0.0.0.0", 8888)

    async with server:
        await server.serve_forever()


asyncio.run(main())
