import logging

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import payment
from core import config
from core.config import DEBUG
from core.logger import LOGGING

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass


app.include_router(payment.router, prefix="/api/v1/payment", tags=["payment"])


if __name__ == '__main__':
    reload = DEBUG
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=reload,
    )
