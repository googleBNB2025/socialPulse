import os
import ast
from google.cloud import pubsub_v1, storage

PROJECT_ID = os.getenv("PROJECT_ID", "socialpulseai-478505")
SUBSCRIPTION = os.getenv("PUBSUB_SUB", "socialpulse-sub")
BUCKET = os.getenv("GCS_BUCKET", "socialpulse-uploads")

storage_client = storage.Client()

def process_file(blob_name):
    bucket = storage_client.bucket(BUCKET)
    blob = bucket.blob(blob_name)
    content = blob.download_as_bytes()
    print(f"🔥 Worker: downloaded {blob_name}, size={len(content)} bytes")

    # 🔥 TODO: AI analysis steps will go here
    print("🔥 Worker: (mock) analysis complete.\n")

def callback(message):
    print("🔥 Worker received:", message.data.decode())
    data = ast.literal_eval(message.data.decode())
    process_file(data["blob"])
    message.ack()

def start_worker():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION)

    print(f"🔥 Worker listening on {subscription_path}")
    subscriber.subscribe(subscription_path, callback=callback)

    import time
    while True:
        time.sleep(60)

if __name__ == "__main__":
    start_worker()
