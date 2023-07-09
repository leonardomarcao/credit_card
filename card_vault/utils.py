# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from functools import wraps
from typing import Dict, List, Union

from flask import jsonify
from flask_restx import fields
from pydantic import BaseModel, ValidationError


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


def marshal_with(model, code=200):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
                return model.dump(result), code
            except ValidationError as e:
                return jsonify({"message": str(e)}), 400

        return wrapper

    return decorator
