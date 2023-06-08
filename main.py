from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from Api.Routes.recordsRoutes import recordRoutes
from Api.Routes.defaultRoute import defaultRoute

app = FastAPI(title="FastAPI-DM-Backend",description = "CRUD API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(recordRoutes,tags=['Users'], prefix='/api')
app.include_router(defaultRoute)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8090)


