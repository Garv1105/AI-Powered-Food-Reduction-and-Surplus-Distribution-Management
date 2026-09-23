'use client';

import { useEffect, useState } from 'react';
import { api, SurplusEvent } from '@/lib/api';
import Link from 'next/link';
import clsx from 'clsx';
import { Clock } from 'lucide-react';

export default function SurplusAlertList({ events: initialEvents }: { events: SurplusEvent[] }) {
  const [events, setEvents] = useState<SurplusEvent[]>(initialEvents);
  const [loading, setLoading] = useState(initialEvents.length === 0);

  useEffect(() => {
    api.getSurplus('active')
      .then((data) => setEvents(data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [initialEvents]);

  const formatTime = (decimalHours: number) => {
    if (decimalHours <= 0) return '00:00';
    const h = Math.floor(decimalHours);
    const m = Math.round((decimalHours - h) * 60);
    return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')} T-MINUS`;
  };

  const getUrgencyIndicator = (urgency: string) => {
    switch (urgency.toUpperCase()) {
      case 'EXPIRED': return 'bg-content-secondary';
      case 'RED': return 'bg-status-critical shadow-[0_0_8px_rgba(217,86,74,0.5)]';
      case 'AMBER': return 'bg-status-warning';
      case 'GREEN': return 'bg-status-success';
      default: return 'bg-content-secondary';
    }
  };

  const getUrgencyText = (urgency: string) => {
    switch (urgency.toUpperCase()) {
      case 'EXPIRED': return 'text-content-secondary';
      case 'RED': return 'text-status-critical';
      case 'AMBER': return 'text-status-warning';
      case 'GREEN': return 'text-status-success';
      default: return 'text-content-secondary';
    }
  };

  return (
    <div className="bg-ink-surface rounded-sm border border-ink-raised p-6 flex flex-col h-full">
      <div className="flex items-center justify-between mb-4 pb-2 border-b border-ink-raised">
        <h3 className="text-lg font-display text-content-primary uppercase tracking-wide flex items-center gap-2">
          Active Surplus
          {!loading && events.length > 0 && (
            <span className="bg-ink-raised text-accent-primary font-mono text-[10px] py-0.5 px-1.5 rounded-sm">
              {events.length}
            </span>
          )}
        </h3>
      </div>

      <div className="flex-1 overflow-y-auto space-y-2">
        {loading ? (
          <div className="space-y-2">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-16 bg-ink-raised rounded-sm animate-pulse"></div>
            ))}
          </div>
        ) : events.length === 0 ? (
          <p className="text-content-secondary text-sm font-mono text-center py-8">NO ACTIVE SURPLUS.</p>
        ) : (
          events.map((event) => {
            const isExpired = event.urgency_level.toUpperCase() === 'EXPIRED';
            const isRed = event.urgency_level.toUpperCase() === 'RED';
            return (
            <div key={event.id} className={clsx(
              'p-3 rounded-sm border transition-colors flex gap-3', 
              isExpired ? 'opacity-50 border-ink-raised bg-ink-base' : 
              isRed ? 'border-status-critical/30 bg-ink-raised/50' : 'border-ink-raised bg-ink-surface hover:bg-ink-raised'
            )}>
              <div className="flex flex-col items-center gap-2 mt-1 shrink-0">
                <div className={clsx('w-2 h-2 rounded-full', getUrgencyIndicator(event.urgency_level))} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex justify-between items-start mb-0.5">
                  <p className={clsx('text-sm font-medium truncate uppercase tracking-wider', isExpired ? 'text-content-secondary line-through' : 'text-content-primary')}>{event.category}</p>
                  <span className={clsx('font-mono font-bold whitespace-nowrap ml-2', isExpired ? 'text-content-secondary line-through' : 'text-accent-secondary')}>{event.quantity_kg} kg</span>
                </div>
                <p className="text-[11px] font-mono text-content-secondary truncate mb-2 uppercase">{event.kitchen_name}</p>
                
                <div className="flex items-center justify-between">
                  <div className={clsx('flex items-center gap-1.5 font-mono text-xs tabular-nums', getUrgencyText(event.urgency_level))}>
                    <Clock size={12} className={isRed ? 'animate-pulse' : ''} />
                    {isExpired ? 'EXPIRED' : formatTime(event.rescue_window_hours)}
                  </div>
                  {!isExpired && (
                    <span className="font-mono text-[9px] uppercase tracking-widest text-content-secondary border border-ink-raised px-1 py-0.5 rounded-sm">
                      {event.status}
                    </span>
                  )}
                </div>
              </div>
            </div>
          )})
        )}
      </div>

      <Link href="/surplus" className="mt-4 text-center block text-xs font-mono uppercase tracking-widest text-accent-secondary hover:text-accent-primary transition-colors">
        View All Alerts
      </Link>
    </div>
  );
}
