import './globals.css';
import Sidebar from '@/components/layout/Sidebar';
import { Inter, Space_Grotesk } from 'next/font/google';
import { ReactNode } from 'react';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });
const spaceGrotesk = Space_Grotesk({ subsets: ['latin'], variable: '--font-space-grotesk' });

export const metadata = {
  title: 'Anna Setu',
  description: 'AI-Powered Institutional Food Waste Reduction',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${spaceGrotesk.variable} font-sans flex w-full min-h-screen bg-ink-base text-content-primary antialiased`}>
        <Sidebar />
        <main className="ml-64 flex-1 w-full min-h-screen bg-ink-base">
          {children}
        </main>
      </body>
    </html>
  );
}
