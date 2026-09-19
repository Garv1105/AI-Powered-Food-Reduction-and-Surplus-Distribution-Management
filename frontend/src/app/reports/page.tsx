'use client';

import { useEffect, useState } from 'react';
import { api, DashboardSummary } from '@/lib/api';
import { ResponsiveContainer, BarChart, CartesianGrid, XAxis, YAxis, Tooltip, Legend, Bar } from 'recharts';
import { Leaf, Cloud, Users, CheckCircle } from 'lucide-react';

export default function ReportsPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getDashboardSummary()
      .then(setSummary)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="p-8">Loading reports...</div>;
  }

  if (!summary) return null;

  // Calculate weekly totals
  const weeklyRescued = summary.weekly_trend.reduce((sum, d) => sum + d.kg_rescued, 0);
  const weeklyWasted = summary.weekly_trend.reduce((sum, d) => sum + d.kg_wasted, 0);
  const weeklyMeals = summary.weekly_trend.reduce((sum, d) => sum + d.meals_served, 0);
  const weeklyCo2 = summary.weekly_trend.reduce((sum, d) => sum + d.co2_saved_kg, 0);
  const rescueRate = weeklyRescued + weeklyWasted > 0 
    ? Math.round((weeklyRescued / (weeklyRescued + weeklyWasted)) * 100) 
    : 0;

  const dateRangeStr = summary.weekly_trend.length > 0
    ? `${summary.weekly_trend[0].date} to ${summary.weekly_trend[summary.weekly_trend.length - 1].date}`
    : 'No data';

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-navy">Sustainability Report</h1>
        <p className="text-slate-500 mt-1">Week of {dateRangeStr}</p>
      </div>

      <div className="grid grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
          <div className="flex items-center gap-3 mb-2">
            <Leaf size={18} className="text-green-600" />
            <h3 className="text-sm font-semibold text-slate-500">Rescued (Week)</h3>
          </div>
          <p className="text-3xl font-bold text-navy">{weeklyRescued} <span className="text-lg font-medium text-slate-500">kg</span></p>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
          <div className="flex items-center gap-3 mb-2">
            <Cloud size={18} className="text-teal" />
            <h3 className="text-sm font-semibold text-slate-500">CO₂ Saved</h3>
          </div>
          <p className="text-3xl font-bold text-navy">{weeklyCo2} <span className="text-lg font-medium text-slate-500">kg</span></p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
          <div className="flex items-center gap-3 mb-2">
            <Users size={18} className="text-blue-600" />
            <h3 className="text-sm font-semibold text-slate-500">Meals Served</h3>
          </div>
          <p className="text-3xl font-bold text-navy">{weeklyMeals}</p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
          <div className="flex items-center gap-3 mb-2">
            <CheckCircle size={18} className="text-amber-500" />
            <h3 className="text-sm font-semibold text-slate-500">Rescue Rate</h3>
          </div>
          <p className="text-3xl font-bold text-navy">{rescueRate}%</p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
        <h3 className="text-lg font-bold text-navy mb-6">Weekly Breakdown Table</h3>
        <div className="h-[280px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={summary.weekly_trend} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
              <XAxis dataKey="date" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
              <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} tickFormatter={v => `${v}kg`} />
              <Tooltip cursor={{ fill: '#f1f5f9' }} contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
              <Legend iconType="circle" />
              <Bar dataKey="kg_rescued" name="Rescued (kg)" fill="#0d9488" radius={[4, 4, 0, 0]} barSize={32} />
              <Bar dataKey="kg_wasted" name="Wasted (kg)" fill="#ef4444" radius={[4, 4, 0, 0]} barSize={32} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
        <div className="p-6 border-b border-slate-100">
          <h3 className="text-lg font-bold text-navy">Daily Log Table</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-teal/5 text-teal-dark border-b border-slate-200">
              <tr>
                <th className="px-6 py-4 font-semibold">Date</th>
                <th className="px-6 py-4 font-semibold">Rescued (kg)</th>
                <th className="px-6 py-4 font-semibold">Wasted (kg)</th>
                <th className="px-6 py-4 font-semibold">Meals Served</th>
                <th className="px-6 py-4 font-semibold">CO₂ Saved (kg)</th>
                <th className="px-6 py-4 font-semibold">Rescue Rate (%)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {summary.weekly_trend.map((stat, i) => {
                const total = stat.kg_rescued + stat.kg_wasted;
                const rate = total > 0 ? Math.round((stat.kg_rescued / total) * 100) : 0;
                
                return (
                  <tr key={stat.date} className={i % 2 === 0 ? 'bg-white' : 'bg-slate-50'}>
                    <td className="px-6 py-4 font-medium text-navy">{stat.date}</td>
                    <td className="px-6 py-4 text-green-600 font-medium">{stat.kg_rescued}</td>
                    <td className="px-6 py-4 text-red-500">{stat.kg_wasted}</td>
                    <td className="px-6 py-4 text-slate-700">{stat.meals_served}</td>
                    <td className="px-6 py-4 text-slate-700">{stat.co2_saved_kg}</td>
                    <td className="px-6 py-4 font-medium text-navy">{rate}%</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      <p className="text-xs text-slate-500 text-center pb-8">
        * CO₂ factor: 1 kg food rescued = 2.5 kg CO₂ equivalent saved. Cost estimate: ₹50/kg.
      </p>
    </div>
  );
}
