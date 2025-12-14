export default function JournalPage() {
  return (
    <div className="min-h-screen px-6 py-10 max-w-3xl mx-auto">
      <h1 className="text-3xl font-semibold text-gray-800 mb-2">
        Daily Journal
      </h1>

      <p className="text-gray-500 mb-6">
        Reflect, reset, and reconnect with your creative self ✨
      </p>

      <div className="bg-white/70 backdrop-blur rounded-2xl shadow-md p-6">
        <textarea
          placeholder="What are you feeling today?"
          className="w-full h-40 resize-none bg-transparent outline-none text-gray-700 placeholder-gray-400"
        />

        <div className="flex justify-end mt-4">
          <button className="px-6 py-2 rounded-full bg-black text-white text-sm hover:opacity-90 transition">
            Save entry
          </button>
        </div>
      </div>
    </div>
  );
}
