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
    return {"status": "Movie Suggester API is running!"}


# THIS IS THE ENDPOINT YOU NEED TO ADD
@app.get("/api/search/{movie_title}")
async def search_movie(movie_title: str):

