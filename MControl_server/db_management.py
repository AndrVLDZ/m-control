import os
import sys

# use `pysqlsimplecipher` from git submodules
from pysqlsimplecipher import decryptor, encryptor
from sqlitedict import SqliteDict

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
    
    pwd = os.path.dirname(os.path.realpath(__file__))
    read_only_db = SqliteDict(os.path.join(pwd, database_path), flag='r')

    for key, value in read_only_db.iteritems():
        print(key, value)

    print(len(read_only_db))

if __name__ == "__main__":
    process_db('test_plain.db', is_encrypted=False)