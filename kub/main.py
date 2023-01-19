from fastapi import FastAPI
import sys
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.background import BackgroundTask
import asyncio
import os


app = FastAPI()


@app.on_event('shutdown')
def shutdown_event():
    print('Shutting down...!')
    
async def exit_app():
    loop = asyncio.get_running_loop()
    loop.stop()
    
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    task = BackgroundTask(exit_app)
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code, background=task)

@app.get("/")
async def home():
    return {"message": "Hello World"}

@app.post("/create")
async def info(data: str):
    file_path = os.path.join(os.path.join(os.getcwd(), "data"), "info.txt")

    print("Writing data to file {}".format(file_path))
    with open(file_path, "w") as f:
        f.write(data)
        print("Wrote data to file")
    return {"Info": data}

@app.get("/read")
async def info():
    data = None
    file_path = os.path.join(os.path.join(os.getcwd(), "data"), "info.txt")
    
    print("Reading data from file")

    try:
        with open(file_path, "r") as f:
            data = f.read()
    except (IOError, OSError) as error:
        print("Resource Not Found")
        return "Resource Not Found"

    print("Read data from file")
    return {"Info": data}

@app.get("/error")
async def exit():
    raise HTTPException(status_code=500, detail='Something went wrong')