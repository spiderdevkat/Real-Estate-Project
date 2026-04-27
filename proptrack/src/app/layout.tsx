import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'PropTrack India — Real Estate Intelligence',
  description: 'Live property price tracking across Gurugram, Delhi & Bangalore',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
