from sqlalchemy.orm import Session

from app import crud
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_document(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    document_in = DocumentCreate(title=title, description=description)
    user = create_random_user(db)
    document = crud.document.create_with_owner(
        db=db, obj_in=document_in, owner_id=user.id
    )
    assert document.title == title
    assert document.description == description
    assert document.owner_id == user.id


def test_get_document(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    document_in = DocumentCreate(title=title, description=description)
    user = create_random_user(db)
    document = crud.document.create_with_owner(
        db=db, obj_in=document_in, owner_id=user.id
    )
    stored_document = crud.document.get(db=db, id=document.id)
    assert stored_document
    assert document.id == stored_document.id
    assert document.title == stored_document.title
    assert document.description == stored_document.description
    assert document.owner_id == stored_document.owner_id


def test_update_document(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    document_in = DocumentCreate(title=title, description=description)
    user = create_random_user(db)
    document = crud.document.create_with_owner(
        db=db, obj_in=document_in, owner_id=user.id
    )
    description2 = random_lower_string()
    document_update = DocumentUpdate(description=description2)
    document2 = crud.document.update(db=db, db_obj=document, obj_in=document_update)
    assert document.id == document2.id
    assert document.title == document2.title
    assert document2.description == description2
    assert document.owner_id == document2.owner_id


def test_delete_document(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    document_in = DocumentCreate(title=title, description=description)
    user = create_random_user(db)
    document = crud.document.create_with_owner(
        db=db, obj_in=document_in, owner_id=user.id
    )
    document2 = crud.document.remove(db=db, id=document.id)
    document3 = crud.document.get(db=db, id=document.id)
    assert document3 is None
    assert document2.id == document.id
    assert document2.title == title
    assert document2.description == description
    assert document2.owner_id == user.id
