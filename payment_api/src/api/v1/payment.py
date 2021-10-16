from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter()


@router.get("/{film_id}",
            response_model=Film,
            description="Подробная информация о фильме с указанным ID",
            )
async def film_details(film_id: str = Query(None, description="Идентификатор"),
                       film_service: FilmService = Depends(get_film_service)
                       ) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return film
