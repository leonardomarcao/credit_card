# -*- coding: utf-8 -*-
"""Factories to help in tests."""

from factory.alchemy import SQLAlchemyModelFactory

from card_vault.extensions import db
from card_vault.models import CreditCard


class CreditCardFactory(SQLAlchemyModelFactory):
    class Meta:
        model = CreditCard
        sqlalchemy_session = db.session

    holder = "John Doe"
    number = "4182-9188-5511-3275"
    exp_date = "12/2025"
    cvv = "123"
