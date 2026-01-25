import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Erlaubt, dass deine Webseite diese API aufrufen darf
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/random-location")
def random_location():
    lat = random.uniform(35.0, 71.0)
    lon = random.uniform(-10.0, 40.0)

    return {
        "latitude": round(lat, 6),
        "longitude": round(lon, 6)
    }
