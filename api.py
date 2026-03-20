from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search import search

#This is the API Layer that exposes the search funtionality as an API endpoint. 
# We are using FastAPI to create a simple API that accepts search queries and returns relevant courses based on the search engine logic defined in the search module. 
app = FastAPI()

#Allow react app to talk to this API
#https://fastapi.tiangolo.com/tutorial/cors/#use-corsmiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], #allowing requests from the React app running on localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/search")
def search_courses(query: str):
    """
    API endpoint to search for courses based on a user query. 
    It takes a query string as input, calls the search function from the search module, and returns the search results in a structured format.
    """
    results = search(query) # calling the search function from the search module to retrieve relevant courses based on the user query
    return results # returning the search results as a response to the API call