import routers

from fastapi import FastAPI

app = FastAPI()

app.include_router(routers.v1)
app.include_router(routers.v2)
