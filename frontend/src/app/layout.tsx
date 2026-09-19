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
      <body className="flex w-full min-h-screen bg-slate-50 text-navy">
        <Sidebar />
        <main className="ml-64 flex-1 w-full min-h-screen">
          {children}
        </main>
      </body>
    </html>
  );
}
