'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';
import { LayoutDashboard, AlertTriangle, Map as MapIcon, BarChart2, BrainCircuit, Factory } from 'lucide-react';
import clsx from 'clsx';
import { api } from '@/lib/api';

export default function Sidebar() {
  const pathname = usePathname();
  const [backendOk, setBackendOk] = useState<boolean | null>(null);
  const [activeAlerts, setActiveAlerts] = useState<number>(0);

  useEffect(() => {
    async function ping() {
      try {
        const res = await fetch('http://127.0.0.1:8080/health', { cache: 'no-store' });
        const data = await res.json();
        setBackendOk(res.ok && data.status === 'ok');
      } catch {
        setBackendOk(false);
      }
    }
    ping();
    const id = setInterval(ping, 15_000);
    return () => clearInterval(id);
  }, []);

  useEffect(() => {
    async function checkAlerts() {
      try {
        const summary = await api.getDashboardSummary();
        setActiveAlerts(summary.active_surplus_count);
      } catch {
        // ignore
      }
    }
    checkAlerts();
    const id = setInterval(checkAlerts, 15_000);
    return () => clearInterval(id);
  }, []);

  const links = [
    { href: '/dashboard', label: 'Dashboard',         icon: LayoutDashboard },
    { href: '/anumaan',   label: 'Anumaan',            icon: BrainCircuit    },
    { href: '/surplus',   label: 'Surplus & Matching', icon: AlertTriangle, hasAlerts: activeAlerts > 0 },
    { href: '/map',             label: 'Map / Routing',      icon: MapIcon         },
    { href: '/processing-unit', label: 'Processing Unit',     icon: Factory         },
    { href: '/reports',         label: 'Reports',             icon: BarChart2       },
  ];

  return (
    <aside className="fixed left-0 top-0 w-64 h-full bg-ink-surface border-r border-ink-raised flex flex-col z-50">
      <div className="p-6">
        <h1 className="text-2xl font-display font-bold text-accent-secondary">Anna Setu</h1>
        <p className="text-xs font-mono text-content-secondary mt-1 tracking-wider uppercase">Ops Console</p>
      </div>

      <nav className="flex-1 mt-6 flex flex-col gap-1 px-3">
        {links.map((link) => {
          const isActive = pathname.startsWith(link.href);
          const Icon = link.icon;

          return (
            <Link
              key={link.href}
              href={link.href}
              className={clsx(
                'flex items-center gap-3 px-3 py-2.5 rounded text-sm transition-colors relative',
                isActive
                  ? 'bg-ink-raised text-accent-primary font-medium'
                  : 'text-content-secondary hover:text-content-primary hover:bg-ink-raised/50'
              )}
            >
              <Icon size={18} className={isActive ? 'text-accent-primary' : 'text-content-secondary'} />
              <span className="flex-1">{link.label}</span>
              {link.hasAlerts && (
                <div className="w-2 h-2 rounded-full bg-status-warning animate-pulse" title={`${activeAlerts} active alerts`} />
              )}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-ink-raised mx-3 mb-3 flex items-center gap-2">
        {backendOk === null ? (
          <div className="w-2 h-2 rounded-full bg-content-secondary animate-pulse" />
        ) : backendOk ? (
          <div className="w-2 h-2 rounded-full bg-status-success" />
        ) : (
          <div className="w-2 h-2 rounded-full bg-status-critical animate-pulse" />
        )}
        <span className="text-xs text-content-secondary font-mono">
          {backendOk === null ? 'SYS_CHECKING...' : backendOk ? 'SYS_ONLINE' : 'SYS_OFFLINE'}
        </span>
      </div>
    </aside>
  );
}
