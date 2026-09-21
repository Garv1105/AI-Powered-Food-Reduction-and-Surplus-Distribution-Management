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
    // If not passed initially, or just always fetch to be safe
    api.getSurplus('active')
      .then((data) => {
        // Data is already sorted by backend
        setEvents(data);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [initialEvents]);

  const getUrgencyBorder = (level: string) => {
    switch (level) {
      case 'RED': return 'bg-red-500';
      case 'AMBER': return 'bg-amber-500';
      case 'GREEN': return 'bg-green-500';
      case 'EXPIRED': return 'bg-slate-300';
      default: return 'bg-slate-300';
    }
  };

  const formatTime = (decimalHours: number) => {
    if (decimalHours <= 0) return '0m';
    const h = Math.floor(decimalHours);
    const m = Math.round((decimalHours - h) * 60);
    if (h > 0) return `${h}h ${m}m`;
    return `${m}m`;
  };

  const getUrgencyColor = (urgency: string) => {
    switch (urgency.toUpperCase()) {
      case 'EXPIRED': return 'bg-slate-400';
      case 'RED': return 'bg-red-500';
      case 'AMBER': return 'bg-amber-500';
      case 'GREEN': return 'bg-green-500';
      default: return 'bg-slate-500';
    }
  };

  const getUrgencyTextColor = (urgency: string) => {
    switch (urgency.toUpperCase()) {
      case 'EXPIRED': return 'text-slate-400';
      case 'RED': return 'text-red-600';
      case 'AMBER': return 'text-amber-600';
      case 'GREEN': return 'text-green-600';
      default: return 'text-slate-600';
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6 flex flex-col h-full">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-navy flex items-center gap-2">
          Active Surplus Alerts
          {!loading && events.length > 0 && (
            <span className="bg-slate-100 text-slate-600 text-xs py-0.5 px-2 rounded-full font-medium">
              {events.length}
            </span>
          )}
        </h3>
      </div>

      <div className="flex-1 overflow-y-auto pr-2 space-y-3">
        {loading ? (
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-20 bg-slate-100 rounded-lg animate-pulse"></div>
            ))}
          </div>
        ) : events.length === 0 ? (
          <p className="text-slate-500 text-sm text-center py-8">No active surplus alerts.</p>
        ) : (
          events.map((event) => {
            const isExpired = event.urgency_level.toUpperCase() === 'EXPIRED';
            return (
            <div key={event.id} className={clsx('p-3 rounded-lg border bg-slate-50 transition-colors flex gap-3', isExpired ? 'opacity-60 border-slate-200 bg-slate-100' : 'border-slate-100 hover:bg-slate-100')}>
              <div className={clsx('w-1.5 rounded-full shrink-0', getUrgencyColor(event.urgency_level))}></div>
              <div className="flex-1 min-w-0">
                <div className="flex justify-between items-start mb-1">
                  <p className={clsx('font-semibold truncate capitalize', isExpired ? 'text-slate-500 line-through' : 'text-navy')}>{event.category}</p>
                  <span className={clsx('font-bold whitespace-nowrap ml-2', isExpired ? 'text-slate-500 line-through' : 'text-navy')}>{event.quantity_kg} kg</span>
                </div>
                <p className="text-xs text-slate-500 truncate mb-2">{event.kitchen_name}</p>
                
                <div className="flex items-center justify-between text-xs">
                  <div className={clsx('flex items-center gap-1 font-medium', getUrgencyTextColor(event.urgency_level))}>
                    <Clock size={12} />
                    {isExpired ? 'EXPIRED' : `${formatTime(event.rescue_window_hours)} remaining`}
                  </div>
                  {!isExpired && (
                    <span className="capitalize px-1.5 py-0.5 bg-slate-200 text-slate-600 rounded text-[10px] font-semibold">
                      {event.status}
                    </span>
                  )}
                </div>
              </div>
            </div>
          )})
        )}
      </div>

      <Link href="/surplus" className="mt-4 text-center block text-sm font-medium text-teal hover:text-teal-dark transition-colors">
        View All Alerts
      </Link>
    </div>
  );
}
