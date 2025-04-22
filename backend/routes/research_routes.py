from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from models.research import ResearchRequest, ResearchResponse
from services.research_services import perform_research
from services.auth import get_current_user
from typing import Annotated

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/", response_model=ResearchResponse)
def research_topic(
    request: ResearchRequest,
    token: Annotated[str, Depends(oauth2_scheme)]
):
    try:
        # Verify user
        user = get_current_user(token)
        print("User verified")
        print(user)
        # Perform research and store in database
        result = perform_research(request, user["user_id"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))