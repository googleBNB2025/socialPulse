export default function Header() {
  return (
    <header className="w-full px-6 py-4 border-b border-neutral-200 bg-white/70 backdrop-blur-md">
      <div className="max-w-4xl mx-auto flex items-center justify-between">
        <h1 className="text-lg font-semibold text-neutral-800">
          🌸 Social Pulse
        </h1>

        <nav className="flex gap-4 text-sm text-neutral-600">
          <a href="/upload" className="hover:text-neutral-900">
            Upload
          </a>
          <a href="/journal" className="hover:text-neutral-900">
            Journal
          </a>
        </nav>
      </div>
    </header>
  );
}
