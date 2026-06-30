from fastapi import FastAPI

app = FastAPI(
    title="Drone Cloud Project",
    description="Secure Private Cloud for Live Video Transmission",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "Drone Cloud Project Backend Running",
        "status": "OK"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }
