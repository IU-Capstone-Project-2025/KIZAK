import type { Metadata } from "next";
import { JetBrains_Mono } from "next/font/google";
import "./globals.css";

const jetBrains_Mono = JetBrains_Mono({});

export const metadata: Metadata = {
  title: "KIZAK",
  description: "Your Personal Map to the IT World — Together with KIZAK",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${jetBrains_Mono.className} bg-bg-main antialiased`}>
        {children}
      </body>
    </html>
  );
}
