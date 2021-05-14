import os
from urllib.parse import quote_plus # database URL: connection strength
import databases, sqlalchemy

## Postgres Database
##DATABASE_URL = "postgresql://usertest:usertest222@127.0.0.1:5432/dbtest"

###############################################################################
# CONNECTION WITH DATABASE
###############################################################################

# host server
# os.environ.get('An_ENV_VARIABLE', 'DEFAULT_VAL_IF_NOT_FOUND')
host_server = os.environ.get('host_server', 'localhost')
db_server_port = quote_plus(str(os.environ.get('db_server_port', '5432')).replace("%", ""))
database_name = os.environ.get('database_name', 'fastapi')
db_username = quote_plus(str( os.environ.get('db_username', 'postgres') ).replace("%", ""))
db_password = quote_plus(str( os.environ.get('db_password', 'secret') ).replace("%", ""))
ssl_mode = quote_plus(str( os.environ.get('ssl_mode', 'prefer') ).replace("%", "")) # SSL mode is a variable required if your instance of posqres server enforces SSL request
#refromat the database URL
DATABASE_URL = "postgresql://{}:{}@{}:{}/{}?sslmode={}".format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)





metadata = sqlalchemy.MetaData()

usersTableObj = sqlalchemy.Table(
    "py_users",
    metadata,
    sqlalchemy.Column("id"        , sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("username"  , sqlalchemy.String),
    sqlalchemy.Column("password"  , sqlalchemy.String),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name" , sqlalchemy.String),
    sqlalchemy.Column("gender"    , sqlalchemy.CHAR  ),
    sqlalchemy.Column("create_at" , sqlalchemy.String),
    sqlalchemy.Column("status"    , sqlalchemy.CHAR  ),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)


database = databases.Database(DATABASE_URL)
