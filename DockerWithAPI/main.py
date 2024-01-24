import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def centarl_function():
    return {"Name": "Muaeen"}

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="127.0.0.1")
