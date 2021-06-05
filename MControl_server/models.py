from datetime import datetime
from pony.orm import *
import os

db = Database()


class User(db.Entity):
    id = PrimaryKey(int, size=32, column="id", auto=True, unsigned=True)
    username = Required(str, unique=True)
    password = Required(str, default="ScooptyWhoop")
    role = Optional(str, default="user")
    scripts = Set("Script")


class Script(db.Entity):
    script_id = PrimaryKey(int)
    created_by = Required(User)
    script_name = Required(str, unique=True)
    description = Optional(str)
    content = Optional(Json)
    editor_data = Optional(Json)
    created = Required(datetime)
    updated = Optional(datetime)


if __name__ == "__main__":
    db.bind(
        provider="sqlite",
        filename=os.path.join("data", "database.sqlite"),
        create_db=True,
    )
    db.generate_mapping(create_tables=True)
