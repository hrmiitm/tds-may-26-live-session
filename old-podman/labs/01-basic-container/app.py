from fastapi import FastAPI

app = FastAPI(title="Container Demo")

@app.get("/")
def home():
    return {"message": "Hello from a container"}
