from pydantic import BaseModel, HttpUrl, Field, ConfigDict
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
    expiry_days: Optional[int] = Field(None, ge=1, le=365)


class URLRead(BaseModel):  # Defining the output
    """
    why model_config = ConfigDict(from_attributes=True)
    usually pydantic models expect dictionary, but with from_attributes=True,
    we tell pydantic to use the objs attributes directly,
    and then we can use URLRead.model_validate(url_obj)
    instead of URLRead(
                    param_1: url_obj.param_1,
                    param_2: url_obj.param_2,
                    ...)
    """
    model_config = ConfigDict(from_attributes=True)

    short_url_id: str
    original_url: str
    created_at: datetime
    expires_at: datetime
    is_expired: bool
