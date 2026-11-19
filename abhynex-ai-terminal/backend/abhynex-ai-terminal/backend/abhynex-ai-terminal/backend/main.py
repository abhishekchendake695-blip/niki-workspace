from fastapi import FastAPI
from api.routes import router
import uvicorn

app = FastAPI(title="ABHYNEX AI TERMINAL API")

app.include_router(router)

@app.get("/")
def read_root():
    return {"status": "online", "project": "ABHYNEX AI TERMINAL"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)