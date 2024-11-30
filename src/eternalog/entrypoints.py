from fastapi import FastAPI

from eternalog.api import create_api


def get_application() -> FastAPI:
    return create_api()
