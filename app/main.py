import uvicorn

from fastapi import FastAPI
from fastapi_share_core import add_share_core
from fastapi_share_core.plugins import rbac

app = FastAPI()
add_share_core(app, enable_db=True)
app.include_router(rbac.router)

if __name__ == '__main__':
    uvicorn.run(app)
