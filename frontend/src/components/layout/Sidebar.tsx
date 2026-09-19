'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, AlertTriangle, Map as MapIcon, BarChart2 } from 'lucide-react';
import clsx from 'clsx';

export default function Sidebar() {
  const pathname = usePathname();

  const links = [
    { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/surplus', label: 'Surplus & Matching', icon: AlertTriangle },
    { href: '/map', label: 'Map / Routing', icon: MapIcon },
    { href: '/reports', label: 'Reports', icon: BarChart2 },
  ];

  return (
    <aside className="fixed left-0 top-0 w-64 h-full bg-navy flex flex-col">
      <div className="p-6">
        <h1 className="text-xl font-bold text-teal">🍱 FoodSaver AI</h1>
        <p className="text-sm text-slate-400 mt-1">SIH 2026 Prototype</p>
      </div>

      <nav className="flex-1 mt-6 flex flex-col gap-2 px-4">
        {links.map((link) => {
          const isActive = pathname.startsWith(link.href);
          const Icon = link.icon;

          return (
            <Link
              key={link.href}
              href={link.href}
              className={clsx(
                'flex items-center gap-3 px-4 py-3 rounded-lg transition-colors',
                isActive
                  ? 'bg-teal/20 text-teal border-l-4 border-teal rounded-l-none'
                  : 'text-white/70 hover:bg-navy-800'
              )}
            >
              <Icon size={20} />
              <span className="font-medium">{link.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="p-6 flex items-center gap-2">
        <div className="w-2 h-2 rounded-full bg-green-500"></div>
        <span className="text-sm text-slate-400">Demo Mode</span>
      </div>
    </aside>
  );
}
