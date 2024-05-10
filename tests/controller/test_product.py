from typing import List

import pytest

from tests.factories import product_data
from fastapi import status


async def test_controller_create_should_return_success(client, products_url):
    response = await client.post(products_url, json=product_data())

    content = response.json()

    del content["created_at"]
    del content["updated_at"]
    del content["id"]

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {
        "name": "iPhone 11 Pro Max",
        "quantity": 10,
        "price": "3.000",
        "status": True,
    }


async def test_controller_get_should_return_success(
    client, products_url, product_inserted
):
    response = await client.get(f"{products_url}{product_inserted.id}")

    content = response.json()

    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "iPhone 11 Pro Max",
        "quantity": 10,
        "price": "3.000",
        "status": True,
    }


async def test_controller_get_should_return_not_found(client, products_url):
    response = await client.get(f"{products_url}64d5d30b-c40a-4a2a-b72e-15f548aacd57")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 64d5d30b-c40a-4a2a-b72e-15f548aacd57"
    }


@pytest.mark.usefixtures("products_inserted")
async def test_controller_query_should_return_success(client, products_url):
    response = await client.get(products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1


async def test_controller_patch_should_return_success(
    client, products_url, product_inserted
):
    updated_values = {
        "quantity": 20,
        "price": "3.100",
    }
    response = await client.patch(
        f"{products_url}{product_inserted.id}", json=updated_values
    )

    content = response.json()

    del content["created_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content["updated_at"] != product_inserted.updated_at

    del content["updated_at"]

    assert content == {
        "id": str(product_inserted.id),
        "name": "iPhone 11 Pro Max",
        "quantity": updated_values["quantity"],
        "price": updated_values["price"],
        "status": True,
    }


async def test_controller_patch_should_return_not_found(client, products_url):
    response = await client.patch(
        f"{products_url}64d5d30b-c40a-4a2a-b72e-15f548aacd57", json={"quantity": 20}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 64d5d30b-c40a-4a2a-b72e-15f548aacd57"
    }


async def test_controller_delete_should_return_no_content(
    client, products_url, product_inserted
):
    response = await client.delete(f"{products_url}{product_inserted.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_controller_delete_should_return_not_found(client, products_url):
    response = await client.delete(
        f"{products_url}64d5d30b-c40a-4a2a-b72e-15f548aacd57"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 64d5d30b-c40a-4a2a-b72e-15f548aacd57"
    }
