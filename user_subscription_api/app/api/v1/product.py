from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from core import User, get_current_user
from schemas import Product, ProductDetail
from services import ProductService, get_product_service

from .error_messag import PRODUCT_NOT_FOUND

product_router = APIRouter()


@product_router.get("/", response_model=List[Product], status_code=200)
async def get_all_products(
        service: ProductService = Depends(get_product_service)
) -> List[Product]:
    return await service.get_all()


@product_router.get("/active", response_model=List[Product], status_code=200)
async def get_active_product(
        service: ProductService = Depends(get_product_service)
) -> List[Product]:
    return await service.get_all(only_active=True)


@product_router.get("/{product_id}", response_model=ProductDetail, status_code=200)
async def get_product_details(
        product_id: str = Query(None),
        service: ProductService = Depends(get_product_service)
) -> ProductDetail:
    product = await service.get(product_id)
    if not product:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=PRODUCT_NOT_FOUND)

    return product

# TODO :)
# @product_router.post("/", status_code=200)
# async def create_product(
#         user: User = Depends(get_current_user),
#         service: ProductService = Depends(get_product_service)
# ):
#     pass


@product_router.delete("/{product_id}", status_code=200)
async def set_product_inactive(
        product_id: str = Query(None),
        user: User = Depends(get_current_user),
        service: ProductService = Depends(get_product_service)
):
    product = await service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=PRODUCT_NOT_FOUND)
