from fastapi import FastAPI
from google.cloud import storage, pubsub_v1, firestore
from google.oauth2 import service_account
from fastapi.middleware.cors import CORSMiddleware
import uuid
import datetime
import json
import os

app = FastAPI()

BUCKET = "socialpulseai-assets-1"
TOPIC = "video-events-1"

# ------------------------------
# LOAD SERVICE ACCOUNT FROM SECRET
# ------------------------------
sa_key_json = os.environ["SIGNER_SA_KEY"]
sa_info = json.loads(sa_key_json)

credentials = service_account.Credentials.from_service_account_info(sa_info)
PROJECT_ID = sa_info["project_id"]

# ------------------------------
# INIT CLIENTS WITH PRIVATE KEY
# ------------------------------
storage_client = storage.Client(credentials=credentials, project=PROJECT_ID)
publisher = pubsub_v1.PublisherClient(credentials=credentials)
db = firestore.Client(
    credentials=credentials,
    project=PROJECT_ID,
    database="socialpulseai"
)

# ------------------------------
# CORS
# ------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        "http://localhost:3000",
        "https://3000-cs-210366940169-default.cs-asia-southeast1-seal.cloudshell.dev",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# SIGNED URL ENDPOINT
# ----------------------------------------------------
@app.get("/upload-url")
def get_upload_url(filename: str):
    file_id = str(uuid.uuid4())
    final_name = f"{file_id}-{filename}"

    bucket = storage_client.bucket(BUCKET)
    blob = bucket.blob(final_name)

    # Signed URL (V4)
    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(hours=1),
        method="PUT",
        content_type="video/mp4",
    )

    # Publish message to Pub/Sub
    message = json.dumps({
        "file": final_name,
        "file_id": file_id
    }).encode("utf-8")

    topic_path = publisher.topic_path(PROJECT_ID, TOPIC)
    publisher.publish(topic_path, message)

    return {
        "file_id": file_id,
        "filename": final_name,
        "upload_url": url
    }


# ----------------------------------------------------
# TRANSCRIPT ENDPOINT
# ----------------------------------------------------
@app.get("/transcript/{file}")
def get_transcript(file: str):
    doc = db.collection("transcripts").document(file).get()
    if not doc.exists:
        return {"status": "processing"}
    return doc.to_dict()

# ----------------------------------------------------
# HEALTH CHECK
# ----------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}