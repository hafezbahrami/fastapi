
# 1 Databse
Here we want to use PostgreSQL as our Sequel databse to store data.

We use SQLAlchemy as a genral tool to connect the Python objects (table object, column object, ..) to Tables, Columns,... in the PostgreSQL database.
SQLAlchemy is genral tool and suport many other dialects other than PostgreSQL (such as mySQL, Oracle, ...)

## 1-1 How to connect to PostgreSQL
First of all, PostgreSQL is a server, is container that runs by a server getting request on a port (like 5432)

We want to create our container in Python with "uvicorn" server and FastAPI (as the Web API) that will connect
to the PostgreSQL container/server

All the infomration on how to connect to PostgreSQL will be sent through a URL:
postgresql://user_name:pass@local_host:5432/database_name

## 1-2 How to save credentials in ENV variables
The best way to use ENV variable is to run below command to look for the "XX_var_in_ENV" and if not found that variable as the ENV variable, then it automatically returns the 
YY as the value to prevent the crash:

my_var_in_python = os.environ.get('XX_var_in_ENV', 'YY')

## 1-3 How to start the PostgreSQL server/container
1) We can use pgAdmin to start the PostgreSQL server

2) It requires a master pass to connect to all servers, and another local pass to connect to speciifc server

3) In the final connectetd server, we might see many databases. We should look for the database name that we want to get connected through our Python progam, and through the SQL Alchemy. Here, we are looking for a databse named "fastapi".

4) With a good connection to the "fastpai" database in PostgreSQL, we can go to Schemas//Public//Tables, and look for table named "notes". This table was created as an object with the same name "notes" in our python program


## 1-4 How does the Alchemy helps
(1) Create the meta data: meta data contains all our Table and/or Column objects, and get them ready to be sent to PostgreSQL through firing an Engine

```python
meta_data = sqlalchemy.MetaData()
```

(2) Create the Table and COlumn object within this meat data:
Below, the name of Table object is "note", also is is named "note" in PostgreSQL as table.
Also, as seen, it is defined  within meta_data.

```python
notes = sqlalchemy.Table(
    "notes",
    meta_data,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

```
3) create an engine:

We can first create an engine that look at the specific URL of a specific database:

```python
engine = sqlalchemy.create_engine(URL)
```

Then, we can create all the objects within our meta data through this engine:
```python
meta_data.create_all(engine)
```

# 2 FastAPI and Python Segment

## 2-1 database package
The database package will provide us the asyncronous capabilities, when executing the queries


## 2-2 connectand disconnect to database
We will do it on event base, and using the decoration provided in FastAPI. So, it will connect to our database in PostgreSQL at the begining, and will disconnet after done

```python
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

```

## 2-3 SQLAlchemy provides method to create query
For a Table_Objet created within a meta data, in SQLAlchemy, provides several method to create 
query. These include: 

Tabel_Object.insert()

Tabel_Object.update()

Tabel_Object.select()

Tabel_Object.delete()

## 2-4 an example of API
Here is an example:

```python
@app.post("/notes/", response_model=Note)
async def create_node(noteIn: NoteIn):
    query = notesTableObj.insert().values(text=noteIn.text, completed=noteIn.completed)
    last_record_id = await database.execute(query)
    return {**noteIn.dict(), "id":last_record_id}

```

Line
```python
@app.post("/notes/", response_model=Note)
```
Is a decorative provided by FastAPI, and for posting a query into a Table in the target database.

"/notes/" is the URL accessible through Swagger.

"response_mdeol=Note" just basically mentions that the response back to Swagger must be type of Note class (Pydantic validation) otherwise it will throw an exception.

```python
    query = notesTableObj.insert().values(text=noteIn.text, completed=noteIn.completed)
```
here is just creating  query that PostgreSQL will underrstand. The notesTableObj object (an object fromSQLAlchemy)
provides us ".inser()" method, and then in the ".value()" we use those attributes that already being defined in
notesTableObj object (i.e: text and completed).

```python
async def create_node(noteIn: NoteIn):
```
words "async" or "await" in front of execution of databse

```python
return {**noteIn.dict(), "id":last_record_id}
```
reponse will be an object from type specified in response_model. FastAPI will convert the dictionary into JSON


# 3 Start the APP and Server running the FastAPI
use:
uvicorn main:app --reload

If the "notes" table does not exist in the PostgreSQL, by starting the application/container/server by above command
we will create the "notes" table in the PostgreSQL, once the code-interpretato reaches the following line:
```python
meta_data.create_all(engine)
```
To check if the table is created after this line, we need to refresh the Table section of the database named "fastapi" in the PostgreSQL.


# Main reference
https://www.youtube.com/watch?v=YUuuJPokBf4