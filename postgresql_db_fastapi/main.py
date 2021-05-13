# reference: https://www.youtube.com/watch?v=YUuuJPokBf4
from urllib.parse import quote_plus # database URL: connection strength
import os
###############################################################################
# CONNECTION WITH DATABASE
###############################################################################

# host server
# os.environ.get('An_ENV_VARIABLE', 'DEFAULT_VAL_IF_NOT_FOUND')
host_server = os.environ.get('host_server', 'localhost')
db_server_port = quote_plus(str(os.environ.get('db_server_port', '5432')).replace("%", ""))
database_name = os.environ.get('database_name', 'fastapi')  # we should already have a databse named "fastapi" in our instance of postgres
db_username = quote_plus(str( os.environ.get('db_username', 'postgres') ).replace("%", ""))
db_password = quote_plus(str( os.environ.get('db_password', 'secret') ).replace("%", ""))
ssl_mode = quote_plus(str( os.environ.get('ssl_mode', 'prefer') ).replace("%", "")) # SSL mode is a variable required if your instance of posqres server enforces SSL request
#refromat the database URL
DATABASE_URL = "postgresql://{}:{}@{}:{}/{}?sslmode={}".format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)

# define a sql_alchemy model
import sqlalchemy

meta_data = sqlalchemy.MetaData()
# creating two entities / 2 properties

notesTableObj = sqlalchemy.Table(
    "notes",
    meta_data,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, pool_size=3,
)

# Actual communication with databse
meta_data.create_all(engine)

###############################################################################
# Pydantic Model
###############################################################################
from pydantic import BaseModel

class NoteIn(BaseModel): # pydantic obj used in request
    text: str
    completed: bool


class Note(BaseModel): # Pydantic obj used in response
    id: int
    text: str
    completed: bool

###############################################################################
# FastApi as the Web API
###############################################################################
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI(title="REST API using FastAPI PostGres Async Endpoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #Now we are allowing all to access my API. other choices ==>  allow_origins=["www.examplpes.com", "example.com", "localhost: 5000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import databases  # enables the async communication with POstgreSQL
database = databases.Database(DATABASE_URL)

# I want to connect to the datase whenever the API (fastAPI) starts
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# an endpoint to add Notes
@app.post("/notes/", response_model=Note)
async def create_node(noteIn: NoteIn):
    query = notesTableObj.insert().values(text=noteIn.text, completed=noteIn.completed)
    last_record_id = await database.execute(query)
    return {**noteIn.dict(), "id":last_record_id}

@app.get("/notes/", response_model=List[Note])
async def read_notes(skip: int=0, take: int=20):
    query = notesTableObj.select().offset(skip).limit(take) # query in a collection of 20 notes
    return await database.fetch_all(query)

@app.get("/notes/{note_id}", response_model=Note)
async def read_note(note_id: int):
    query = notesTableObj.select().where(notesTableObj.c.id == note_id)
    return await database.fetch_one(query)

# an update endpoint ==> response type for "the updated note"
@app.put("/notes/{note_id}", response_model=Note)
async def update_note(note_id: int, payload: NoteIn):  # the updated note is coming as payload
    query = notesTableObj.update().where( notesTableObj.c.id == note_id).values(text = payload.text, completed=payload.completed)
    await database.execute(query)
    return {**payload.dict(), "id": note_id}

@app.delete("/notes/{note_id}")
async def delete_notes(note_id: int):
    query = notesTableObj.delete().where(notesTableObj.c.id == note_id)
    await database.execute(query)
    return {"message": "Note with id = {} got deleted successfully.".format(note_id)}