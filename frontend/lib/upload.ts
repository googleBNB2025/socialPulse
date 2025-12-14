import { BACKEND_URL } from "./config";

export async function getUploadUrl(filename: string) {
  const res = await fetch(
    `${BACKEND_URL}/upload-url?filename=${encodeURIComponent(filename)}`
  );

  if (!res.ok) {
    throw new Error("Failed to get upload URL");
  }

  return res.json() as Promise<{
    file_id: string;
    filename: string;
    upload_url: string;
  }>;
}

export async function uploadToSignedUrl(
  uploadUrl: string,
  file: File
) {
  const res = await fetch(uploadUrl, {
    method: "PUT",
    headers: {
      "Content-Type": file.type || "video/mp4",
    },
    body: file,
  });

  if (!res.ok) {
    throw new Error("Failed to upload file");
  }
}
