import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def centarl_function():
    return {"Name": "Muaeen"}

if __name__ == "__main__":
    uvicorn.run(app, port=2000, host="0.0.0.0")
