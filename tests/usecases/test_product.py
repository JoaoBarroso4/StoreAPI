from typing import List
from uuid import UUID

import pytest

from store.core.exceptions import NotFoundException
from store.schemas.product import ProductOut, ProductUpdateOut
from store.usecases.product import product_usecase


async def test_usecases_should_return_success(product_in):
    result = await product_usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == product_in.name


async def test_usecases_get_should_return_success(product_inserted):
    result = await product_usecase.get(product_inserted.id)

    assert isinstance(result, ProductOut)
    assert result.name == "iPhone 11 Pro Max"


async def test_usecases_get_should_return_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.get(
            product_id=UUID("27034d0d-71f3-4a03-a479-e93be663dd08")
        )

    assert (
        err.value.message
        == "Product not found with filter: 27034d0d-71f3-4a03-a479-e93be663dd08"
    )


@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_should_return_success(products_inserted):
    result = await product_usecase.query()

    assert isinstance(result, List)
    assert len(result) > 1


async def test_usecases_update_should_return_success(product_inserted, product_up):
    product_up.price = 4000
    result = await product_usecase.update(
        product_id=product_inserted.id, body=product_up
    )

    assert isinstance(result, ProductUpdateOut)


async def test_usecases_delete_should_return_success(product_inserted):
    result = await product_usecase.delete(product_id=product_inserted.id)

    assert result is True


async def test_usecases_delete_should_return_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.delete(
            product_id=UUID("27034d0d-71f3-4a03-a479-e93be663dd08")
        )

    assert (
        err.value.message
        == "Product not found with filter: 27034d0d-71f3-4a03-a479-e93be663dd08"
    )
