import logging

import stripe
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from src.api.v1 import payment
from src.core.config import settings
from src.core.logger import LOGGING
from src.common.tests import patch_services

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    stripe.api_key = settings.stripe_secret_key

    if settings.test:
        patch_services()


@app.on_event("shutdown")
async def shutdown():
    ...  # noqa: WPS428


app.include_router(payment.router, prefix="/v1", tags=["payment"])

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    reload = settings.debug
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # noqa: S104
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=reload,
    )
