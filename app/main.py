import uvicorn

from fastapi_share_core import add_share_core
from fastapi import FastAPI

app = FastAPI()
add_share_core(app, enable_redis=True)

if __name__ == '__main__':
    uvicorn.run(app)
