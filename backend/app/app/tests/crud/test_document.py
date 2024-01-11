from sqlalchemy.orm import Session

from app import crud
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_document(db: Session) -> None:
    title = random_lower_string()
    document_in = DocumentCreate(
        title=title,
    )
    user = create_random_user(db)
    document = crud.document.create_with_user(
        db=db, obj_in=document_in, user_id=user.id
    )
    assert document.title == title
    assert document.user_id == user.id


def test_get_document(db: Session) -> None:
    title = random_lower_string()
    document_in = DocumentCreate(
        title=title,
    )
    user = create_random_user(db)
    document = crud.document.create_with_user(
        db=db, obj_in=document_in, user_id=user.id
    )
    stored_document = crud.document.get(db=db, id=document.id)
    assert stored_document
    assert document.id == stored_document.id
    assert document.title == stored_document.title
    assert document.user_id == stored_document.user_id


def test_delete_document(db: Session) -> None:
    title = random_lower_string()
    document_in = DocumentCreate(
        title=title,
    )
    user = create_random_user(db)
    document = crud.document.create_with_user(
        db=db, obj_in=document_in, user_id=user.id
    )
    document2 = crud.document.remove(db=db, id=document.id)
    document3 = crud.document.get(db=db, id=document.id)
    assert document3 is None
    assert document2.id == document.id
    assert document2.title == title
    assert document2.user_id == user.id