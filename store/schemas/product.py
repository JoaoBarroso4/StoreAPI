from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional, Annotated

from bson import Decimal128
from pydantic import Field, AfterValidator

from store.schemas.base import BaseSchemaMixin, OutSchema


class ProductBase(BaseSchemaMixin):
    name: str = Field(
        ..., description="Product name", min_length=3, max_length=100
    )  # ... is a required field
    quantity: int = Field(..., description="Product quantity", ge=0)  # ge means >= 0
    price: Decimal = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")


class ProductIn(ProductBase, BaseSchemaMixin):
    ...


class ProductOut(ProductIn, OutSchema):
    ...


def convert_decimal_128(v):
    return Decimal128(str(v))


Decimal_ = Annotated[Decimal, AfterValidator(convert_decimal_128)]


class ProductUpdate(BaseSchemaMixin):
    quantity: Optional[int] = Field(None, description="Product quantity")
    price: Optional[Decimal_] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProductUpdateOut(ProductOut):
    ...
