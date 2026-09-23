'use client';

import { useEffect, useState } from 'react';
import { api, DashboardSummary, ForecastResponse } from '@/lib/api';
import ForecastChart from '@/components/dashboard/ForecastChart';
import SurplusAlertList from '@/components/dashboard/SurplusAlertList';
import { Leaf, Trash2, AlertCircle, Cloud } from 'lucide-react';

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [forecast, setForecast] = useState<ForecastResponse | null>(null);
  const [productionPlan, setProductionPlan] = useState<any>(null);
  const [surplusEvents, setSurplusEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [sumData, foreData, planData, surplusData] = await Promise.all([
          api.getDashboardSummary(),
          api.getForecast('K1_MainCampus', '2026-09-25', 7),
          api.getProductionPlan('K1_MainCampus', '2026-09-25'),
          api.getSurplus('active')
        ]);
        setSummary(sumData);
        setForecast(foreData);
        setProductionPlan(planData);
        setSurplusEvents(surplusData);
      } catch (err: any) {
        setError(err.message || 'Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleConfirmPlan = async () => {
    try {
      await api.saveProductionPlan(productionPlan);
      alert('Production plan saved successfully!');
    } catch (err: any) {
      alert('Error saving plan: ' + err.message);
    }
  };

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
    <div className="p-8 space-y-6 max-w-7xl mx-auto">
      <header className="flex justify-between items-end border-b border-ink-raised pb-4">
        <div>
          <h1 className="text-3xl font-display font-bold text-content-primary">Dashboard</h1>
          <p className="text-content-secondary mt-1 font-mono text-sm tracking-wide">REAL-TIME OVERVIEW &middot; BMTC STAFF CANTEEN, BENGALURU</p>
        </div>
        
        <div className="flex gap-6">
          <div className="text-right">
            <p className="text-xs text-content-secondary uppercase tracking-widest font-medium mb-1">Rescued Today</p>
            <p className="text-2xl font-bold font-mono text-status-success">{summary.kg_rescued_today} kg</p>
          </div>
          <div className="w-px bg-ink-raised" />
          <div className="text-right">
            <p className="text-xs text-content-secondary uppercase tracking-widest font-medium mb-1">Wasted Today</p>
            <p className="text-2xl font-bold font-mono text-status-critical">{summary.kg_wasted_today} kg</p>
          </div>
          <div className="w-px bg-ink-raised" />
          <div className="text-right">
            <p className="text-xs text-content-secondary uppercase tracking-widest font-medium mb-1">Active Alerts</p>
            <p className="text-2xl font-bold font-mono text-status-warning">{summary.active_surplus_count}</p>
          </div>
          <div className="w-px bg-ink-raised" />
          <div className="text-right">
            <p className="text-xs text-content-secondary uppercase tracking-widest font-medium mb-1">CO₂ Saved</p>
            <p className="text-2xl font-bold font-mono text-accent-secondary">{summary.co2_saved_today_kg} kg</p>
          </div>
        </div>
      </header>

      {/* Hero Chart */}
      <section className="bg-ink-surface border border-ink-raised p-6 rounded-sm">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-lg font-display text-content-primary uppercase tracking-wide flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-accent-secondary animate-pulse" />
            Demand Forecast
          </h2>
          <span className="text-xs font-mono text-content-secondary">ANUMAAN XGBOOST ENGINE &middot; MAE 49</span>
        </div>
        <div className="h-80 w-full">
          <ForecastChart data={forecast.predictions} category={forecast.category} />
        </div>
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <section className="col-span-2 bg-ink-surface border border-ink-raised p-6 rounded-sm">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-display text-content-primary uppercase tracking-wide">Production Plan</h2>
            <button 
              onClick={handleConfirmPlan}
              className="bg-accent-primary hover:bg-opacity-90 text-ink-base px-4 py-1.5 rounded-sm font-medium text-sm transition-colors uppercase tracking-wide"
            >
              Confirm Plan
            </button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left font-mono">
              <thead className="bg-ink-raised text-content-secondary text-xs uppercase tracking-wider">
                <tr>
                  <th className="px-4 py-3 font-medium">Category</th>
                  <th className="px-4 py-3 font-medium">Forecast</th>
                  <th className="px-4 py-3 font-medium">Buffer</th>
                  <th className="px-4 py-3 font-medium">Recommended</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-ink-raised">
                {productionPlan?.categories.map((cat: any) => (
                  <tr key={cat.category_id} className="hover:bg-ink-raised/30 transition-colors">
                    <td className="px-4 py-3 text-content-primary capitalize">{cat.category_name}</td>
                    <td className="px-4 py-3 text-content-secondary">{cat.predicted_qty} {cat.unit}</td>
                    <td className="px-4 py-3 text-content-secondary" title={cat.buffer_reasoning}>
                      {(cat.buffer_pct * 100).toFixed(1)}%
                    </td>
                    <td className="px-4 py-3 font-bold text-accent-secondary">{cat.recommended_production_qty} {cat.unit}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="col-span-1">
          <SurplusAlertList events={surplusEvents} />
        </section>
      </div>
    </div>
  );
}
