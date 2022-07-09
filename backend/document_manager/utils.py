from typing import Optional
from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class DocumentId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(oid=value):
            raise ValueError("Invalid object id")
        return ObjectId(value)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class HandInModel(BaseModel):
    id: DocumentId = Field(default_factory=DocumentId, alias="_id")
    title: str = Field(...)
    author: str = Field(...)
    description: str | None = None
    content: str = Field(...)
    tags: list[str] = Field(...)
    publish_date: str | None = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdatedHandInModel(BaseModel):
    title: Optional[str]
    author: Optional[str]
    description: Optional[str]
    content: Optional[str]
    tags: Optional[str]
