from typing import Union
import os
from src.utils.configs import DBConfig
from src.utils.common import check_dir, check_file, get_project_dir as cwd

# use models to generate new DB
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
    def try_connect_to_existing(self) -> bool:
        try:
            self.db.bind(provider="sqlite", filename=self._filename, create_db=False)
            return True
        except Exception as err:
            # TODO: maybe logging ?
            return False

    @db_session
    def generate_db_from_models(self, **kwargs) -> bool:
        raise NotImplemented

    def db_has_table(self, name: str):
        raise NotImplemented

    def db_has_field(self, table_name: str, field: str):
        raise NotImplemented

    def get_field_data(self, table_name: str, field: str):
        raise NotImplemented

    def update_field_data(self, table_name: str, field: str):
        raise NotImplemented

    @db_session
    def check_user(self, username: str):
        return User.exists(username=username)
