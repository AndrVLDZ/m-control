from datetime import datetime
from typing import Any, AnyStr, Union, Tuple, Callable
from pony.converting import str2datetime
from pony.orm import *
from rich.table import Table as RichTextTable
import os


# create db `ponyorm` context
db = Database()


class User(db.Entity):
    id = PrimaryKey(int, column="id", auto=True, unsigned=True)
    username = Required(str, unique=True)
    password = Required(str, default="ScooptyWhoop")
    role = Optional(str, default="user")
    scripts = Set("Script")


class Script(db.Entity):
    id = PrimaryKey(int, column="script_id", auto=True)
    created_by = Required(User)
    script_name = Required(str, unique=True)
    description = Optional(str)
    content = Optional(Json)
    editor_data = Optional(Json)
    created = Required(datetime)
    updated = Optional(datetime)


def init_user_columns():
    tb = RichTextTable()
    tb.add_column("id", justify="right", style="green")
    tb.add_column("username", style="cyan")
    tb.add_column("password", style="magenta")
    tb.add_column("role", justify="center")
    tb.add_column("scripts (count)", style="yellow")
    return tb


def get_printable_users():
    tb = init_user_columns()
    with db_session:
        all_users = select(u for u in User)
        for user in all_users:
            tb.add_row(
                str(user.id),
                str(user.username),
                str(user.password),
                str(user.role),
                str(count(user.scripts)),
            )
    return tb


def get_users_which(constraint_lambda: Callable[[Any], bool]) -> RichTextTable:
    tb = init_user_columns()
    with db_session:
        all_users = select(u for u in User)
        users = all_users.filter(constraint_lambda)
        for user in users:
            tb.add_row(
                str(user.id),
                str(user.username),
                str(user.password),
                str(user.role),
                str(count(user.scripts)),
            )
    return tb


@db_session
def populate_with_test_data():
    # test users
    vlad = User(username="VladosBandos", password="anime_govno")
    boris = User(username="BariskaRediska", password="hentai_top")

    # test scripts
    Script(
        created_by=vlad,
        script_name="сгенерить сэмпл",
        created=str2datetime("2020-03-12 09:40:00"),
    )
    Script(
        created_by=vlad,
        script_name="врубить музыку на кухне",
        created=str2datetime("2021-05-29 19:52:37"),
        updated=datetime.now(),
    )
    Script(
        created_by=boris, script_name="Алиса, скачай all hentai", created=datetime.now()
    )

    # commit transactions to SQLite
    commit()


if __name__ == "__main__":
    # enable debug mode
    sql_debug(True)

    db.bind(
        provider="sqlite",
        filename=os.path.join("data", "database.sqlite"),
        create_db=True,
    )

    db.generate_mapping(create_tables=True)
    populate_with_test_data()
