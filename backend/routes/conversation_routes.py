
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from models.research import ResearchRequest, ResearchResponse
from services.research_services import perform_research
from services.auth import get_current_user
from typing import Annotated
from models.conversations import *
from databases.mongodb import *
from bson import ObjectId

convesation_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# New Conversation Endpoints
@convesation_router.post("/store_conversations")
def create_or_update_conversation(
    conversation: Conversation, token: Annotated[str, Depends(oauth2_scheme)]
) -> dict:
    user = get_current_user(token)
    user_id = user["user_id"]
    conversation_dict = conversation.dict()
    conversation_dict["user_id"] = user_id
    existing = conversations_collection.find_one({"user_id": user_id})
    if existing:
        conversations_collection.update_one(
            {"_id": existing["_id"]}, {"$set": {"messages": conversation_dict["messages"]}}
        )
        conversation_dict["id"] = str(existing["_id"])
    else:
        result = conversations_collection.insert_one(conversation_dict)
        conversation_dict["id"] = str(result.inserted_id)
    return {"message": "Conversations stored succesfully"}

@convesation_router.get("/fetch_conversations", response_model=list[ConversationResponse])
def get_conversations(token: Annotated[str, Depends(oauth2_scheme)]):
    user = get_current_user(token)
    user_id = user["user_id"]
    conversations = conversations_collection.find({"user_id": user_id})
    return [
        {
            "id": str(conv["_id"]),
            "messages": conv["messages"],
        }
        for conv in conversations
    ]

@convesation_router.delete("/delete_conversations/{id}")
def delete_conversation(id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    user = get_current_user(token)
    user_id = user["user_id"]
    result = conversations_collection.delete_one({"_id": ObjectId(id), "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"message": "Conversation deleted"}