from typing import List
from uuid import UUID

import pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from store.core.exceptions import NotFoundException
from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut


class ProductUseCase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        await self.collection.insert_one(product_model.model_dump())

        return ProductOut(**product_model.model_dump())

    async def get(self, product_id: UUID) -> ProductOut:
        product = await self.collection.find_one({"id": product_id})

        if not product:
            raise NotFoundException(msg=f"Product not found with filter: {product_id}")

        return ProductOut(**product)

    async def query(self) -> List[ProductOut]:
        return [ProductOut(**product) async for product in self.collection.find()]

    async def update(self, product_id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        product = await self.collection.find_one_and_update(
            filter={"id": product_id},
            update={"$set": body.model_dump(exclude_none=True)},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        return ProductUpdateOut(**product)

    async def delete(self, product_id: UUID) -> bool:
        product = await self.collection.find_one({"id": product_id})

        if not product:
            raise NotFoundException(msg=f"Product not found with filter: {product_id}")

        result = await self.collection.delete_one({"id": product_id})

        return result.deleted_count > 0


product_usecase = ProductUseCase()
