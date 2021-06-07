from typing import Union, Tuple
import os

# import configs and common functions
from src.utils.common import check_dir, check_file, get_project_dir as cwd
from src.utils.configs import DBConfig

# SQLiteCipher requires `pysqlsimplecipher` from git submodules
# source:
#   https://github.com/bssthu/pysqlsimplecipher
# WARNING: this package uses `pycryptodome` library
# installation:
#   git submodule update --recursive
#   pip install <project_dir>/MControl_server/pysqlsimplecipher/

from pysqlsimplecipher import decryptor, encryptor


class SQLiteCipher:
    def __init__(
        self,
        filename: str,
        passwd: str,
        path_to_db_folder: Union[str, None] = None,
    ):
        self.filename = filename
        # the default value is: <project directory>/<default DB folder>/
        self.directory = os.path.join(cwd(), DBConfig.db_folder_name)
        # if directory
        # was passed to constructor by user
        # -> check it first
        if path_to_db_folder is not None:
            # might raise 'IOError' exception if file do not exists
            self.directory = check_dir(path_to_db_folder)

        # construct abs path
        self._abs_path = check_file(os.path.join(self.directory, filename))
        self._password: bytearray = bytearray(passwd.encode(DBConfig.passwd_encoding))

    @property
    def db_path(self) -> Tuple[str, str]:
        return self.directory, self.filename

    @db_path.setter
    def db_path(self, path: Tuple[str, str]):
        dir_path, filename = path
        # might raise 'IOError' exception if file do not exists
        self.directory = check_dir(dir_path)
        # update abs path if file exists
        # might raise 'FileNotFoundError'
        self._abs_path = check_file(os.path.join(dir_path, filename))
        self.filename = filename

    @property
    def password(self) -> str:
        return self._password.decode(encoding=DBConfig.passwd_encoding)

    @password.setter
    def password(self, secret: str):
        self._password = bytearray(secret.encode(encoding=DBConfig.passwd_encoding))

    def decrypt(self, file_out: Union[str, None] = None) -> str:
        # Usage: encrypted.db <password> output.db
        # if `file_out` specified -- rewrite with original filename
        output_filename = file_out if file_out is not None else self.filename
        decryptor.decrypt_file(
            self._abs_path,
            self._password,
            os.path.join(self.directory, output_filename),
        )
        return output_filename

    def encrypt(self, file_out: Union[str, None] = None) -> str:
        # Usage: plain.db <password> output.db
        # if `file_out` specified -- rewrite with original filename
        output_filename = file_out if file_out is not None else self.filename
        encryptor.encrypt_file(
            self._abs_path,
            self._password,
            os.path.join(self.directory, output_filename),
        )
        return output_filename
