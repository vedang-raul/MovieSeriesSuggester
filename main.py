# main.py

import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv() # Load variables from the .env file
app = FastAPI()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_API_URL = "https://api.themoviedb.org/3"

# --- Security (CORS) ---
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500",
    "null"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---

@app.get("/")
def read_root():
    """ A simple root endpoint to check if the server is running. """
    return {"status": "Movie Suggester is running!"}


# THIS IS THE ENDPOINT YOU NEED TO ADD
@app.get("/api/search/{movie_title}")
async def search_movie(movie_title: str):
    if not TMDB_API_KEY:
        raise HTTPException(status_code=500,detail="TMDB API key is not configured.")
    search_url= f"{TMDB_API_URL}/search/movie"

    params={
        "api_key": TMDB_API_KEY,
        "query":movie_title
        }
    async with httpx.AsyncClient() as client: #This line create a fresh request page with is sent to the API
        try:
            response = await client.get(search_url,params=params) #This is the main event, this is where we send the request to 
                                                                  #the API for the movie. using search_url and params
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()  #This line parses (coverts kinda) the response to JSON format and returns it
        except httpx.HTTPStatusError as exc: #This block catches erros when you successfully connected to the API but the API rejected your request
            raise HTTPException(status_code=exc.response.status_code,detail=f"Error from TMDB API{exc.response.text}") #Take the error msg sent from TMDB and show it to user
        except httpx.RequestError as exc: #This block catches errors when you couldn't connect to the API at all
            raise HTTPException(status_code=503,detail=f"Error connecting to TMDB API server{exc}")
    #Retry code block in case of connection issues
    attemps = 10 #How many times it try to fetch the data from the API
    delay = 1   #how much time gap inbetween tries
    for i in range(attemps):
        try:
            async with httpx.AsyncClient() as client:
                response=client.get(search_url,params=params)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as exc:
            if i < attemps - 1: #If this is not the last attempt
                import asyncio
                await aysncio.time.sleep(delay)  # Wait before retrying
                delay = delay * 2
                return {"Message":"Retrying......."} #give breathing time to the api fetch request
                continue
            else:
                print("All attemps failed.")
                raise HTTPException(sattus_code=503,detail=f"Error connecting to TMDB API server{exc}")
@app.get("/api/popular")
async def show_pop_movies():
    # This endpoint fetches popular movies from TMDB
    if not TMDB_API_KEY:
        raise HTTPException(status_code=500,detail=f"TMDB API key is not configured.")
    url=f"{TMDB_API_URL}/movie/popular"
    params={
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "page":1
    }
    async with httpx.AsyncClient() as client:
        try:
            response= await client.get(url,params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code,detail=f"Error connecting to the TMDB API: {exc.response.text}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503,detail=f"Error connecting to the TMDB API server: {exc}")
@app.get("/api/search/tv/{query}")
async def search_series(query:str):
    if not TMDB_API_KEY:
        raise HTTPException(status_code=500,detail="TMDB API key is not configured.")
    search_url=f"{TMDB_API_URL}/search/tv"
    params={
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "en-US"
    }
    async with httpx.AsyncClient() as client: #This line create a fresh request page with is sent to the API
        try:
            response = await client.get(search_url,params=params) #This is the main event, this is where we send the request to 
                                                                  #the API for the movie. using search_url and params
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()  #This line parses (coverts kinda) the response to JSON format and returns it
        except httpx.HTTPStatusError as exc: #This block catches erros when you successfully connected to the API but the API rejected your request
            raise HTTPException(status_code=exc.response.status_code,detail=f"Error from TMDB API{exc.response.text}") #Take the error msg sent from TMDB and show it to user
        except httpx.RequestError as exc: #This block catches errors when you couldn't connect to the API at all
            raise HTTPException(status_code=503,detail=f"Error connecting to TMDB API server{exc}")