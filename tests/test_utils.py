from flask_restx import fields
from pydantic import BaseModel, Field

from card_vault.utils import AESCipher, pydantic_to_flask_restx


# Pydantic model for testing purposes
class TestModel(BaseModel):
    field1: str = Field(...)
    field2: int = Field(...)
    field3: bool = Field(...)


def test_pydantic_to_flask_restx():
    """Test if pydantic_to_flask_restx() returns a dict with the correct types"""
    result = pydantic_to_flask_restx(TestModel)
    assert isinstance(result["field1"], fields.String)
    assert isinstance(result["field2"], fields.Integer)
    assert isinstance(result["field3"], fields.Boolean)


def test_AESCipher():
    """Test if AESCipher() encrypts and decrypts correctly"""
    cipher = AESCipher()
    text = "test text"
    encrypted = cipher.encrypt(text)
    decrypted = cipher.decrypt(encrypted)
    assert decrypted == text
