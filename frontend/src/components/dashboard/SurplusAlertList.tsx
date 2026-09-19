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
    if (initialEvents.length === 0) {
      api.getSurplus('active')
        .then((data) => {
          // Sort by urgency, critical first
          const urgencyOrder: Record<string, number> = { critical: 0, high: 1, medium: 2, low: 3 };
          const sorted = [...data].sort((a, b) => 
            (urgencyOrder[a.urgency_level.toLowerCase()] ?? 4) - (urgencyOrder[b.urgency_level.toLowerCase()] ?? 4)
          );
          setEvents(sorted.slice(0, 5)); // Show top 5
        })
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [initialEvents]);

  const getUrgencyColor = (urgency: string) => {
    switch (urgency.toLowerCase()) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-amber-500';
      case 'low': return 'bg-green-500';
      default: return 'bg-slate-500';
    }
  };

  const getUrgencyTextColor = (urgency: string) => {
    switch (urgency.toLowerCase()) {
      case 'critical': return 'text-red-600';
      case 'high': return 'text-orange-600';
      case 'medium': return 'text-amber-600';
      case 'low': return 'text-green-600';
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
          events.map((event) => (
            <div key={event.id} className="p-3 rounded-lg border border-slate-100 bg-slate-50 hover:bg-slate-100 transition-colors flex gap-3">
              <div className={clsx('w-1.5 rounded-full shrink-0', getUrgencyColor(event.urgency_level))}></div>
              <div className="flex-1 min-w-0">
                <div className="flex justify-between items-start mb-1">
                  <p className="font-semibold text-navy truncate capitalize">{event.category}</p>
                  <span className="font-bold text-navy whitespace-nowrap ml-2">{event.quantity_kg} kg</span>
                </div>
                <p className="text-xs text-slate-500 truncate mb-2">{event.kitchen_name}</p>
                
                <div className="flex items-center justify-between text-xs">
                  <div className={clsx('flex items-center gap-1 font-medium', getUrgencyTextColor(event.urgency_level))}>
                    <Clock size={12} />
                    {event.rescue_window_hours}h remaining
                  </div>
                  <span className="capitalize px-1.5 py-0.5 bg-slate-200 text-slate-600 rounded text-[10px] font-semibold">
                    {event.status}
                  </span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      <Link href="/surplus" className="mt-4 text-center block text-sm font-medium text-teal hover:text-teal-dark transition-colors">
        View All Alerts
      </Link>
    </div>
  );
}
