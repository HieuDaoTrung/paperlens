"""
Basic CRUD operations
"""
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pymongo import ASCENDING
from pymongo.mongo_client import MongoClient
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_417_EXPECTATION_FAILED
from utils import HandInModel, UpdatedHandInModel
from bson.json_util import dumps
import json
from datetime import date


app = FastAPI()

# client = MongoClient(host="mongo:27017")
client = MongoClient("mongodb+srv://admin:admin@nigelx-test-database.ih7yh.mongodb.net/?retryWrites=true&w=majority")
db = client["paperlens"]


@app.get("/documents", status_code=status.HTTP_200_OK)
async def get_documents():
    """Query all registered documents from database"""
    collections = db.list_collection_names()
    return {
        "document_types": collections
    }


@app.post("/documents/{collection_name}", response_model=HandInModel)
async def insert_document(collection_name: str, document: HandInModel):
    """Insert a new document to database"""
    # Check publish_date, if not explicitly stated, then create a new one
    if not document.publish_date:
        document.publish_date = date.today().strftime("%m/%d/%Y")

    # To insert Pydantic Models to MongoDB, it must first be converted to BSON or JSON. See more https://fastapi.tiangolo.com/tutorial/encoder/
    document = jsonable_encoder(document)
    insertion = db[collection_name].insert_one(document)  # type:ignore

    inserted_doc = db[collection_name].find_one(insertion.inserted_id)

    if insertion.acknowledged:
        return JSONResponse(status_code=HTTP_201_CREATED, content=inserted_doc)
    else:
        return JSONResponse(status_code=HTTP_417_EXPECTATION_FAILED, content="Cannot write to database")


@app.get("/documents/{collection_name}", response_model=list[HandInModel])
async def get_collection_docs(collection_name: str):
    """Return all documents in the collection"""
    collection = db[collection_name]
    docs_as_string = dumps(collection.find().sort("title", ASCENDING))  # A serializable string
    docs_as_json = json.loads(docs_as_string)
    return docs_as_json


@app.get("/documents/{collection_name}/{document_id}", response_model=HandInModel)
async def get_single_doc(collection_name: str, document_id: str):
    """Return information about a single document"""
    collection = db[collection_name]
    return collection.find_one(document_id)


@app.put("/documents/{collection_name}/{document_id}")
async def update_document(collection_name: str, document_id: str, updates: UpdatedHandInModel):
    """Update a single document"""
    collection = db[collection_name]
    updates = {k: v for k, v in updates.dict.items() if v is not None}  # type:ignore
    result = collection.update_one({"_id": document_id}, {"$set": updates})
    if result.acknowledged:
        return collection.find_one(document_id, projection={"_id": 0})
    else:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content=f"Document id {document_id} not found")


@app.delete("/documents/{collection_name}/{document_id}", response_description="Delete a document")
async def delete_document(collection_name: str, document_id: str):
    """Delete a single document"""
    collection = db[collection_name]
    deletion = collection.delete_one({"_id": document_id})

    if deletion.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)  # Code 204 cannot use JSONResponse. See more https://github.com/tiangolo/fastapi/issues/2253
    else:
        raise HTTPException(status_code=404, detail=f"Document not found")
