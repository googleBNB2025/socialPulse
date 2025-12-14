export default function AppShell({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(180deg, #fdfbff 0%, #f6f3ff 100%)",
        padding: "32px",
      }}
    >
      <div
        style={{
          maxWidth: "720px",
          margin: "0 auto",
        }}
      >
        {children}
      </div>
    </div>
  );
}
