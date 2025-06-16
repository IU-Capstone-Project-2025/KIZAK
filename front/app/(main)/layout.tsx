import { Sidebar } from "@/shared/components/sidebar/sidebar";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div
      className={`h-screen bg-bg-main flex items-center gap-x-4 p-5 antialiased`}
    >
      <Sidebar />
      <div className="h-full w-full">{children}</div>
    </div>
  );
}
