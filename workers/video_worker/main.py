import functions_framework
from process_video import process_video as worker_fn

@functions_framework.cloud_event
def process_video(event):
    # CloudEvent payload is inside event.data
    data = event.data if hasattr(event, "data") else event
    return worker_fn(data, None)