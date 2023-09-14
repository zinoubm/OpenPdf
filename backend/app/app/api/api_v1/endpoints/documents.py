from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse

from typing import Any, List
from uuid import uuid4
import logging
from sqlalchemy.orm import Session

from app.schemas.document import UpsertResponse
from app.parser.parser import get_document_from_file
from app.parser.chunk import chunk_text

from app.openai.base import openai_manager
from app.openai.core import ask, ask_stream
from app.vectorstore.qdrant import qdrant_manager
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post(
    "/upsert",
    response_model=UpsertResponse,
)
async def upsert_file(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    if not file:
        logging.error("There was a problem with file Upload")
        raise HTTPException(status_code=500, detail="No File Recieved")

    # Until openpdf supports more document formats
    if file.content_type != "application/pdf":
        logging.error("OpenPdf only supports PDFs")
        raise HTTPException(
            status_code=415, detail="Openpdf Does Not Support Other Formats Yet!"
        )

    document_text = await get_document_from_file(file)
    chunks = chunk_text(document_text, max_size=2000)

    document_in = schemas.DocumentCreate(title=file.filename)
    document = crud.document.create_with_user(
        db=db, obj_in=document_in, user_id=current_user.id
    )

    ids = [uuid4().hex for chunk in chunks]
    payloads = [
        {
            "user_id": current_user.id,
            "document_id": document.id,
            "chunk": chunk,
        }
        for chunk in chunks
    ]
    embeddings = openai_manager.get_embeddings(chunks)

    try:
        res = qdrant_manager.upsert_points(ids, payloads, embeddings)
        logging.info(f"Vector Store Response: {res}")

    except Exception as e:
        logging.error(e)
        crud.document.remove(db=db, id=document.id)
        qdrant_manager.delete_points(user_id=current_user.id, document_id=document.id)
        raise HTTPException(
            status_code=502, detail="Something Went Wrong With The Vector Store!"
        )

    logging.info(f"Document Uploaded Succesfuly")

    return UpsertResponse(id=document.id)


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
        documents = crud.document.get_multi_by_user(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )

    return documents


@router.post("/query")
async def query(
    query: str,
    document_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> str:
    document = crud.document.get(db=db, id=document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if document.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    query_vector = openai_manager.get_embedding(query)

    points = qdrant_manager.search_point(
        query_vector=query_vector,
        user_id=current_user.id,
        document_id=document_id,
        limit=5,
    )

    context = "\n\n\n".join([point.payload["chunk"] for point in points])

    answer = ask(
        context,
        query,
        openai_manager,
    )

    return {"answer": answer, "context": context}


@router.post("/query-stream")
async def query_stream(
    query: str,
    document_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> str:
    document = crud.document.get(db=db, id=document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if document.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    query_vector = openai_manager.get_embedding(query)

    points = qdrant_manager.search_point(
        query_vector=query_vector,
        user_id=current_user.id,
        document_id=document_id,
        limit=5,
    )

    context = "\n\n\n".join([point.payload["chunk"] for point in points])

    return StreamingResponse(
        ask_stream(
            context,
            query,
            openai_manager,
        ),
        media_type="text/event-stream",
    )


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
        document.user_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    try:
        qdrant_manager.delete_points(user_id=current_user.id, document_id=id)

    except Exception as e:
        raise HTTPException(
            status_code=502, detail="Something Went Wrong With The Vector Store!"
        )

    document = crud.document.remove(db=db, id=id)
    return document
