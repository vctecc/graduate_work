from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas.subscription import SubscriptionDetails, SubscriptionPreview
from app.services.subscription import (SubscriptionService,
                                       get_subscription_service)

from .error_messag import SUBSCRIPTION_NOT_FOUND

service_router = APIRouter()


@service_router.get("/subscription/{subscription_id}",
                    response_model=SubscriptionDetails,
                    status_code=200)
async def get_subscription_details(
        subscription_id: str,
        service: SubscriptionService = Depends(get_subscription_service)
) -> SubscriptionDetails:

    subscription = await service.get(subscription_id)
    if not subscription:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=SUBSCRIPTION_NOT_FOUND)

    return subscription


@service_router.post("/subscription/{subscription_id}",
                     response_model=SubscriptionPreview,
                     status_code=200)
async def activate_subscription(
        subscription_id: str,
        period: Optional[int] = Query(None,
                                      description="subscription duration in days"),
        service: SubscriptionService = Depends(get_subscription_service)
) -> SubscriptionPreview:

    subscription = await service.activate(subscription_id, period)
    if not subscription:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=SUBSCRIPTION_NOT_FOUND)

    return subscription


@service_router.delete("/subscription/{subscription_id}",
                       response_model=SubscriptionPreview,
                       status_code=200)
async def deactivate_subscription(
        subscription_id: str,
        service: SubscriptionService = Depends(get_subscription_service)
) -> SubscriptionPreview:

    subscription = await service.deactivate(subscription_id)
    if not subscription:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=SUBSCRIPTION_NOT_FOUND)

    return subscription
