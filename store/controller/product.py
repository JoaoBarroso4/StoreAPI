from typing import List

from fastapi import APIRouter, status, Depends, Body, Path, HTTPException
from pydantic import UUID4

from store.core.exceptions import NotFoundException
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.usecases.product import ProductUseCase

router = APIRouter()


@router.post("/", summary="Create a product", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUseCase = Depends()
) -> ProductOut:
    return await usecase.create(body=body)


@router.get("/{product_id}", summary="Get a product", status_code=status.HTTP_200_OK)
async def get(
    product_id: UUID4 = Path(alias="product_id"), usecase: ProductUseCase = Depends()
) -> ProductOut:
    try:
        return await usecase.get(product_id=product_id)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e.message)
        )


@router.get("/", summary="Query products", status_code=status.HTTP_200_OK)
async def query(usecase: ProductUseCase = Depends()) -> List[ProductOut]:
    return await usecase.query()


@router.patch(
    "/{product_id}", summary="Update a product", status_code=status.HTTP_200_OK
)
async def patch(
    product_id: UUID4 = Path(alias="product_id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUseCase = Depends(),
) -> ProductUpdateOut:
    return await usecase.update(product_id=product_id, body=body)


@router.delete(
    "/{product_id}", summary="Delete a product", status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
    product_id: UUID4 = Path(alias="product_id"), usecase: ProductUseCase = Depends()
) -> None:
    try:
        await usecase.delete(product_id=product_id)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e.message)
        )
