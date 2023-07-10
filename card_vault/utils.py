# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
import binascii
from base64 import b64decode, b64encode
from typing import Dict, List, Union

from Crypto import Random
from Crypto.Cipher import AES
from flask_restx import fields
from pydantic import BaseModel


def pydantic_to_flask_restx(
        pydantic_model: BaseModel,
) -> Dict[str, Union[fields.Raw, fields.Nested]]:
    TYPE_MAPPER = {
        str: fields.String,
        int: fields.Integer,
        float: fields.Float,
        bool: fields.Boolean,
        dict: fields.Nested,
        list: fields.List,
    }
    flask_model = {}

    for name, field in pydantic_model.__annotations__.items():
        field_type = TYPE_MAPPER.get(field, fields.Raw)

        if field_type is fields.Nested:
            if hasattr(field, "__origin__") and issubclass(field.__origin__, List):
                nested_model = pydantic_to_flask_restx(field.__args__[0])
                flask_model[name] = fields.List(fields.Nested(nested_model))
            else:
                nested_model = pydantic_to_flask_restx(field)
                flask_model[name] = fields.Nested(nested_model)
        else:
            flask_model[name] = field_type()

    return flask_model


class AESCipher:
    def __init__(self, key=None):
        self.bs = AES.block_size
        if key is not None:
            self.key = b64decode(key)
        else:
            self.key = Random.new().read(AES.key_size[-1])

    def encrypt(self, raw):
        raw = self._pad(raw).encode()
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + cipher.encrypt(raw)).decode("utf-8")

    def decrypt(self, enc):
        try:
            enc = b64decode(enc)
            iv = enc[: AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode("utf-8")
        except binascii.Error:
            print("Error: Incorrect padding")
            return None

    def get_key(self):
        return b64encode(self.key).decode("utf-8")

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[: -ord(s[len(s) - 1:])]
