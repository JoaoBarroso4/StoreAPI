import pytest
from pydantic import ValidationError

from store.schemas.product import ProductIn
from tests.factories import product_data


def test_schemas_validated():
    data = product_data()
    product = ProductIn.model_validate(data)  # or ProductIn(**data)

    assert product.name == "iPhone 11 Pro Max"


def test_schemas_return_raise():
    data = {"name": "iPhone 11 Pro Max", "quantity": 10, "price": 3000}

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert err.value.errors()[0] == {
        "type": "missing",
        "loc": ("status",),
        "msg": "Field required",
        "input": {"name": "iPhone 11 Pro Max", "quantity": 10, "price": 3000},
        "url": "https://errors.pydantic.dev/2.7/v/missing",
    }
