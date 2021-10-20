from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.subscription import SubscriptionDetails, SubscriptionPreview
from app.services.user import UserService, get_user_service
from core import User, get_current_user

from .error_messag import SUBSCRIPTION_NOT_FOUND

user_router = APIRouter()


@user_router.get("/subscription",
                 response_model=List[SubscriptionPreview],
                 status_code=200)
async def get_user_subscriptions(
        user: User = Depends(get_current_user),
        service: UserService = Depends(get_user_service)
) -> List[SubscriptionPreview]:

    subscriptions = await service.get_all_user_subscriptions(user.id)
    if not subscriptions:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=SUBSCRIPTION_NOT_FOUND)

    return subscriptions


@user_router.get("/subscription/{subscription_id}",
                 response_model=SubscriptionDetails,
                 status_code=200)
async def get_subscription_details(
        subscription_id: UUID,
        user: User = Depends(get_current_user),
        service: UserService = Depends(get_user_service)
) -> SubscriptionPreview:

    subscription = await service.get_user_subscription(user.id, subscription_id)
    if not subscription:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=SUBSCRIPTION_NOT_FOUND)

    return subscription


@user_router.delete("/subscription/{subscription_id}",
                    response_model=SubscriptionPreview,
                    status_code=200)
async def cancel_subscription(
        subscription_id: UUID,
        user: User = Depends(get_current_user),
        service: UserService = Depends(get_user_service)
) -> SubscriptionPreview:

    subscription = await service.cancel(user.id, subscription_id)
    if not subscription:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=SUBSCRIPTION_NOT_FOUND)

    return subscription


@user_router.post("/subscription/{subscription_id}",
                  response_model=SubscriptionPreview,
                  status_code=200)
async def refund_subscription(
        subscription_id: UUID,
        user: User = Depends(get_current_user),
        service: UserService = Depends(get_user_service)
) -> SubscriptionPreview:

    subscription = await service.refund(user.id, subscription_id)
    if not subscription:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=SUBSCRIPTION_NOT_FOUND)

    return subscription
