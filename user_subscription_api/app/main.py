import logging

# import aioredis
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings, LOG_CONFIG
from tags import tags_metadata
from api.v1 import user_router, service_router, product_router

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
    # redis_cache.redis = await aioredis.create_redis_pool((config.REDIS_HOST, config.REDIS_PORT),
    #                                                      minsize=10,
    #                                                      maxsize=20,
    #                                                      timeout=1)
    # es_storage.es = AsyncElasticsearch(hosts=[f"{config.ELASTIC_HOST}:{config.ELASTIC_PORT}"])


@app.on_event("shutdown")
async def shutdown():
    pass
    # await redis_cache.redis.close()
    # await es_storage.es.close()


app.include_router(user_router, prefix="/api/v1/user", tags=["user"])
app.include_router(product_router, prefix="/api/v1/product", tags=["product"])
app.include_router(service_router, prefix="/api/v1/service", tags=["service"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOG_CONFIG,
        log_level=logging.DEBUG,
        reload=settings.debug,
    )