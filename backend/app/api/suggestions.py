from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def get_suggestions(payload: dict):
    return {"status": "ok", "suggestions": []}
