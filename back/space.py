from fastapi import FastAPI, Body
from pydantic import BaseModel
from datetime import datetime, timezone
import ephem
import uvicorn
import math

class Constellation(BaseModel):
    time_data: str
    lat: float
    lon: float

app = FastAPI()

Planet_body = {
    "Sun": ephem.Sun,
    "Moon": ephem.Moon,
    "Mars": ephem.Mars,
    "Venus": ephem.Venus,
    "Jupiter": ephem.Jupiter,
    "Saturn": ephem.Saturn,
    "Uranus": ephem.Uranus,
    "Neptune": ephem.Neptune,
}

@app.get("/api/constellation/current")
async def get_current_constellation():
    planets = list(Planet_body.keys())
    current_hour = datetime.now(timezone.utc).hour
    body_name = planets[current_hour % len(planets)]

    planet_class = Planet_body[body_name]
    body = planet_class()
    body.compute(datetime.now(timezone.utc))
    code, name = ephem.constellation(body)

    return {
        "body": body.name,
        "constellation_code": code,
        "constellation_name": name
    }

@app.post("/api/calculation")
async def calculate_the_system(data: Constellation):
    constellation = Constellation(
        time_data=data.time_data,
        lat=data.lat,
        lon=data.lon
    )
    observer = ephem.Observer()
    observer.lat = math.radians(constellation.lat)
    observer.lon = math.radians(constellation.lon)
    observer.date = constellation.time_data

    zenith = observer.radec_of(0, math.pi / 2)

    if not isinstance(zenith, tuple):
        zenith = (zenith.ra, zenith.dec) 
    code, name = ephem.constellation(zenith)

    return {
        "lat": constellation.lat,
        "lon": constellation.lon,
        "date": constellation.time_data, 
        "constellation_code": code,
        "constellation_name": name
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, ssl_keyfile="key.pem", ssl_certfile="cert.pem")

