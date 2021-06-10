from typing import Tuple, Any

# functionality provider ________________________________

# db provider ___________________________________________
from core.models import *
from utils.configs import DBConfig
from core.db_management import (
    populate_with_entities,
    load_scripts_to_db,
    USER_DEFAULT_NAME,
    try_get_scripts_from_db,
)
from core.json_schema import *
from os.path import realpath, dirname, join as join_path
from utils.common import check_dir


class DBProvider:
    def __init__(self, config: DBConfig):
        self.conf = config
        # path validation: might throw an exception
        self.sqlite_file = config.check_db_path()
        # path validation: might throw an exception if directory with specified name not found in path
        _checked = check_dir(
            join_path(dirname(realpath(__file__)), self.conf.db_folder)
        )
        self.JSON_dir_path = _checked

    # loads json scripts from specified directory to SQLite
    def load_user_scripts_to_db(self, username: str = USER_DEFAULT_NAME):
        load_scripts_to_db(
            username=username, json_dir_validated_full_path=self.JSON_dir_path
        )

    # connects to existing database specified in config
    def connect_to_db(self, create_new_file: bool = True, debug_info: bool = False):
        set_up(self.sqlite_file, file_creation=create_new_file, debug=debug_info)
        if create_new_file:
            populate_with_entities()

    @staticmethod
    def get_all_scripts_of_user(username: str = USER_DEFAULT_NAME):
        return try_get_scripts_from_db(username)

    def update_users(self, username: str, password: str, query: str) -> bool:
        raise NotImplemented

    def update_scripts(self, script: str, password: str, query: str) -> bool:
        raise NotImplemented

    def try_get_script(self, username: str, script) -> Tuple[bool, Any]:
        raise NotImplemented

    def try_get_user(self) -> Tuple[bool, Any]:
        raise NotImplemented


# async server _________________________________________
# use asyncio to implement multi-client server
import asyncio
from rich.console import Console
from rich.pretty import pprint as rich_pprint


def get_default_provider(path: Tuple[str, str]):
    db_dirname, db_filename = path
    db_config = DBConfig(db_filename=db_filename, db_folder=db_dirname)
    provider = DBProvider(db_config)
    provider.connect_to_db(debug_info=True)
    provider.load_user_scripts_to_db()
    return provider


class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info("peername")
        rich_pprint(f"Connection from [red]{peername}[/red]")
        self.transport = transport

    def data_received(self, data, msg_encoding: str = "utf-8"):
        message: str = data.decode(msg_encoding)
        print(f"Data received: {message}")
        provider = get_default_provider(
            (join_path("core", "tmp_dir"), "db_for_tests.sqlite")
        )
        status, scripts_data = provider.get_all_scripts_of_user(
            username=USER_DEFAULT_NAME
        )
        if status:
            for s in scripts_data:
                if message in s.keys():
                    print(f"Received: {message} matched")
                    rich_pprint(s)
        else:
            rich_pprint(
                f"[red]Err:[/red] could not match specified username [bold yellow]script_name: {message}[/bold yellow]"
            )


async def server_main(host: str, port: int, out_stream: Console):
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()
    server = await loop.create_server(lambda: EchoServerProtocol(), host, port)

    console = Console() if out_stream is None else out_stream
    console.print("\nStarting server at:", style="yellow")
    console.print(f"\t-> HOST: [bold cyan]{host}[/bold cyan]")
    console.print(f"\t-> [u]PORT[/u]: [bold magenta]{port}[/bold magenta]")

    async with server:
        await server.serve_forever()


def main():
    # TODO:
    # 0) get all cmd args (<passwd>, <path>, <server_mode=(tcp || http)>, <server_host>, <server_port>, ...)
    # 1) get [server_database] from <path>
    #   1.1) check if <path> -> 'is ok'
    #   1.2) decrypt [server_database] with <passwd>
    #   1.2) open server database and check whether it's empty or not
    #       => if it is empty -- try create new db with <std_user> and <std_script> (=std_tables)
    #       => if it is not empty -- print content to [stdout]
    # 2) start
    # 3) start in [interactive mode] (=event_loop) => new Thread for working with user
    #       - prints <messages> from [tcp_server] || [http_server?]
    #       - waits for user [commands] = {
    #               stop_server: {}
    #               restart_server: {}
    #               update_db: { table="", field="", value="" },
    #               add_or_replace_script:  { username="", script_name="", script_content="<JSON>" },
    #               add_script_from_path:   { username="", script_name="", json_file="<path>" },
    #               exit: {}
    #       }
    pass


def start():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    # TODO: cli argument parsing
    raise NotImplemented


if __name__ == "__main__":
    rich_console = Console(width=80)
    asyncio.run(server_main("0.0.0.0", 9999, out_stream=rich_console))
