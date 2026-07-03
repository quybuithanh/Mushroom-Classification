from fastapi import FastAPI

app = FastAPI(
    title="Mushroom Classification API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Mushroom Classification API"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }