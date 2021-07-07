from datetime import datetime

# use orm with DB
from pony import orm
from pony.orm.core import sql_debug

# create db `ponyorm` context
db = orm.Database()


class User(db.Entity):
    id = orm.PrimaryKey(int, column="id", auto=True, unsigned=True)
    username = orm.Required(str, unique=True)
    password = orm.Required(str, default="admin")
    role = orm.Optional(str, default="user")
    scripts = orm.Set("Script")


class Script(db.Entity):
    id = orm.PrimaryKey(int, column="script_id", auto=True)
    created_by = orm.Required(User)
    script_name = orm.Required(str, unique=True)
    description = orm.Optional(str)
    content = orm.Optional(orm.Json)
    editor_data = orm.Optional(orm.Json)
    created = orm.Required(datetime)
    updated = orm.Optional(datetime)


def set_up(full_path, file_creation: bool = False, debug: bool = True):
    # TODO: check path to file
    sql_debug(debug)
    db.bind("sqlite", full_path, create_db=file_creation)
    db.generate_mapping(create_tables=True)
