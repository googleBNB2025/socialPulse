from fastapi import APIRouter, UploadFile, File, HTTPException
from google.cloud import storage
from google.cloud import pubsub_v1
from google.api_core import exceptions
import uuid
import os
import json

router = APIRouter()

BUCKET = os.getenv("GCS_BUCKET")
TOPIC_PATH = os.getenv("PUBSUB_TOPIC")

# Initialize clients outside of the request handler for reuse
storage_client = storage.Client()
publisher = pubsub_v1.PublisherClient()

@router.post("/")
async def upload(file: UploadFile = File(...), metadata: str = ""):
    if not BUCKET or not TOPIC_PATH:
        raise HTTPException(status_code=500, detail="Server configuration error: GCS_BUCKET or PUBSUB_TOPIC not set.")

    try:
        # save to GCS
        blob_name = f"uploads/{uuid.uuid4().hex}_{file.filename}"
        bucket = storage_client.bucket(BUCKET)
        blob = bucket.blob(blob_name)
        contents = await file.read()
        blob.upload_from_string(contents, content_type=file.content_type)
    except exceptions.NotFound:
        raise HTTPException(status_code=404, detail=f"GCS bucket '{BUCKET}' not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not upload file to GCS: {e}")

    try:
        # publish to Pub/Sub for worker
        message_data = {"blob": blob_name, "content_type": file.content_type, "metadata": metadata}
        # Use json.dumps for a robust message format
        message_bytes = json.dumps(message_data).encode("utf-8")
        publisher.publish(TOPIC_PATH, data=message_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not publish to Pub/Sub: {e}")

    return {"status":"uploaded","blob":blob_name}
