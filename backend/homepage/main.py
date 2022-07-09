from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def return_homepage():
    return {
        "application": "Paperlens",
        "version": "0.0.1",
        "contributor": "nigelx"
    }
