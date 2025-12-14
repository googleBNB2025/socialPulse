"use client";

import { useState } from "react";
import { getUploadUrl, uploadToSignedUrl } from "@/lib/upload";
import { fetchTranscript } from "@/lib/transcript";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState("");
  const [transcript, setTranscript] = useState<any>(null);

  async function handleUpload() {
    if (!file) return;

    try {
      setStatus("Preparing upload...");

      const { upload_url, filename } = await getUploadUrl(file.name);

      setStatus("Uploading video...");
      await uploadToSignedUrl(upload_url, file);

      setStatus("Processing video...");

      // poll transcript
      let attempts = 0;
      const interval = setInterval(async () => {
        attempts++;

        const result = await fetchTranscript(filename);

        if (result.status !== "processing") {
          setTranscript(result);
          setStatus("Done");
          clearInterval(interval);
        }

        if (attempts > 20) {
          setStatus("Still processing...");
          clearInterval(interval);
        }
      }, 3000);
    } catch (err: any) {
      console.error(err);
      setStatus("Error occurred");
    }
  }

  return (
    <div className="p-6 space-y-4">
      <input
        type="file"
        accept="video/*"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <button
        onClick={handleUpload}
        className="px-4 py-2 rounded bg-black text-white"
      >
        Upload
      </button>

      <p>{status}</p>

      {transcript && (
        <pre className="bg-gray-100 p-4 rounded text-sm">
          {JSON.stringify(transcript, null, 2)}
        </pre>
      )}
    </div>
  );
}