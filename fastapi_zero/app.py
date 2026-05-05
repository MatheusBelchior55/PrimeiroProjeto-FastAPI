from fastapi import FastAPI

from fastapi_zero.routers import auth, users
from fastapi_zero.schemas import Message

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)


@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}
