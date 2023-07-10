# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
import os
from pathlib import Path

from environs import Env

env = Env()
root_dir = Path(__file__).parent.parent
base_dir = root_dir / "card_vault"
env.read_env()

ENV = env.str("FLASK_ENV", default="development")
DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(root_dir, "data.sqlite")
BASIC_AUTH_USERNAME = env.str("BASIC_AUTH_USERNAME")
BASIC_AUTH_PASSWORD = env.str("BASIC_AUTH_PASSWORD")
SQLALCHEMY_TRACK_MODIFICATIONS = False
AUTHORIZATIONS = {
    "basicAuth": {"type": "basic", "in": "header", "name": "Authorization"}
}
