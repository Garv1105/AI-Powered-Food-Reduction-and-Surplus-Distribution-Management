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
        <div className="col-span-2 space-y-6">
          <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6 relative group">
            <div className="absolute top-4 right-4 text-xs text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity bg-slate-50 p-2 rounded border border-slate-100 z-10 shadow-sm pointer-events-none w-64">
              Forecast powered by Anumaan (XGBoost, MAE ~49 customers on held-out test data).
            </div>
            <ForecastChart data={forecast.predictions} category={forecast.category} />
          </div>
          
          <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-navy">Today's Production Plan</h2>
              <button 
                onClick={handleConfirmPlan}
                className="bg-teal hover:bg-teal-600 text-white px-4 py-2 rounded font-medium transition-colors"
              >
                Confirm Plan
              </button>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="bg-slate-50 text-slate-600">
                  <tr>
                    <th className="px-4 py-2">Category</th>
                    <th className="px-4 py-2">Forecast</th>
                    <th className="px-4 py-2">Buffer</th>
                    <th className="px-4 py-2">Recommended</th>
                  </tr>
                </thead>
                <tbody>
                  {productionPlan?.categories.map((cat: any) => (
                    <tr key={cat.category_id} className="border-b border-slate-100">
                      <td className="px-4 py-2 font-medium capitalize">{cat.category_name}</td>
                      <td className="px-4 py-2">{cat.predicted_qty} {cat.unit}</td>
                      <td className="px-4 py-2 text-slate-500" title={cat.buffer_reasoning}>
                        {(cat.buffer_pct * 100).toFixed(1)}%
                      </td>
                      <td className="px-4 py-2 font-bold text-navy">{cat.recommended_production_qty} {cat.unit}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div className="col-span-1">
          <SurplusAlertList events={surplusEvents} />
        </div>
      </div>
    </div>
  );
}
