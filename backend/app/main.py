# backend/app/main.py
print("🔥 DEBUG: main.py LOADED")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
print("🔥 DEBUG: imported FastAPI")

from api.uploads import router as upload_router
print("🔥 DEBUG: imported uploads")

from api.suggestions import router as suggestions_router
print("🔥 DEBUG: imported suggestions")

app = FastAPI(title="SocialPulseAI")
print("🔥 DEBUG: app created")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/upload")
app.include_router(suggestions_router, prefix="/suggestions")
