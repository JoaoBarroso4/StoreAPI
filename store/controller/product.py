from fastapi import APIRouter, status, Depends, Body

from store.schemas.product import ProductIn, ProductOut
from store.usecases.product import ProductUseCase

router = APIRouter()


@router.post("/", summary="Create a product", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUseCase = Depends()
) -> ProductOut:
    return await usecase.create(body=body)
