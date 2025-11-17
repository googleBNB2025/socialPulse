from fastapi import FastAPI, Request
import base64

app = FastAPI()

# Health check endpoint (required by Cloud Run)
@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/")
async def pubsub_handler(request: Request):
    envelope = await request.json()
    print("🔥 Worker received Pub/Sub push event:", envelope)

    if "message" not in envelope:
        return {"status": "no-message"}

    msg = envelope["message"]
    data = msg.get("data")

    if data:
        decoded = base64.b64decode(data).decode("utf-8")
        print("🔥 Decoded message:", decoded)
    else:
        decoded = None

    return {"status": "processed", "decoded": decoded}
