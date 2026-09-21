'use client';

import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
import { api, RouteResponse, NGOMatch } from '@/lib/api';
import { Navigation2, Clock, MapPin } from 'lucide-react';
import clsx from 'clsx';

const RouteMap = dynamic(() => import('@/components/map/RouteMap'), { 
  ssr: false, 
  loading: () => (
    <div className="w-full h-full bg-slate-100 animate-pulse flex items-center justify-center text-slate-500">
      Loading map...
    </div>
  )
});

export default function MapPage() {
  const [route, setRoute] = useState<RouteResponse | null>(null);
  const [ngos, setNgos] = useState<NGOMatch[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [optimizing, setOptimizing] = useState(false);

  const [activeSurplusId, setActiveSurplusId] = useState<number | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const events = await api.getSurplus('ACTIVE');
        if (events.length > 0) {
          const id = events[0].id;
          setActiveSurplusId(id);
          const ngoData = await api.getMatches(id);
          setNgos(ngoData);
        } else {
          setNgos([]);
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleOptimize = async () => {
    if (!activeSurplusId) {
      setError("No active surplus event to route.");
      return;
    }
    try {
      setOptimizing(true);
      setError(null);
      // Pass the active surplus delivery ID. Note: deliveries may not exist yet in demo, but we use the surplus ID as a proxy delivery ID for the demo spec
      const routeData = await api.optimizeRoute(1, [activeSurplusId]);
      setRoute(routeData);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setOptimizing(false);
    }
  };

  if (loading) {
    return <div className="p-8">Loading map data...</div>;
  }

  if (error) {
    return (
      <div className="p-8">
        <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-100">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen w-full relative">
      <div className="p-6 pb-4 shrink-0 bg-white border-b border-slate-200 z-10 shadow-sm relative">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-2xl font-bold text-navy">Map / Routing</h1>
          <button
            onClick={handleOptimize}
            disabled={optimizing}
            className="bg-teal text-white px-4 py-2 rounded-lg font-medium shadow-sm hover:bg-teal/90 disabled:opacity-50"
          >
            {optimizing ? 'Optimizing...' : 'Optimize Route'}
          </button>
        </div>
        
        {route ? (
          <div className="flex flex-col gap-4">
            <div className="flex gap-6">
              <div className="flex items-center gap-2 bg-slate-50 px-4 py-2 rounded-lg border border-slate-200">
                <Navigation2 className="text-teal" size={20} />
                <div>
                  <p className="text-xs text-slate-500 font-medium">Total Distance</p>
                  <p className="font-bold text-navy">{route.total_distance_km} km</p>
                </div>
              </div>
              
              <div className="flex items-center gap-2 bg-slate-50 px-4 py-2 rounded-lg border border-slate-200">
                <Clock className="text-amber-600" size={20} />
                <div>
                  <p className="text-xs text-slate-500 font-medium">Est. Time</p>
                  <p className="font-bold text-navy">{route.eta_minutes} mins</p>
                </div>
              </div>

              <div className="flex items-center gap-2 bg-slate-50 px-4 py-2 rounded-lg border border-slate-200">
                <MapPin className="text-navy" size={20} />
                <div>
                  <p className="text-xs text-slate-500 font-medium">Waypoints</p>
                  <p className="font-bold text-navy">{route.waypoints.length} stops</p>
                </div>
              </div>

              {route.routing_method_used && (
                <div className="flex items-center gap-2 bg-slate-50 px-4 py-2 rounded-lg border border-slate-200">
                  <div className="px-2 py-1 bg-navy/10 text-navy font-bold text-[10px] rounded uppercase">
                    {route.routing_method_used}
                  </div>
                  <div>
                    <p className="text-xs text-slate-500 font-medium">Method</p>
                  </div>
                </div>
              )}
            </div>

            {/* Waypoint Sequence */}
            <div className="flex items-center flex-wrap gap-2 text-sm text-slate-600 font-medium bg-slate-50 p-3 rounded-lg border border-slate-200">
              <span className="text-xs text-slate-400 uppercase tracking-wider font-bold mr-1">Sequence:</span>
              {route.waypoints.map((wp, i) => (
                <div key={i} className="flex items-center gap-2">
                  <span className={clsx("px-2 py-0.5 rounded text-xs", wp.type === 'kitchen' ? 'bg-navy text-white' : 'bg-teal/10 text-teal border border-teal/20')}>
                    {wp.name}
                  </span>
                  {i < route.waypoints.length - 1 && <span className="text-slate-300">→</span>}
                </div>
              ))}
            </div>
          </div>
        ) : (
          <p className="text-slate-500 text-sm">Click "Optimize Route" to generate an optimized delivery plan using OR-Tools VRPTW.</p>
        )}
      </div>

      <div className="flex-1 w-full relative z-0" style={{ height: 'calc(100vh - 140px)' }}>
        <RouteMap route={route} ngos={ngos} />
        
        {/* Overlay Sidebar */}
        <div className="absolute top-4 right-4 w-80 max-h-[calc(100%-32px)] bg-white rounded-xl shadow-lg border border-slate-200 flex flex-col overflow-hidden z-10">
          <div className="p-4 border-b border-slate-100 bg-navy text-white">
            <h3 className="font-bold">Nearby NGOs</h3>
          </div>
          <div className="flex-1 overflow-y-auto p-2">
            {ngos.map(ngo => (
              <div key={ngo.ngo_id} className="p-3 border-b border-slate-100 last:border-0 hover:bg-slate-50">
                <h4 className="font-bold text-sm text-navy">{ngo.ngo_name}</h4>
                <div className="flex justify-between items-center mt-1">
                  <p className="text-xs text-slate-500 truncate max-w-[180px]">{ngo.match_reason}</p>
                  <span className="text-xs font-semibold text-teal bg-teal/10 px-2 py-0.5 rounded">
                    {ngo.distance_km} km
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
