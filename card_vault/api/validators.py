from datetime import datetime

from creditcard import CreditCard as CreditCardValidator
from pydantic import BaseModel, Field, field_validator


class CreditCardModel(BaseModel):
    id: int = Field(None, ge=1)
    holder: str = Field(..., min_length=2)
    number: str
    exp_date: str
    cvv: str = Field(None, min_length=3, max_length=4)
    brand: str = Field(None, min_length=2)

    @field_validator("number")
    def validate_number(cls, v):
        cc = CreditCardValidator(v)
        if not cc.is_valid():
            raise ValueError("Invalid credit card number")
        return v

    @field_validator("exp_date")
    def validate_exp_date(cls, v):
        try:
            exp_dt = datetime.strptime(v, "%m/%Y")
        except ValueError:
            raise ValueError("Invalid expiration date")
        if exp_dt < datetime.now():
            raise ValueError("Expired credit card")
        return v
