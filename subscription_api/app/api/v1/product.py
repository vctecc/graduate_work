from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas import Product, ProductDetail
from app.services import ProductService, get_product_service
from .error_messag import PRODUCT_NOT_FOUND

product_router = APIRouter()


@product_router.get("/",
                    response_model=List[Product],
                    status_code=HTTPStatus.OK)
async def get_all_products(
        service: ProductService = Depends(get_product_service)
) -> List[Product]:
    return await service.get_all()


@product_router.get("/active",
                    response_model=List[Product],
                    status_code=HTTPStatus.OK)
async def get_active_product(
        service: ProductService = Depends(get_product_service)
) -> List[Product]:
    return await service.get_all(only_active=True)


@product_router.get("/{product_id}",
                    response_model=ProductDetail,
                    status_code=HTTPStatus.OK)
async def get_product_details(
        product_id: str = Query(None),
        service: ProductService = Depends(get_product_service)
) -> ProductDetail:
    product = await service.get(product_id)
    if not product:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=PRODUCT_NOT_FOUND)

    return product
