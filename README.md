# SocialPulseAI

SocialPulseAI is a creator-focused productivity and self-reflection platform that helps users upload videos, extract insights, and maintain a personal journal — combining content intelligence with self-care.

---

## ✨ Current Status (MVP – In Progress)

This repository currently contains the **foundational MVP setup**, including:

### ✅ Backend (Cloud Run)
- FastAPI backend deployed on Google Cloud Run
- Signed URL–based video upload to Google Cloud Storage
- Pub/Sub event publishing on upload
- Worker service processes videos and generates transcripts
- Transcripts stored and fetched from Firestore
- Health and transcript status endpoints available

### ✅ Frontend (Next.js + Tailwind)
- Next.js App Router setup
- Upload UI connected to backend signed URL flow
- Journal & upload pages wired
- Backend integration tested end-to-end
- Functional video upload and transcript retrieval

> UI styling is intentionally minimal at this stage.  
> Aesthetic, calming, and creator-friendly design will be added next.

---

## 🧱 Tech Stack

**Frontend**
- Next.js (App Router)
- TypeScript
- Tailwind CSS

**Backend**
- FastAPI
- Google Cloud Run
- Google Cloud Storage
- Pub/Sub
- Firestore

---

## 🔁 High-Level Flow

1. User uploads a video from the frontend
2. Backend generates a signed upload URL
3. Video is uploaded directly to GCS
4. Pub/Sub event triggers worker
5. Worker processes video and generates transcript
6. Transcript is stored in Firestore
7. Frontend polls transcript endpoint and displays results

---

## 🚧 What’s Coming Next

- Aesthetic & calming UI (soft colors, journaling vibe)
- Creator productivity dashboard
- Enhanced journal experience
- Error handling & UX polish
- Authentication & user sessions

---

## 🧠 Vision

SocialPulseAI aims to blend **creator productivity**, **content intelligence**, and **self-care journaling** into one calm, intentional experience.

---

## 📝 Notes

This project is under active development.  
The current branch represents a **working integration milestone**, not final UI/UX.


