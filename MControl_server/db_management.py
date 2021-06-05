import os
import sys
from pony import orm as ponyORM

# use `pysqlsimplecipher` from git submodules
from pysqlsimplecipher import decryptor, encryptor


def decrypt(filename_in: str, password: str, filename_out: str):
    """Usage: encrypted.db <password> output.db"""
    passwd = bytearray(password.encode("utf8"))
    decryptor.decrypt_file(filename_in, passwd, filename_out)


def encrypt(filename_in: str, password: str, filename_out: str):
    """Usage: plain.db <password> output.db"""
    passwd = bytearray(password.encode("utf8"))
    encryptor.encrypt_file(filename_in, passwd, filename_out)


DIRNAME = "data"
PASSWORD = "password"


def process_db(filename: str, is_encrypted: bool = False):
    database_path: str = os.path.join(DIRNAME, filename)
    if is_encrypted == True:
        new_name = database_path[:-3] + "_decrypted.db"
        # try to decrypt
        # TODO: handling of possible DB decryption errors
        decrypt(database_path, PASSWORD, new_name)
        database_path = new_name

    cwd = os.path.dirname(os.path.realpath(__file__))
    db = ponyORM.Database()
    db.bind(
        provider="sqlite", filename=os.path.join(cwd, database_path), create_db=False
    )

    # do stuff with DB


if __name__ == "__main__":
    # process_db("test_plain.db", is_encrypted=False)
    process_db(filename="sqlite_pony_plain.db")
