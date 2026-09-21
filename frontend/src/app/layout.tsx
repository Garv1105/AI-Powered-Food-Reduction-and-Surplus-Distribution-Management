import './globals.css';
import Sidebar from '@/components/layout/Sidebar';
import { ReactNode } from 'react';

export const metadata = {
  title: 'FoodSaver AI',
  description: 'Food waste reduction platform',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="flex w-full min-h-screen bg-slate-50 text-navy">
        <Sidebar />
        <main className="ml-64 flex-1 w-full min-h-screen">
          {children}
        </main>
      </body>
    </html>
  );
}
