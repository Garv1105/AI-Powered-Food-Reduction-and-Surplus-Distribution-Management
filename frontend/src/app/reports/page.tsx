'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { BarChart2, Cloud, Users, CheckCircle, Leaf, AlertCircle } from 'lucide-react';
import clsx from 'clsx';

export default function ReportsPage() {
  const [dateRange, setDateRange] = useState('30d');
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [demoMode, setDemoMode] = useState(true);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const data = await api.getSustainabilityReport(dateRange);
        setReport(data);
        setError(null);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [dateRange]);

  const metrics = report?.metrics;
  const prov = report?.provenance;
  const llmStatus = report?.llm_error || '';

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-6 h-screen overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between shrink-0">
        <div>
          <h1 className="text-2xl font-bold text-navy">Sustainability Report</h1>
          <p className="text-sm text-slate-500 mt-1">
            {demoMode ? "Automated sustainability narrative and impact metrics" : "LLM-grounded narrative backed by aggregated metrics"}
          </p>
        </div>
        <div className="flex gap-4 items-center">
          <label className="flex items-center gap-2 cursor-pointer bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200">
            <input 
              type="checkbox" 
              checked={demoMode} 
              onChange={e => setDemoMode(e.target.checked)} 
              className="rounded text-teal focus:ring-teal"
            />
            <span className="text-sm font-medium text-slate-700">Presentation Mode</span>
          </label>
          <select 
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
            className="border-slate-200 rounded-lg text-sm bg-white"
          >
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="90d">Last Quarter</option>
          </select>
        </div>
      </div>

      {loading && <div className="p-8 animate-pulse text-slate-500">Generating report...</div>}
      
      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-100">
          {error}
        </div>
      )}

      {!demoMode && llmStatus && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg px-4 py-3 text-sm text-amber-800 flex items-center gap-2">
          <AlertCircle size={16} />
          <strong>Developer Notice:</strong> {llmStatus.includes('fell back') ? 'Add GEMINI_API_KEY to backend/.env to enable real narrative generation.' : llmStatus}
        </div>
      )}

      {!loading && report && (
        <>
          {/* Key Metrics Grid */}
          <div className="grid grid-cols-4 gap-4">
            <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-100">
              <div className="flex items-center gap-3 mb-2">
                <Leaf size={16} className="text-green-600" />
                <h3 className="text-sm font-semibold text-slate-500">Rescued</h3>
              </div>
              <p className="text-2xl font-bold text-navy">{metrics?.surplus?.kg_rescued || 0} <span className="text-sm font-medium text-slate-500">kg</span></p>
            </div>
            
            <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-100">
              <div className="flex items-center gap-3 mb-2">
                <Cloud size={16} className="text-teal" />
                <h3 className="text-sm font-semibold text-slate-500">CO2e Avoided</h3>
              </div>
              <p className="text-2xl font-bold text-navy">{metrics?.impact?.co2e_avoided_kg || 0} <span className="text-sm font-medium text-slate-500">kg</span></p>
            </div>

            <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-100">
              <div className="flex items-center gap-3 mb-2">
                <Users size={16} className="text-blue-600" />
                <h3 className="text-sm font-semibold text-slate-500">Meals Redistributed</h3>
              </div>
              <p className="text-2xl font-bold text-navy">{metrics?.impact?.meals_redistributed || 0}</p>
            </div>

            <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-100">
              <div className="flex items-center gap-3 mb-2">
                <CheckCircle size={16} className="text-amber-500" />
                <h3 className="text-sm font-semibold text-slate-500">Rescue Rate</h3>
              </div>
              <p className="text-2xl font-bold text-navy">{metrics?.surplus?.rescue_rate_pct || 0}%</p>
            </div>
          </div>

          {/* Narrative */}
          <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden flex flex-col">
            <div className="p-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
              <h2 className="font-bold text-navy">Executive Summary</h2>
              <span className={clsx("text-xs font-semibold px-2 py-1 rounded border", 
                report.narrative_source === 'gemini' ? 'bg-teal/10 text-teal border-teal/20' : 'bg-slate-100 text-slate-600 border-slate-200'
              )}>
                Source: {report.narrative_source}
              </span>
            </div>
            <div className="p-6 prose prose-slate max-w-none text-slate-700">
              {report.narrative.split('\n\n').map((paragraph: string, i: number) => (
                <p key={i} className="mb-4 last:mb-0 leading-relaxed text-sm">{paragraph}</p>
              ))}
            </div>
          </div>

          {/* Provenance */}
          {!demoMode && (
            <div className="bg-white rounded-xl p-5 shadow-sm border border-slate-100">
              <h2 className="font-bold text-navy mb-3 flex items-center gap-2">
                <BarChart2 size={18} className="text-teal" /> Provenance & Assumptions
              </h2>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-slate-500 text-xs font-medium mb-1">Data Sources</p>
                  <ul className="text-slate-700 space-y-1 list-disc list-inside">
                    <li>Synthetic SQLite Kitchen Data</li>
                    <li>{prov?.processing_unit_dataset || 'processing_unit_dataset_v3_verified.csv'}</li>
                  </ul>
                </div>
                <div>
                  <p className="text-slate-500 text-xs font-medium mb-1">Standard Assumptions</p>
                  <ul className="text-slate-700 space-y-1 list-disc list-inside">
                    <li>Meals: {prov?.documented_assumptions?.meal_weight_kg || '0.4 kg/meal'}</li>
                    <li>Emissions: {prov?.documented_assumptions?.co2e_factor || '2.5 kg CO2e/kg'}</li>
                  </ul>
                </div>
              </div>
            </div>
          )}

          {demoMode && (
             <div className="text-center pb-8 pt-4">
               <p className="text-xs text-slate-400">
                 Note: CO2e factor based on global average (FAO, 2013). Meal weight assumption sourced from FSSAI institutional guidance (0.4kg/meal).
               </p>
             </div>
          )}
        </>
      )}
    </div>
  );
}
