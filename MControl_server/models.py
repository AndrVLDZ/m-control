from datetime import datetime
from pony.converting import str2datetime
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
    id = PrimaryKey(int, column="script_id", auto=True)
    created_by = Required(User)
    script_name = Required(str, unique=True)
    description = Optional(str)
    content = Optional(Json)
    editor_data = Optional(Json)
    created = Required(datetime)
    updated = Optional(datetime)


@db_session
def papulate_with_test_data():
    # enable degug mode
    sql_debug(True)

    # test users
    vlad = User(username="VladosBandos", password="anime_govno")
    boris = User(username="BariskaPipiska", password="hentai_top")

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
    
    # DO IT!
    commit()


if __name__ == "__main__":
    db.bind(
        provider="sqlite",
        filename=os.path.join("data", "database.sqlite"),
        create_db=True,
    )

    db.generate_mapping(create_tables=True)
    papulate_with_test_data()
