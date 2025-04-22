from pydantic import BaseModel
from typing import List, Dict

class ResearchRequest(BaseModel):
    topic: str
    max_results: int = 5

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: List[Dict[str, str]]
    research_id: str