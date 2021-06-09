from typing import Tuple, Optional

# WARNING: encryption works only when empty sqlite database
# created with reserved space at the end of each page.
# more at: https://stackoverflow.com/questions/46452599/

# SQLiteCipher requires `pysqlsimplecipher` from git submodules
# source:
#   https://github.com/bssthu/pysqlsimplecipher
# WARNING: this package uses `pycryptodome` library
# installation:
#   git submodule update --recursive
#   pip install <project_dir>/MControl_server/pysqlsimplecipher/

from pysqlsimplecipher import decryptor, encryptor
from os.path import join as join_path


# Usage: encrypted.db <password> output.db
def decrypt(
    in_path: Tuple[str, str], passwd: str, file_out: str = None, encoding: str = "utf-8"
) -> str:
    directory, file_in = in_path
    save_path = (
        join_path(directory, ("decrypted_" + file_in))
        if file_out is None
        else join_path(directory, file_out)
    )
    decryptor.decrypt_file(
        filename_in=join_path(directory, file_in),
        password=bytearray(passwd, encoding),
        filename_out=save_path,
    )

    return save_path


# Usage: plain.db <password> output.db
def encrypt(
    in_path: Tuple[str, str], passwd: str, file_out: str = None, encoding: str = "utf-8"
) -> str:
    directory, file_in = in_path
    save_path = (
        join_path(directory, ("encrypted_" + file_in))
        if file_out is None
        else join_path(directory, file_out)
    )
    encryptor.encrypt_file(
        filename_in=join_path(directory, file_in),
        password=bytearray(passwd, encoding),
        filename_out=save_path,
    )

    return save_path


# usage example
if __name__ == "__main__":
    my_password = "qwerty12345"
    # "database.sqlite" -- needs to be created with reserved space at the end of each page.
    path = "tmp_db", "database.sqlite"

    print("Trying to encrypt DB at:", join_path(*path))
    encrypted: str = encrypt(path, my_password, "encrypted.sqlite")
    print("Encrypted at:", encrypted)
    print("_" * 10)

    print("Trying to decrypt DB at:", encrypted)
    decrypted: str = decrypt(
        ("tmp_db", "encrypted.sqlite"), my_password, "decrypted.sqlite"
    )
    print("Decrypted at:", decrypted)
    print("_" * 10)
