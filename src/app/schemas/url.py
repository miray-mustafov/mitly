from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional

"""
This file defines how the api input and output should look for the URL model.
It uses pydantic.BaseModel for data validation and serialization.
Serialization: Python obj -> JSON (sending response to the client)
Deserialization: JSON -> Python obj (receiving request from the client)
"""


class URLBase(BaseModel):
    original_url: HttpUrl


class URLCreate(URLBase):  # Defining the input
    # Allows user to specify custom expiration, default to None (CRUD handles default)
    expiration_days: Optional[int] = Field(None, ge=1, le=365)


class URLRead(BaseModel):  # Defining the output
    short_url_id: str
    original_url: str
    created_at: datetime
    expires_at: datetime
    is_expired: bool

    class Config:
        # This tells Pydantic to read data even if it's an SQLAlchemy model object instead of a dictionary.
        from_attributes = True
