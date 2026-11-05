from fastapi import FastAPI
import uvicorn

app = FastAPI(title="projects_time")

if __name__ == "__main__":
  uvicorn.run("main:app", host="127.0.0.1", port=9000)
