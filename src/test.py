from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    print("test")
    return {"message": "Hello World"}