'use client';

import { useEffect, useState } from 'react';
import { api, SurplusEvent, NGOMatch } from '@/lib/api';
import NGOMatchList from '@/components/surplus/NGOMatchList';
import clsx from 'clsx';
import { Clock } from 'lucide-react';

const categoryEmojis: Record<string, string> = {
  rice: '🍚',
  dal: '🫘',
  curry: '🥘',
  roti: '🫓',
  salad: '🥗',
  dessert: '🍮',
  sambar: '🍲',
  milk: '🥛'
};

export default function SurplusPage() {
  const [events, setEvents] = useState<SurplusEvent[]>([]);
  const [selectedEvent, setSelectedEvent] = useState<SurplusEvent | null>(null);
  const [matches, setMatches] = useState<NGOMatch[]>([]);
  const [loadingEvents, setLoadingEvents] = useState(true);
  const [loadingMatches, setLoadingMatches] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getSurplus('active')
      .then((data) => {
        const urgencyOrder: Record<string, number> = { critical: 0, high: 1, medium: 2, low: 3 };
        const sorted = [...data].sort((a, b) => 
          (urgencyOrder[a.urgency_level.toLowerCase()] ?? 4) - (urgencyOrder[b.urgency_level.toLowerCase()] ?? 4)
        );
        setEvents(sorted);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoadingEvents(false));
  }, []);

  const handleSelectEvent = async (event: SurplusEvent) => {
    setSelectedEvent(event);
    setLoadingMatches(true);
    try {
      const matchData = await api.getMatches(event.id);
      setMatches(matchData);
    } catch (err: any) {
      console.error(err);
      // Fallback empty on error just in case
      setMatches([]);
    } finally {
      setLoadingMatches(false);
    }
  };

  const getUrgencyBadge = (urgency: string) => {
    switch (urgency.toLowerCase()) {
      case 'critical': return 'bg-red-100 text-red-700 border-red-200';
      case 'high': return 'bg-orange-100 text-orange-700 border-orange-200';
      case 'medium': return 'bg-amber-100 text-amber-700 border-amber-200';
      case 'low': return 'bg-green-100 text-green-700 border-green-200';
      default: return 'bg-slate-100 text-slate-700 border-slate-200';
    }
  };

  return (
    <div className="p-8 h-screen flex flex-col">
      <div className="mb-6 shrink-0">
        <h1 className="text-2xl font-bold text-navy">Surplus & Matching</h1>
        <p className="text-slate-500 mt-1">Manage food surplus and connect with NGOs</p>
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-100 mb-6 shrink-0">
          {error}
        </div>
      )}

      <div className="flex-1 min-h-0 flex gap-8">
        {/* Left Column: Surplus Events */}
        <div className="w-1/2 flex flex-col h-full bg-white rounded-xl shadow-sm border border-slate-100">
          <div className="p-4 border-b border-slate-100">
            <h2 className="font-bold text-navy">Active Surplus ({events.length})</h2>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {loadingEvents ? (
              <div className="space-y-3">
                {[1, 2, 3, 4].map(i => (
                  <div key={i} className="h-32 bg-slate-100 rounded-xl animate-pulse"></div>
                ))}
              </div>
            ) : events.length === 0 ? (
              <p className="text-center text-slate-500 py-10">No active surplus items right now.</p>
            ) : (
              events.map((event) => {
                const isSelected = selectedEvent?.id === event.id;
                
                return (
                  <div 
                    key={event.id}
                    onClick={() => handleSelectEvent(event)}
                    className={clsx(
                      'p-4 rounded-xl border cursor-pointer transition-all',
                      isSelected 
                        ? 'border-teal ring-1 ring-teal bg-teal/5 shadow-md' 
                        : 'border-slate-200 hover:border-slate-300 hover:shadow-sm bg-white'
                    )}
                  >
                    <div className="flex justify-between items-start mb-3">
                      <div className="flex items-center gap-3">
                        <div className="w-12 h-12 bg-slate-50 rounded-lg flex items-center justify-center text-2xl border border-slate-100">
                          {categoryEmojis[event.category.toLowerCase()] || '🍱'}
                        </div>
                        <div>
                          <h3 className="font-bold text-navy capitalize">{event.category}</h3>
                          <p className="text-sm text-slate-500">{event.kitchen_name}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <span className="text-xl font-bold text-navy">{event.quantity_kg}</span>
                        <span className="text-sm font-medium text-slate-500 ml-1">kg</span>
                      </div>
                    </div>
                    
                    <div className="flex items-center justify-between border-t border-slate-100 pt-3">
                      <div className="flex gap-2">
                        <span className={clsx('text-xs font-semibold px-2 py-1 rounded-md border capitalize', getUrgencyBadge(event.urgency_level))}>
                          {event.urgency_level}
                        </span>
                        <span className="text-xs font-semibold px-2 py-1 bg-slate-100 text-slate-600 rounded-md border border-slate-200 capitalize">
                          {event.status}
                        </span>
                      </div>
                      
                      <div className="flex items-center gap-1.5 text-sm font-medium text-slate-600">
                        <Clock size={14} className={event.rescue_window_hours < 2 ? 'text-red-500' : 'text-slate-400'} />
                        <span className={event.rescue_window_hours < 2 ? 'text-red-600' : ''}>
                          {event.rescue_window_hours}h left
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Right Column: NGO Matches */}
        <div className="w-1/2 flex flex-col h-full bg-slate-50 rounded-xl border border-slate-200">
          {!selectedEvent ? (
            <div className="flex-1 flex items-center justify-center text-slate-500">
              <p>Select a surplus event to see NGO matches</p>
            </div>
          ) : (
            <NGOMatchList 
              matches={matches} 
              surplusEvent={selectedEvent} 
              isLoading={loadingMatches} 
            />
          )}
        </div>
      </div>
    </div>
  );
}
