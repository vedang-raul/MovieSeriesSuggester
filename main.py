# main.py

import os
import httpx
import random
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
    "null",
    "https://vedang-raul.github.io",
    "https://vedang-raul.github.io/MovieSeriesSuggester"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# async def movie_detail_helper(movie_id):
#     if not TMDB_READ_ACCESS_TOKEN:
#         raise HTTPException(status_code=500,detail="TMDB READ ACCESS TOKEN key is not configured.")
#     det_url= f"{TMDB_API_URL}/movie/{movie_id}"
#     headers={
#         "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}",
#         "accept": "application/json"
#     }
#     params={
#         "language": "en-US"
#     } 
#     async with httpx.AsyncClient() as client:
#         try:
        
#             response = await client.get(det_url,headers=headers,params=params)
#             response.raise_for_status()
#             data= response.json()
#             genres=", ".join([genre["name"] for genre in data.get("genres",[])])  #it appends genres with a comma and if nothing is there in genres it returns an empty list
#             budget=f"${data.get("budget",0):,}" if data.get("budget") else "N/A"  #adds a $ and a comma in appropriate places if budget is there else returns N/A
#             revenue=f"${data.get("revenue", 0):,}" if data.get("revenue") else "N/A" #adds a $ and a comma in appropriate places if revenue is there else returns N/A

#             details={
#                 "title": data.get("title"),
#                 "overview": data.get("overview"),
#                 "release_date": data.get("release_date"),
#                 "genres": genres,
#                 "runtime": f"{data.get('runtime')} minutes" if data.get("runtime") else "N/A",
#                 "budget": budget,
#                 "revenue": revenue,
#                 "vote_average": data.get("vote_average"),
#                 "vote_count": data.get("vote_count"),
#                 "tagline": data.get("tagline"),
#                 "poster_path": f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}" if data.get("poster_path") else None,
                

#             }
#             return details
            
#         except httpx.HTTPStatusError as exc:
#            raise HTTPException(status_code=exc.response.status_code,detail=f"Error from TMDB API: {exc.response.text}")
#         except httpx.RequestError as exc:
#            raise HTTPException(status_code=503,detail=f"TMDB API server error: {exc}")

# --- API Endpoints ---

@app.get("/")
def read_root():
    """ A simple root endpoint to check if the server is running. """
    return {"status": "Movie Suggester is running!"}



@app.get("/api/search/movie/{query}")
async def search_movie(query: str):
    if not TMDB_READ_ACCESS_TOKEN:
        raise HTTPException(status_code=500,detail="TMDB READ ACCESS TOKEN key is not configured.")
    search_url= f"{TMDB_API_URL}/search/movie"
    headers = {
        "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}",
        "accept": "application/json"
    }
    params={
        "query":query
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
            genres=", ".join([genre["name"] for genre in data.get("genres",[])])  #it appends genres with a comma and if nothing is there in genres it returns an empty list
            budget=f"${data.get("budget",0):,}" if data.get("budget") else "N/A"  #adds a $ and a comma in appropriate places if budget is there else returns N/A
            revenue=f"${data.get("revenue", 0):,}" if data.get("revenue") else "N/A" #adds a $ and a comma in appropriate places if revenue is there else returns N/A

            details={\
                "id": data.get("id"),
                "title": data.get("title"),
                "overview": data.get("overview"),
                "release_date": data.get("release_date"),
                "genres": genres,
                "runtime": f"{data.get('runtime')} minutes" if data.get("runtime") else "N/A",
                "budget": budget,
                "revenue": revenue,
                "vote_average": data.get("vote_average"),
                "vote_count": data.get("vote_count"),
                "tagline": data.get("tagline"),
                "poster_path": f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}" if data.get("poster_path") else None,
                

            }
            return details
            
        except httpx.HTTPStatusError as exc:
           raise HTTPException(status_code=exc.response.status_code,detail=f"Error from TMDB API: {exc.response.text}")
        except httpx.RequestError as exc:
           raise HTTPException(status_code=503,detail=f"TMDB API server error: {exc}")
@app.get("/api/tv/{tv_id}")
async def tv_detail(tv_id: int):
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
            data= response.json()
            genres=", ".join([genre["name"] for genre in data.get("genres",[])])  #it appends genres with a comma and if nothing is there in genres it returns an empty list
            creators=", ".join([creator["name"] for creator in data.get("created_by",[])])  #it appends genres with a comma and if nothing is there in genres it returns an empty list
            details={
                "original_name": data.get("original_name"),
                "overview": data.get("overview"),
                "first_air_date": data.get("first_air_date"),
                "last_air_date": data.get("last_air_date"),
                "status": data.get("status"),
                "genres": genres,
                "number_of_episodes": data.get("number_of_episodes"),
                "number_of_seasons": data.get("number_of_seasons"),
                "vote_average": data.get("vote_average"),
                "vote_count": data.get("vote_count"),
                "creators": creators,
                "tagline": data.get("tagline"),
                "poster_path": f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}" if data.get("poster_path") else None

            }
            return details
            
        except httpx.HTTPStatusError as exc:
           raise HTTPException(status_code=exc.response.status_code,detail=f"Error from TMDB API: {exc.response.text}")
        except httpx.RequestError as exc:
           raise HTTPException(status_code=503,detail=f"TMDB API server error: {exc}")
