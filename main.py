from fastapi import FastAPI
import uvicorn
from api.routers import routers

app = FastAPI(title="projects_time")
app.include_router(routers)

if __name__ == "__main__":
  uvicorn.run("main:app", host="127.0.0.1", port=9000)
