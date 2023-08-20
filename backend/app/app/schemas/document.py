from typing import Optional, List

from pydantic import BaseModel


# Shared properties
class DocumentBase(BaseModel):
    title: Optional[str] = None
    # description: Optional[str] = None


# Properties to receive on item creation
class DocumentCreate(DocumentBase):
    pass


# Properties to receive on item update
class DocumentUpdate(DocumentBase):
    pass


# Properties shared by models stored in DB
class DocumentInDBBase(DocumentBase):
    id: int
    title: str
    user_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Document(DocumentInDBBase):
    pass


# Properties properties stored in DB
class DocumentInDB(DocumentInDBBase):
    pass


class UpsertRequest(BaseModel):
    documents: List[Document]


class UpsertResponse(BaseModel):
    id: str
