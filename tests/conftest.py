import asyncio
from uuid import UUID

import pytest

from store.db.mongo import db_client
from store.schemas.product import ProductIn, ProductUpdate
from store.usecases.product import product_usecase
from tests.factories import product_data, products_data


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mongo_client():
    return db_client.get()


# this fixture is used to clear the collections after each test,
# so the db is not polluted with test data
@pytest.fixture(autouse=True)
async def clear_collections(mongo_client):
    yield
    collections_names = await mongo_client.get_database().list_collection_names()
    for collection_name in collections_names:
        if collection_name.startswith("system"):
            continue

        await mongo_client.get_database()[collection_name].delete_many({})


@pytest.fixture
def product_id() -> UUID:
    return UUID("61b8c22a-015f-4c0c-a3f6-681b39bcbec9")


@pytest.fixture
def product_in(product_id) -> ProductIn:
    return ProductIn(**product_data(), id=product_id)


@pytest.fixture
def product_up(product_id) -> ProductUpdate:
    return ProductUpdate(**product_data(), id=product_id)


@pytest.fixture
async def product_inserted(
    product_in,
):  # fix the broken tests that clear_collections fixture caused
    return await product_usecase.create(body=product_in)


# the next 2 fixtures are used to insert multiple lines to the db,
# and so improve the query test
# it is needed because clear_collections deletes all the data after each test
@pytest.fixture
def products_in() -> list[ProductIn]:
    return [ProductIn(**product) for product in products_data()]


@pytest.fixture
async def products_inserted(products_in):
    return [await product_usecase.create(body=product_in) for product_in in products_in]
