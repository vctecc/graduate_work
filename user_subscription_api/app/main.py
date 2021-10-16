import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api.v1 import product_router, service_router, user_router
from app.core.config import LOG_CONFIG, settings
from tags import tags_metadata

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    openapi_tags=tags_metadata
)


@app.on_event("startup")
async def startup():
    pass
    # redis_cache.redis = await aioredis.create_redis_pool()


@app.on_event("shutdown")
async def shutdown():
    pass
    # await redis_cache.redis.close()


app.include_router(user_router, prefix="/api/v1/user", tags=["user"])
app.include_router(product_router, prefix="/api/v1/product", tags=["product"])
app.include_router(service_router, prefix="/api/v1/service", tags=["service"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        log_config=LOG_CONFIG,
        log_level=logging.DEBUG,
        reload=settings.debug,
    )
