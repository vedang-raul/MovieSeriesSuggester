# main.py

import os
import httpx
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv() # Load variables from the .env file
app = FastAPI()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_READ_ACCESS_TOKEN = os.getenv("TMDB_READ_ACCESS_TOKEN")
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
    if not TMDB_READ_ACCESS_TOKEN:
        raise HTTPException(status_code=500,detail="TMDB READ ACCESS TOKEN key is not configured.")
    search_url= f"{TMDB_API_URL}/search/movie"
    headers = {
        "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}",
        "accept": "application/json"
    }
    params={
        "query":movie_title
        }
    async with httpx.AsyncClient() as client: #This line create a fresh request page with is sent to the API
        try:
            response = await client.get(search_url,headers=headers,params=params) #This is the main event, this is where we send the request to 
                                                                  #the API for the movie. using search_url and params
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()  #This line parses (coverts kinda) the response to JSON format and returns it
        except httpx.HTTPStatusError as exc: #This block catches erros when you successfully connected to the API but the API rejected your request
            raise HTTPException(status_code=exc.response.status_code,detail=f"Error from TMDB API{exc.response.text}") #Take the error msg sent from TMDB and show it to user
        except httpx.RequestError as exc: #This block catches errors when you couldn't connect to the API at all
            raise HTTPException(status_code=503,detail=f"Error connecting to TMDB API server{exc}")
@app.get("/api/popular")
async def show_pop_movies():
    # This endpoint fetches popular movies from TMDB
    if not TMDB_READ_ACCESS_TOKEN:
        raise HTTPException(status_code=500,detail="TMDB READ ACCESS TOKEN key is not configured.")
    search_url= f"{TMDB_API_URL}/movie/popular"
    headers = {
        "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}",
        "accept": "application/json"
    }
    params={
        "language": "en-US",
        "page":1
    }
    async with httpx.AsyncClient() as client:
        try:
            response= await client.get(search_url,headers=headers,params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code,detail=f"Error connecting to the TMDB API: {exc.response.text}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503,detail=f"Error connecting to the TMDB API server: {exc}")
@app.get("/api/search/tv/{query}")
async def search_series(query:str):
    if not TMDB_READ_ACCESS_TOKEN:
        raise HTTPException(status_code=500,detail="TMDB READ ACCESS TOKEN key is not configured.")
    search_url= f"{TMDB_API_URL}/search/tv"
    headers = {
        "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}",
        "accept": "application/json"
    }
    params={
        "query": query,
        "language": "en-US"
    }
    async with httpx.AsyncClient() as client: #This line create a fresh request page with is sent to the API
        try:
            response = await client.get(search_url,headers=headers,params=params) #This is the main event, this is where we send the request to 
                                                                  #the API for the movie. using search_url and params
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()  #This line parses (coverts kinda) the response to JSON format and returns it
        except httpx.HTTPStatusError as exc: #This block catches erros when you successfully connected to the API but the API rejected your request
            raise HTTPException(status_code=exc.response.status_code,detail=f"Error from TMDB API{exc.response.text}") #Take the error msg sent from TMDB and show it to user
        except httpx.RequestError as exc: #This block catches errors when you couldn't connect to the API at all
            raise HTTPException(status_code=503,detail=f"Error connecting to TMDB API server{exc}")
@app.get("/api/details/movie/{movie_id}")
async def get_movie_details(movie_id : int):
    if not TMDB_READ_ACCESS_TOKEN:
        raise HTTPException(status_code=500,detail="TMDB READ ACCESS TOKEN key is not configured.")
    det_url= f"{TMDB_API_URL}/movie/{movie_id}"
    headers = {
        "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}",
        "accept": "application/json"
    }
    params={
        "language": "en-US"
    }
    async with httpx.AsyncClient() as client:
        try:
            response =await client.get(det_url,headers=headers,params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code,detail=f"Error from TMDB API: {exc.response.text}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503,detail=f"Error connecting to TMDB API server: {exc}") 
@app.get("/api/details/tv/{tv_id}")
async def det_tv(tv_id: int):
    if not TMDB_READ_ACCESS_TOKEN:
        raise HTTPException(status_code=500,detail="TMDB READ ACCESS TOKEN key is not configured.")
    det_url= f"{TMDB_API_URL}/tv/{tv_id}"
    headers={
        "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}",
        "accept": "application/json"        
    }
    params={
        "language": "en-US"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(det_url,headers=headers,params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code,detail=f"Error from TMDB API: {exc.response.text}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503,detail=f"TMDB API server error: {exc}")
@app.get("/api/movie/{movie_id}")
async def movie_detail(movie_id: int):
    if not TMDB_READ_ACCESS_TOKEN:
        raise HTTPException(status_code=500,detail="TMDB READ ACCESS TOKEN key is not configured.")
    det_url= f"{TMDB_API_URL}/movie/{movie_id}"
    headers={
        "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}",
        "accept": "application/json"
    }
    params={
        "language": "en-US"
    }
    async with httpx.AsyncClient() as client:
        try:
        
            response = await client.get(det_url,headers=headers,params=params)
            response.raise_for_status()
            data= response.json()
            genres=", ".join([genre["name"] for genre in data.get("genres",[])])
            budget=f"${data.get("budget",0):,}" if data.get("budget") else "N/A"
            revenue=f"${data.get("revenue", 0):,}" if data.get("revenue") else "N/A"

            details={
                "title": data.get("title"),
                "overview": data.get("overview"),
                "release_date": data.get("release_date"),
                "genres": genres,
                "runtime": f"{data.get('runtime')} minutes" if data.get("runtime") else "N/A",
                "budget": budget,
                "revenue": revenue,
                "vote_average": data.get("vote_average"),
                "vote_count": data.get("vote_count")

            }
            return details
            
        except httpx.HTTPStatusError as exc:
           raise HTTPException(status_code=exc.response.status_code,detail=f"Error from TMDB API: {exc.response.text}")
        except httpx.RequestError as exc:
           raise HTTPException(status_code=503,detail=f"TMDB API server error: {exc}")
