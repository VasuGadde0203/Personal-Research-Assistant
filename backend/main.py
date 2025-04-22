from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.research_routes import router as research_router
from routes.conversation_routes import convesation_router
import asyncio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Personal Research Assistant API")


# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(research_router, prefix="/research", tags=["research"])
app.include_router(convesation_router, prefix="/chats", tags=["chats"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)