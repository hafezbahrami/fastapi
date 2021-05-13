

# Databse
Here we use in-memory database, meaning by the time we shut down the server / container, we will loose all data

# The API (FastAPI, or Web API)
We first instantiate the FastAPI object by: app = FastAPI()
This is just an API, and need a server to serve this API

The FastAPI object (app) now exposes many useful http requests tool that we can use

# The Server
We can fire up a server, using uvicorn or hypercorn, to serve our FastAPI (the Web API)

After going to venv environment, run the following:
heypercorn cityapi/main:app -reload

# The documentation
After firing up the server, now probably a local server (localhost://8000) is listening. The FastAPI offers two types of documentation:
1) Swagger:
localhost:8000/docs

2) 
localhost:8000/redoc

Examples of city that we can try to "post" first:
"name": "Los Vegas"
"timezone": "America/Los_Angeles"

"name": "Miami"
"timezone": "America/New_York"

After entering the data in Swagger, try to see if you get 200 reponse code (for a successful execution)

After posting, we can "get" the data from our in-memory database:


# Main reference
https://www.youtube.com/watch?v=kCggyi_7pHg&t=804s

