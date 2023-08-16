from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Document])
def read_documents(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve documents.
    """
    if crud.user.is_superuser(current_user):
        documents = crud.document.get_multi(db, skip=skip, limit=limit)
    else:
        documents = crud.document.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return documents


@router.post("/", response_model=schemas.Document)
def create_document(
    *,
    db: Session = Depends(deps.get_db),
    document_in: schemas.DocumentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new document.
    """
    document = crud.document.create_with_owner(
        db=db, obj_in=document_in, owner_id=current_user.id
    )
    return document


@router.put("/{id}", response_model=schemas.Document)
def update_document(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    document_in: schemas.DocumentUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an document.
    """
    document = crud.document.get(db=db, id=id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if not crud.user.is_superuser(current_user) and (
        document.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    document = crud.document.update(db=db, db_obj=document, obj_in=document_in)
    return document


@router.get("/{id}", response_model=schemas.Document)
def read_document(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get document by ID.
    """
    document = crud.document.get(db=db, id=id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if not crud.user.is_superuser(current_user) and (
        document.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return document


@router.delete("/{id}", response_model=schemas.Document)
def delete_document(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an document.
    """
    document = crud.document.get(db=db, id=id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if not crud.user.is_superuser(current_user) and (
        document.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    document = crud.document.remove(db=db, id=id)
    return document
