"""API Token schemas."""

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
