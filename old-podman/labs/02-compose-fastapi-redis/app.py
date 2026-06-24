import os
from fastapi import FastAPI
import redis

app = FastAPI(title="FastAPI + Redis Compose Demo")
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.from_url(redis_url, decode_responses=True)

@app.get("/")
def home():
    return {"message": "Open /count to increment Redis counter"}

@app.get("/count")
def count():
    value = r.incr("visits")
    return {"visits": value, "redis_url": redis_url}
