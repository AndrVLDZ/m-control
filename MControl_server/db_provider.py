import os
from typing import Tuple, Union
from pony.orm import orm as ponyORM
import tinydb

get_current_dir = lambda: os.path.dirname(os.path.realpath(__file__))

class MainDBProvider:
    def __init__(self, db_filename, db_full_path: Union[str, None] = None) -> None:
        self.db = ponyORM.Database()
        self.db_filename = db_filename  
        self.full_path = db_full_path
        self.db_std_dir = os.path.join(get_current_dir, "data")  

    def try_open_db_file() -> Tuple[bool, ]:
        raise NotImplemented

    def db_has_table(name: str):
        raise NotImplemented

    def db_has_field(tablename: str, field: str):
        raise NotImplemented

    def db_has_field(tablename: str, field: str):
        raise NotImplemented