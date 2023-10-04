from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string
from app.tests.parser.data import dummy_pdf


def test_upload(client: TestClient, normal_user_token_headers: Dict[str, str]) -> None:
    pdf_path = dummy_pdf(
        random_lower_string(), temp_file_path="/tmp/temp_file_test.pdf"
    )
    files = {"file": open(pdf_path, "rb")}

    r = client.post(
        f"{settings.API_V1_STR}/documents/upsert",
        headers=normal_user_token_headers,
        files=files,
    )

    assert r.status_code == 200
