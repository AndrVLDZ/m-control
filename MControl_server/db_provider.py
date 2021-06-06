import os
from typing import Union
import tinydb
from pony.orm import orm as ponyORM
from pony.orm import db_session

from dataclasses import dataclass

from common import DBConfig, check_dir, check_file, get_project_dir as cwd


from models import *


class MainDBProvider:
    def __init__(self, filename: str, db_path: Union[str, None] = None):
        self._filename = filename
        # the default value is: <project directory>/<default DB folder>/
        self._directory = os.path.join(cwd(), DBConfig.db_folder_name)
        # check directory if specified by user
        if db_path is not None:
            # might raise 'IOError' exception if file do not exists
            self._directory = check_dir(db_path)

        # construct abs path
        self._abs_db_path = check_file(os.path.join(self._directory, filename))
        self.db = Database()

    @db_session
    def try_connect(self) -> bool:
        try:
            self.db.bind(provider="sqlite", filename=self._filename, create_db=False)
            return True
        except Exception as err:

            return False

    def db_has_table(self, name: str):
        raise NotImplemented

    def db_has_field(self, tablename: str, field: str):
        raise NotImplemented

    def get_field_data(self, tablename: str, field: str):
        raise NotImplemented

    def update_field_data(self, tablename: str, field: str):
        raise NotImplemented

    @db_session
    def check_user(self, username: str):
        return User.exists(username=username)
