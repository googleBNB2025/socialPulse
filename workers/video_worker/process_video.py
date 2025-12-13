import os
import tempfile
import subprocess
from google.cloud import storage, speech_v1p1beta1, videointelligence_v1, language_v1, firestore
import json

storage_client = storage.Client()
speech_client = speech_v1p1beta1.SpeechClient()
video_client = videointelligence_v1.VideoIntelligenceServiceClient()
nlp_client = language_v1.LanguageServiceClient()
db = firestore.Client(database="socialpulseai")

def process_video(event, context):
    bucket_name = event.get("bucket") or event["bucket"]
    file_name = event.get("name") or event.get("object") or event["name"]

    bucket = storage_client.bucket(bucket_name)
    print(f"🎥 Processing video: {file_name}")

    # DOWNLOAD
    tmp_video = tempfile.mkstemp(suffix=".mp4")[1]
    bucket.blob(file_name).download_to_filename(tmp_video)

    # EXTRACT AUDIO
    tmp_audio = tempfile.mkstemp(suffix=".wav")[1]
    print("🎧 Running ffmpeg...")

    ffmpeg = subprocess.run([
        "ffmpeg", "-i", tmp_video, "-vn",
        "-ac", "1", "-ar", "16000", "-y", tmp_audio
    ], capture_output=True)

    if ffmpeg.returncode != 0:
        print("⚠️ No audio detected. Saving empty transcript.")
        save_empty_transcript(file_name)
        return

    # STT
    with open(tmp_audio, "rb") as f:
        audio_content = f.read()

    audio = speech_v1p1beta1.RecognitionAudio(content=audio_content)
    config = speech_v1p1beta1.RecognitionConfig(
        encoding=speech_v1p1beta1.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_word_time_offsets=True,
        enable_speaker_diarization=True,
        diarization_speaker_count=2
    )

    stt_response = speech_client.recognize(config=config, audio=audio)
    result = stt_response.results[-1]

    transcript = ""
    speakers = []

    for word_info in result.alternatives[0].words:
        transcript += word_info.word + " "
        speakers.append({
            "word": word_info.word,
            "speaker": word_info.speaker_tag
        })

    # NLP
    document = language_v1.Document(
        content=transcript,
        type_=language_v1.Document.Type.PLAIN_TEXT
    )

    sentiment = nlp_client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    entities = nlp_client.analyze_entities(
        request={"document": document}
    ).entities

    topics = [e.name for e in entities][:10]

    # VIDEO LABELS
    with open(tmp_video, "rb") as f:
        video_data = f.read()

    features = [videointelligence_v1.Feature.LABEL_DETECTION]

    print("⏳ Waiting for video labels...")
    operation = video_client.annotate_video(
        request={
            "features": features,
            "input_content": video_data
        }
    )

    vi_response = operation.result()

    labels = []
    for annotation in vi_response.annotation_results[0].segment_label_annotations:
        labels.append(annotation.entity.description)

    # SAVE
    db.collection("transcripts").document(file_name).set({
        "file": file_name,
        "transcript": transcript,
        "topics": topics,
        "sentiment": {
            "score": sentiment.score,
            "magnitude": sentiment.magnitude
        },
        "visual_labels": labels,
        "speakers": speakers,
        "status": "done"
    })

    print("✅ DONE")


def save_empty_transcript(file_name):
    db.collection("transcripts").document(file_name).set({
        "file": file_name,
        "transcript": "",
        "topics": [],
        "sentiment": {},
        "visual_labels": [],
        "speakers": [],
        "status": "no-audio"
    })
    print("🟡 Stored empty transcript.")