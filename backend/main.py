from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import api
from database.db import engine
from database.models import Base
from setting.meta import title, description, version, tags_metadata


app = FastAPI(
    title=title,
    description=description,
    version=version,
    openapi_tags=tags_metadata
)

Base.metadata.create_all(bind=engine)
app.include_router(api.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)