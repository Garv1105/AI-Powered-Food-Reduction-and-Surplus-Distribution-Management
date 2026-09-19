'use client';

import { useEffect, useState } from 'react';
import { api, DashboardSummary, ForecastResponse } from '@/lib/api';
import ForecastChart from '@/components/dashboard/ForecastChart';
import SurplusAlertList from '@/components/dashboard/SurplusAlertList';
import { Leaf, Trash2, AlertCircle, Cloud } from 'lucide-react';

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [forecast, setForecast] = useState<ForecastResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [sumData, foreData] = await Promise.all([
          api.getDashboardSummary(),
          api.getForecast('rice', 7) // Using 'rice' and 7 days as default
        ]);
        setSummary(sumData);
        setForecast(foreData);
      } catch (err: any) {
        setError(err.message || 'Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="p-8 space-y-6 animate-pulse">
        <div className="h-10 bg-slate-200 rounded w-1/4"></div>
        <div className="grid grid-cols-4 gap-6">
          <div className="h-32 bg-slate-200 rounded-xl"></div>
          <div className="h-32 bg-slate-200 rounded-xl"></div>
          <div className="h-32 bg-slate-200 rounded-xl"></div>
          <div className="h-32 bg-slate-200 rounded-xl"></div>
        </div>
        <div className="grid grid-cols-3 gap-6">
          <div className="h-80 bg-slate-200 rounded-xl col-span-2"></div>
          <div className="h-80 bg-slate-200 rounded-xl"></div>
        </div>
      </div>
    );
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

  if (!summary || !forecast) return null;

  return (
    <div className="p-8 space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-navy">Dashboard</h1>
        <p className="text-slate-500 mt-1">Real-time overview · BMTC Staff Canteen, Bengaluru</p>
      </div>

      <div className="grid grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex items-center gap-4">
          <div className="w-12 h-12 bg-green-50 text-green-600 rounded-lg flex items-center justify-center shrink-0">
            <Leaf size={24} />
          </div>
          <div>
            <p className="text-sm text-slate-500 font-medium">Rescued Today</p>
            <p className="text-2xl font-bold text-green-600">{summary.kg_rescued_today} kg</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex items-center gap-4">
          <div className="w-12 h-12 bg-red-50 text-red-600 rounded-lg flex items-center justify-center shrink-0">
            <Trash2 size={24} />
          </div>
          <div>
            <p className="text-sm text-slate-500 font-medium">Wasted Today</p>
            <p className="text-2xl font-bold text-red-600">{summary.kg_wasted_today} kg</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex items-center gap-4">
          <div className="w-12 h-12 bg-amber-50 text-amber-600 rounded-lg flex items-center justify-center shrink-0">
            <AlertCircle size={24} />
          </div>
          <div>
            <p className="text-sm text-slate-500 font-medium">Active Surplus</p>
            <p className="text-2xl font-bold text-amber-600">{summary.active_surplus_count} items</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex items-center gap-4">
          <div className="w-12 h-12 bg-teal/10 text-teal rounded-lg flex items-center justify-center shrink-0">
            <Cloud size={24} />
          </div>
          <div>
            <p className="text-sm text-slate-500 font-medium">CO₂ Saved</p>
            <p className="text-2xl font-bold text-teal">{summary.co2_saved_today_kg} kg</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2 bg-white rounded-xl shadow-sm border border-slate-100 p-6">
          <ForecastChart data={forecast.predictions} category={forecast.category} />
        </div>
        <div className="col-span-1">
          {/* We will fetch surplus events here or pass empty array for now and let the component handle its own fetch or just fetch it in dashboard */}
          <SurplusAlertList events={[]} />
        </div>
      </div>
    </div>
  );
}
