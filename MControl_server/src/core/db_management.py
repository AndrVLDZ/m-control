# typing
from typing import Callable, Any, Tuple
from datetime import datetime

# use orm with DB
from pony import orm
from pony.converting import str2datetime

# DB models and context
from models import set_up
from models import User, Script

# using 'rich' for beautiful table printing
from rich.table import Table as RichTextTable
from rich.console import Console


@orm.db_session
def populate_with_entities():
    # test users
    vlad = User(username="vlad", password="do you know the way")
    boris = User(username="boris", password="understandable")

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


def init_user_columns():
    t = RichTextTable()
    t.add_column("id", justify="right", style="green")
    t.add_column("username", style="cyan")
    t.add_column("password", style="magenta")
    t.add_column("role", justify="center")
    t.add_column("scripts (count)", style="yellow")
    return t


def all_users_to_table():
    t = init_user_columns()
    with orm.db_session:
        users = orm.select(u for u in User)
        for u in users:
            user_scripts = orm.select(s for s in Script if s.created_by == u)
            t.add_row(
                str(u.id),
                str(u.username),
                str(u.password),
                str(u.role),
                str(orm.count(user_scripts)),
            )
    return t


def users_which(constraint_lambda: Callable[[Any], bool]) -> RichTextTable:
    t = init_user_columns()
    with orm.db_session:
        users = orm.select(u for u in User)
        some_users = users.filter(constraint_lambda)
        for user in some_users:
            t.add_row(
                str(user.id),
                str(user.username),
                str(user.my_password),
                str(user.role),
                str(orm.count(user.scripts)),
            )
    return t


if __name__ == "__main__":
    import os

    def create_db_with_entities_test(db_path: Tuple[str, str]):
        path = os.path.join(*db_path)
        set_up(path, file_creation=True, debug=True)
        populate_with_entities()
        t = all_users_to_table()
        console = Console()
        console.print(t)

    def users_from_existing_db_test(db_path: Tuple[str, str]):
        path = os.path.join(*db_path)
        set_up(path, file_creation=False, debug=True)
        t = all_users_to_table()
        console = Console()
        console.print(t)

    tmp_path = ("tmp_db", "database.sqlite")
    # create_db_with_entities_test(tmp_path)
    users_from_existing_db_test(tmp_path)
