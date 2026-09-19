'use client';

import { NGOMatch, SurplusEvent } from '@/lib/api';
import { CheckCircle2, XCircle, MapPin, Scale } from 'lucide-react';
import clsx from 'clsx';

interface NGOMatchListProps {
  matches: NGOMatch[];
  surplusEvent: SurplusEvent | null;
  isLoading: boolean;
}

export default function NGOMatchList({ matches, surplusEvent, isLoading }: NGOMatchListProps) {
  if (isLoading) {
    return (
      <div className="p-6 space-y-4">
        <div className="h-6 w-1/2 bg-slate-200 rounded animate-pulse mb-6"></div>
        {[1, 2, 3].map(i => (
          <div key={i} className="h-40 bg-white rounded-xl shadow-sm border border-slate-100 animate-pulse"></div>
        ))}
      </div>
    );
  }

  if (!surplusEvent) return null;

  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b border-slate-200 bg-white rounded-t-xl">
        <h2 className="font-bold text-navy">
          Matching Results for: <span className="capitalize">{surplusEvent.category}</span>
        </h2>
        <p className="text-sm text-slate-500">
          Finding NGOs to rescue {surplusEvent.quantity_kg}kg
        </p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {matches.length === 0 ? (
          <div className="text-center py-10 bg-white rounded-xl border border-slate-200">
            <p className="text-slate-500">No suitable NGOs found for this surplus.</p>
          </div>
        ) : (
          matches.map((match) => {
            const scoreColor = 
              match.match_score >= 0.8 ? 'bg-green-500' :
              match.match_score >= 0.6 ? 'bg-amber-500' : 'bg-red-500';

            return (
              <div key={match.ngo_id} className="bg-white p-5 rounded-xl shadow-sm border border-slate-100">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h3 className="font-bold text-navy text-lg">{match.name}</h3>
                    <p className="text-sm text-slate-500 mt-0.5">{match.address}</p>
                  </div>
                  <div className="w-16 h-16 relative flex items-center justify-center">
                    <svg className="w-full h-full -rotate-90" viewBox="0 0 36 36">
                      <path
                        className="text-slate-100"
                        strokeWidth="3"
                        stroke="currentColor"
                        fill="none"
                        d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      />
                      <path
                        className={scoreColor.replace('bg-', 'text-')}
                        strokeWidth="3"
                        strokeDasharray={`${match.match_score * 100}, 100`}
                        stroke="currentColor"
                        fill="none"
                        d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      />
                    </svg>
                    <span className="absolute text-xs font-bold text-navy">
                      {Math.round(match.match_score * 100)}%
                    </span>
                  </div>
                </div>

                <div className="flex gap-2 mb-4 flex-wrap">
                  <span className="text-xs font-medium px-2 py-1 bg-slate-100 text-slate-600 rounded-md border border-slate-200 capitalize">
                    {match.food_preference} Pref
                  </span>
                  <span className="text-xs font-medium px-2 py-1 bg-slate-100 text-slate-600 rounded-md border border-slate-200 flex items-center gap-1">
                    <Scale size={12} />
                    {match.capacity_kg}kg Capacity
                  </span>
                  <span className="text-xs font-medium px-2 py-1 bg-slate-100 text-slate-600 rounded-md border border-slate-200 flex items-center gap-1">
                    <MapPin size={12} />
                    {match.distance_km}km
                  </span>
                </div>

                <div className="space-y-2 mb-5">
                  <div className="flex items-center gap-2 text-sm">
                    {match.capacity_match ? (
                      <CheckCircle2 size={16} className="text-green-500" />
                    ) : (
                      <XCircle size={16} className="text-red-500" />
                    )}
                    <span className={match.capacity_match ? 'text-slate-700' : 'text-slate-500 line-through'}>
                      Capacity Match
                    </span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    {match.food_pref_match ? (
                      <CheckCircle2 size={16} className="text-green-500" />
                    ) : (
                      <XCircle size={16} className="text-red-500" />
                    )}
                    <span className={match.food_pref_match ? 'text-slate-700' : 'text-slate-500'}>
                      Food Preference Match
                    </span>
                  </div>
                </div>

                <button 
                  onClick={() => alert(`Delivery assigned to ${match.name} (stub)!`)}
                  className="w-full bg-teal hover:bg-teal-dark text-white font-semibold py-2.5 rounded-lg transition-colors text-sm"
                >
                  Assign Delivery
                </button>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
