# typing
from typing import Callable, Any, Tuple, Dict
from datetime import datetime

# using orm with DB
from pony import orm
from pony.converting import str2datetime

# DB models and context
from models import set_up
from models import User, Script

# using 'rich' for beautiful table printing
from rich.table import Table as RichTextTable
from fernet_crypt import password_encrypt

# using JSON validation
from json_schema import *

USERS_ENCRYPTION_SECRET = "default_secret"
USER_DEFAULT_NAME = "default_user"


def encrypt_with_secret(
    plain_passwords: Dict[str, Any],
    secret_key: str,
    passwd_encoding: str = "utf-8",
) -> Dict[str, Any]:
    # transform dict of <username>:<plain_passwd> to <username>:<encrypted_passwd>
    encrypted = dict()
    for name, plain in plain_passwords.items():
        plain_bytes = plain.encode(passwd_encoding)
        encrypted[name] = password_encrypt(
            msg=plain_bytes, secret_key=secret_key
        ).decode(passwd_encoding)
    return encrypted


@orm.db_session
def populate_with_entities():
    # TODO: separation of logic
    plain_passwd = {
        "vlad": "do you know the way",
        "boris": "understandable",
        "default_user": "default_password",
    }

    encrypted = encrypt_with_secret(plain_passwd, USERS_ENCRYPTION_SECRET)
    # test users
    vlad = User(
        username="vlad",
        password=encrypted["vlad"],
    )
    boris = User(
        username="boris",
        password=encrypted["boris"],
    )

    default_user = User(
        username=USER_DEFAULT_NAME,
        password=encrypted["default_user"],
    )

    # test scripts
    Script(
        created_by=vlad,
        script_name="script of vlad #1",
        created=str2datetime("2020-03-12 09:40:00"),
    )

    Script(
        created_by=vlad,
        script_name="script of vlad #2",
        created=str2datetime("2021-05-29 19:52:37"),
        updated=datetime.now(),
    )

    Script(created_by=boris, script_name="script of boris #1", created=datetime.now())

    # commit transactions to SQLite
    orm.commit()


@orm.db_session
def load_scripts_to_db(username: str, json_dir_validated_full_path: str):
    _scripts = get_script_files_from_dir(json_dir_validated_full_path)
    print(
        "Total count of JSON files in",
        json_dir_validated_full_path,
        "=",
        len(_scripts),
    )
    status, good_scripts = validate_scripts(_scripts)
    print("All is valid:", status)
    print(f"Found {len(good_scripts)} valid files in ->", json_dir_validated_full_path)
    that_user = User.get(username=username)
    scripts_of_that_user = []

    for json_content in good_scripts:
        scripts_of_that_user.append(
            Script(
                created_by=that_user,
                script_name=json_content["script_name"],
                created=datetime.now(),
                content=json_content,
            )
        )

    orm.flush()


@orm.db_session
def try_get_scripts_from_db(username: str = USER_DEFAULT_NAME) -> Tuple[bool, List[Any]]:
    success = True
    json_data = list()
    try:
        u = User.get(username=username)
        user_scripts = orm.select(s for s in Script if s.created_by == u)
        for script in user_scripts:
            json_data.append(script)
    except Exception:
        success = False
    if len(json_data) == 0:
        success = False
    return success, json_data


def init_user_columns():
    _tb = RichTextTable()
    _tb.add_column("id", justify="right", style="green")
    _tb.add_column("username", style="cyan")
    _tb.add_column("password", style="magenta")
    _tb.add_column("role", justify="center")
    _tb.add_column("scripts (count)", style="yellow")
    return _tb


def all_users_to_table():
    _tb = init_user_columns()
    with orm.db_session:
        users = orm.select(u for u in User)
        for u in users:
            user_scripts = orm.select(s for s in Script if s.created_by == u)
            _tb.add_row(
                str(u.id),
                str(u.username),
                str(u.password),
                str(u.role),
                str(orm.count(user_scripts)),
            )
    return _tb


def users_which(constraint_lambda: Callable[[Any], bool]) -> RichTextTable:
    _tb = init_user_columns()
    with orm.db_session:
        users = orm.select(u for u in User)
        some_users = users.filter(constraint_lambda)
        for user in some_users:
            _tb.add_row(
                str(user.id),
                str(user.username),
                str(user.my_password),
                str(user.role),
                str(orm.count(user.scripts)),
            )
    return _tb


# example usage and some tests
if __name__ == "__main__":
    import os

    def create_db_with_entities_test(db_path: Tuple[str, str]):
        path = os.path.join(*db_path)
        set_up(path, file_creation=True, debug=True)
        populate_with_entities()
        tb = all_users_to_table()
        terminal = Console()
        terminal.print(tb)

    def users_from_existing_db_test(db_path: Tuple[str, str]):
        path = os.path.join(*db_path)
        set_up(path, file_creation=False, debug=True)
        tb = all_users_to_table()
        terminal = Console()
        terminal.print(tb)

    tmp_path = ("tmp_db", "database.sqlite")
    create_db_with_entities_test(tmp_path)
    load_scripts_to_db(
        USER_DEFAULT_NAME,
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "tmp_db"),
    )
    t = all_users_to_table()
    console = Console()
    console.print(t)
