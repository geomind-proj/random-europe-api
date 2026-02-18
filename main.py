import random
import geopandas as gpd
from shapely.geometry import Point
from fastapi import FastAPI

app = FastAPI()

# -----------------------------
# LOAD GEO DATA (ONCE AT START)
# -----------------------------
land = gpd.read_file("data/ne_10m_land.shp")
countries = gpd.read_file("data/ne_10m_admin_0_countries.shp")

# Exclude Russia & Belarus
excluded = countries[countries["ADMIN"].isin(["Russia", "Belarus"])]

# Europe bounding box (includes Iceland, Turkey, Svalbard)
europe_bbox = land.cx[-30:45, 30:75]

# Remove excluded countries from land
europe_land = gpd.overlay(
    europe_bbox,
    excluded,
    how="difference"
)

# Merge into single geometry
EUROPE_LAND = europe_land.geometry.union_all()

MINX, MINY, MAXX, MAXY = EUROPE_LAND.bounds

# -----------------------------
# RANDOM POINT ON LAND
# -----------------------------
def random_point_on_land():
    while True:
        lon = random.uniform(MINX, MAXX)
        lat = random.uniform(MINY, MAXY)
        point = Point(lon, lat)

        if EUROPE_LAND.contains(point):
            return lat, lon

# -----------------------------
# API ENDPOINT
# -----------------------------
@app.get("/random-location")
def random_location():
    lat, lon = random_point_on_land()
    return {
        "latitude": round(lat, 6),
        "longitude": round(lon, 6)
    }
