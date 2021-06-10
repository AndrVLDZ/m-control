from typing import Tuple, Any
# functionality provider ________________________________

# db provider ___________________________________________
from core.models import *
from utils.configs import DBConfig
from core.db_management import populate_with_entities
from core.json_schema import *
from pony import orm
from datetime import datetime


class DBProvider:
    def __init__(self, config: DBConfig):
        self.conf = config
        self.sqlite_file = config.check_db_path()

    def connect_to_db(self, create_new_file: bool = True, debug_info: bool = False):
        set_up(self.sqlite_file, file_creation=create_new_file, debug=debug_info)
        if create_new_file:
            populate_with_entities()

    @orm.db_session
    def load_scripts_to_db(self, username: str, json_dir_validated_full_path: str):
        all_scripts = get_script_files_from_dir(json_dir_validated_full_path)
        print("Total count of JSON files in", dirname, "=", len(all_scripts))
        status, good_scripts = validate_scripts(all_scripts)
        print("All is valid:", status)
        print(f"Found {len(good_scripts)} valid files in ->", json_dir_validated_full_path)
        that_user = User.get(username=username)
        scripts_of_that_user = []

        for json_content in good_scripts:
            scripts_of_that_user.append(Script(
                created_by=that_user,
                script_name=json_content["script_name"],
                created=datetime.now(),
                content=json_content
            ))

        that_user.scripts.scripts = orm.Set(*scripts_of_that_user)
        orm.flush()

    def update_users(self, username: str, password: str, query: str) -> bool:
        raise NotImplemented

    def update_scripts(self, script: str, password: str, query: str) -> bool:
        raise NotImplemented

    def try_get_script(self, username: str, script) -> Tuple[bool, Any]:
        raise NotImplemented

    def try_get_user(self) -> Tuple[bool, Any]:
        raise NotImplemented


# async server _________________________________________
from os.path import realpath, dirname, join as join_path


def prepare_db(path: Tuple[str, str]):
    db_dirname, db_filename = path
    _cwd = join_path(dirname(realpath(__file__)))
    _path_to_dir = join_path(_cwd, db_dirname)

    db_config = DBConfig(db_filename=db_filename, db_folder=_path_to_dir)
    db_provider = DBProvider(db_config)
    return db_provider


# use asyncio to implement multi-client server
import asyncio
from rich.console import Console
from rich.pretty import pprint as rich_pprint


class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info("peername")
        rich_pprint(f"Connection from [red]{peername}[/red]")
        self.transport = transport

    def data_received(self, data, msg_encoding: str = "utf-8"):
        message: str = data.decode(msg_encoding)
        print(f"Data received: {message}")
        # get the provider instances
        provider = prepare_db(("test_data", "db.sqlite"))
        provider.connect_to_db(debug_info=True)
        provider.load_scripts_to_db("default_user", join_path(dirname(realpath(__file__)), "test_data"))
        # populate with scripts from specified <JSON_dir>

        # TODO: actual data processing
        # print(f"Send to client: {message}")
        # self.transport.write(data)


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
