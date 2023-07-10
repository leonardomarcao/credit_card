# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import logging

import pytest
from webtest import TestApp

from card_vault.app import create_app
from card_vault.extensions import db as _db


@pytest.fixture(scope="function")
def app():
    """Create application for the tests."""
    _app = create_app("card_vault.settings")
    _app.logger.setLevel(logging.CRITICAL)
    with _app.app_context():
        _db.create_all()
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope="function")
def testapp(app):
    """Create Webtest app."""
    test_app = TestApp(app)
    test_app.authorization = (
        "Basic",
        (app.config["BASIC_AUTH_USERNAME"], app.config["BASIC_AUTH_PASSWORD"]),
    )
    return test_app


@pytest.fixture(scope="function")
def db(app):
    """Create database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def payload():
    return {
        "holder": "John Doe",
        "number": "4182-9188-5511-3275",
        "exp_date": "12/2025",
        "cvv": "123",
    }
