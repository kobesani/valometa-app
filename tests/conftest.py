import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from valometa.api.routes import app



@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
