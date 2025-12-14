import { BACKEND_URL } from "./config";

export async function fetchTranscript(filename: string) {
  const res = await fetch(
    `${BACKEND_URL}/transcript/${filename}`,
    {
      cache: "no-store",
    }
  );

  if (!res.ok) {
    throw new Error("Failed to fetch transcript");
  }

  return res.json();
}