@app.get("/api/tv/{tv_id}/credits")
async def tv_credits(tv_id: int):
    if not TMDB_READ_ACCESS_TOKEN:
        raise HTTPException(status_code=500,detail="TMDB READ ACCESS TOKEN is not configured.")
    url= f"{TMDB_API_URL}/tv/{tv_id}/credits"
    headers={
        "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}",
    }
    params={
        "language": "en-US"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url,headers=headers,params=params)
            response.raise_for_status()
            data= response.json()
            cast = data.get('cast', [])
            top_cast_names = [f"{member.get('name')} as {member.get('character')}" for member in cast[:4]]
            return top_cast_names
        except httpx.HTTPStatusError as exc:
           raise HTTPException(status_code=exc.response.status_code,detail=f"Error from TMDB API: {exc.response.text}")
        except httpx.RequestError as exc:
           raise HTTPException(status_code=503,detail=f"TMDB API server error: {exc}")
@app.get("/api/movie/{movie_id}/credits")
async def movie_credits(movie_id: int):
    if not TMDB_READ_ACCESS_TOKEN:
        raise HTTPException(status_code=500,detail="TMDB READ ACCESS TOKEN is not configured.")
    url= f"{TMDB_API_URL}/movie/{movie_id}/credits"
    headers={
        "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}",
    }
    params={
        "language": "en-US"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url,headers=headers,params=params)
            response.raise_for_status()
            data= response.json()
            cast = data.get('cast', [])
            top_cast_names = [f"{member.get('name')} as {member.get('character')}" for member in cast[:4]]
            return top_cast_names
        except httpx.HTTPStatusError as exc:
           raise HTTPException(status_code=exc.response.status_code,detail=f"Error from TMDB API: {exc.response.text}")
        except httpx.RequestError as exc:
           raise HTTPException(status_code=503,detail=f"TMDB API server error: {exc}")
@app.get("/api/movie/watch/{movie_id}")
async def watch_movie(movie_id : int):
    if not TMDB_READ_ACCESS_TOKEN:
        raise HTTPException(status_code=500,detail="TMDB read access token is not configured.")
    url=f"{TMDB_API_URL}/movie/{movie_id}/watch/providers"
    headers={
        "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}",
    }
    params={
        "language":"en-US"
    }
    async with httpx.AsyncClient() as client:
        try:
            response= await client.get(url,headers=headers,params=params)
            response.raise_for_status()
            data=response.json()
            watch_providers = data.get("results", {}).get("IN", {})
            flatrate_providers = watch_providers.get("flatrate", [])
    
            top_services = [
            {
                "name": provider.get('provider_name'),
                "logo_path": provider.get('logo_path')
            } 
            for provider in flatrate_providers[:4]
            ]
            return {"providers": top_services}
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code,detail=f"Error from TMDB API: {exc.response.text}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503,detail=f"TMDB API server error: {exc}")
@app.get("/api/tv/watch/{tv_id}")
async def watch_tv(tv_id : int):
    if not TMDB_READ_ACCESS_TOKEN:
        raise HTTPException(status_code=500,detail="TMDB read access token is not configured.")
    url=f"{TMDB_API_URL}/tv/{tv_id}/watch/providers"
    headers={
        "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}",
    }
    params={
        "language":"en-US"
    }
    async with httpx.AsyncClient() as client:
        try:
            response= await client.get(url,headers=headers,params=params)
            response.raise_for_status()
            data=response.json()
            watch_providers = data.get("results", {}).get("IN", {})
            flatrate_providers = watch_providers.get("flatrate", [])
    
            top_services = [
            {
                "name": provider.get('provider_name'),
                "logo_path": provider.get('logo_path')
            } 
            for provider in flatrate_providers[:4]
            ]
            return {"providers": top_services}
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code,detail=f"Error from TMDB API: {exc.response.text}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503,detail=f"TMDB API server error: {exc}")
@app.get("/api/surprise_me/movie")
async def surprise_movie():
    if not TMDB_READ_ACCESS_TOKEN:
        raise HTTPException(status_code=500,detail="TMDB READ ACCESS TOKEN key is not configured.")
    url= f"{TMDB_API_URL}/movie/top_rated"
    headers = {
        "Authorization": f"Bearer {TMDB_READ_ACCESS_TOKEN}"
    }
    params={
        "language": "en-US",
        "page":random.randint(1,10)
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=url,headers=headers,params=params)
            response.raise_for_status()
            data= response.json()
            results_tmdb=data.get("results",[])
            surprise_movie = results_tmdb[random.randint(1,20)]
            id = surprise_movie.get("id")
            result = id

            

            return {"results":result}
        except httpx.HTTPStatusError as exc:
              raise HTTPException(status_code=exc.response.status_code,detail=f"Error from TMDB API: {exc.response.text}")
        except httpx.RequestError as exc:
              raise HTTPException(status_code=503,detail=f"TMDB API server error: {exc}")
@app.get("/api/surprise_me/tv")
async def surprise_tv():
    if not TMDB_READ_ACCESS_TOKEN:
        raise HTTPException(status_code=500,detail="TMDB READ ACCESS TOKEN not configured.")
    url=f"{TMDB_API_URL}/tv/top_rated"
    headers={
        "Authorization":f"Bearer {TMDB_READ_ACCESS_TOKEN}"
    }
    params={
        "language":"en-US",
        "page":random.randint(1,10)
    }
    async with httpx.AsyncClient() as client:
        try:
            response= await client.get(url=url,headers=headers,params=params)
            response.raise_for_status()
            data=response.json()
            results_tmdb=data.get("results",[])
            surprise_tv=results_tmdb[random.randint(1,20)]
            id=surprise_tv.get("id")
            results=await tv_detail(id)
            return results
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code,detail=f"Error from TMDB API: {exc.response.text}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503,detail=f"TMDB API server error: {exc}")

