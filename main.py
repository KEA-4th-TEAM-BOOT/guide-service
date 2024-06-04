import os
import uvicorn
import config
from fastapi import FastAPI
from api import spelling, tag, writing
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

port = int(os.environ.get("GUIDE_PORT", 8003))

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

app.include_router(spelling.router)
app.include_router(tag.router)
app.include_router(writing.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

@app.get("/health/liveness")
async def liveness():
    return {"status": "alive"}

@app.get("/health/readiness")
async def readiness():
    return {"status": "ready"}

@app.get("/")
async def root():
    return {"message": "Hello World"}