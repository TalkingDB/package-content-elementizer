from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel


class RequestModel(BaseModel):
    document_file: UploadFile
    metadata: Optional[str] = None
