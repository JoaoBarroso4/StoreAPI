from tests.factories import product_data
from fastapi import status


async def test_usecases_create_should_return_success(client, products_url):
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
