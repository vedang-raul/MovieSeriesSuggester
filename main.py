from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def Root():
    return{"Message": "Welcome to the Movie/Series suggestor. Find your next favorite movie here!!"} 