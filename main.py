import os
import uvicorn
import config
from fastapi import FastAPI
from api import spelling, tag, writing

app = FastAPI()

port = int(os.environ.get("GUIDE_PORT", 8003))

app.include_router(spelling.router)
app.include_router(tag.router)
app.include_router(writing.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)

@app.get("/")
async def root():
    return {"message": "Hello World"}