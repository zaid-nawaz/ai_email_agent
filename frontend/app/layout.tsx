import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Email Agent",
  description:
    "AI-powered personalized email outreach",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
