import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: "Ari's Local Helper",
  description: 'Terse robot assistant for local tasks',
  manifest: '/manifest.json',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
