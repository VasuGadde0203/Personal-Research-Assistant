from pydantic import BaseModel

# Pydantic Models
class Message(BaseModel):
    role: str
    content: dict | str

class Conversation(BaseModel):
    messages: list[Message]

class ConversationResponse(Conversation):
    id: str