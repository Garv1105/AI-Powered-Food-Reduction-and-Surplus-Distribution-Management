'use client';

import { useEffect, useState } from 'react';
import {
  api,
  ProcessingUnitMetrics,
  FlaggedDaysResponse,
  ProcessingUnitTrendPoint,
} from '@/lib/api';
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ReferenceLine,
} from 'recharts';
import { TrendingUp, TrendingDown, Zap, AlertTriangle } from 'lucide-react';

const DATE_RANGES = ['7d', '30d', 'All'] as const;
type Range = (typeof DATE_RANGES)[number];

function rangeParam(r: Range): string {
  if (r === 'All') return '2026-03-24:2026-09-19';
  return r;
}

function fmt(n: number | null | undefined, decimals = 1, suffix = '') {
  if (n == null) return '—';
  return `${n.toFixed(decimals)}${suffix}`;
}
function fmtINR(n: number | null | undefined) {
  if (n == null) return '—';
  return `₹${n.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`;
}

function Scorecard({
  label,
  value,
  sub,
  color,
  icon: Icon,
}: {
  label: string;
  value: string;
  sub?: string;
  color: string;
  icon: React.ElementType;
}) {
  return (
    <div className="bg-white rounded-xl p-5 shadow-sm border border-slate-100">
      <div className="flex items-center justify-between mb-2">
        <p className="text-sm text-slate-500 font-medium">{label}</p>
        <div className={`p-2 rounded-lg ${color}`}>
          <Icon size={16} className="text-white" />
        </div>
      </div>
      <p className="text-2xl font-bold text-navy">{value}</p>
      {sub && <p className="text-xs text-slate-400 mt-1">{sub}</p>}
    </div>
  );
}

function TrendChart({
  data,
  dataKey,
  label,
  color,
  refLine,
  refLabel,
  suffix = '%',
}: {
  data: ProcessingUnitTrendPoint[];
  dataKey: keyof ProcessingUnitTrendPoint;
  label: string;
  color: string;
  refLine?: number;
  refLabel?: string;
  suffix?: string;
}) {
  const formatted = data.map((d) => ({
    ...d,
    displayDate: d.date.slice(5), // MM-DD
  }));

  return (
    <div className="bg-white rounded-xl p-5 shadow-sm border border-slate-100">
      <h3 className="text-sm font-semibold text-navy mb-3">{label}</h3>
      <div className="h-[180px]">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={formatted} margin={{ top: 4, right: 8, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
            <XAxis
              dataKey="displayDate"
              stroke="#94a3b8"
              fontSize={10}
              tickLine={false}
              axisLine={false}
              interval="preserveStartEnd"
            />
            <YAxis
              stroke="#94a3b8"
              fontSize={10}
              tickLine={false}
              axisLine={false}
              tickFormatter={(v) => `${v}${suffix}`}
              width={40}
            />
            <Tooltip
              contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,.1)', fontSize: 12 }}
              formatter={(v: number) => [`${v.toFixed(2)}${suffix}`, label]}
            />
            {refLine != null && (
              <ReferenceLine y={refLine} stroke="#ef4444" strokeDasharray="4 4" label={{ value: refLabel, position: 'insideTopRight', fontSize: 10, fill: '#ef4444' }} />
            )}
            <Line type="monotone" dataKey={dataKey as string} stroke={color} strokeWidth={2} dot={false} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default function ProcessingUnitPage() {
  const [range, setRange] = useState<Range>('30d');
  const [metrics, setMetrics] = useState<ProcessingUnitMetrics | null>(null);
  const [flagged, setFlagged] = useState<FlaggedDaysResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    Promise.all([
      api.getProcessingUnitMetrics(1, rangeParam(range)),
      api.getFlaggedDays(1),
    ])
      .then(([m, f]) => {
        setMetrics(m);
        setFlagged(f);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [range]);

  const agg = metrics?.aggregates ?? null;

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-navy">Processing Unit Efficiency</h1>
          <p className="text-sm text-slate-500 mt-1">
            Central Processing Unit — Maize/Pulse Line · Peenya Industrial Area, Bengaluru
          </p>
        </div>
        <div className="flex gap-2">
          {DATE_RANGES.map((r) => (
            <button
              key={r}
              onClick={() => setRange(r)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                range === r
                  ? 'bg-teal text-white'
                  : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
              }`}
            >
              {r}
            </button>
          ))}
        </div>
      </div>

      {/* Synthetic data notice */}
      <div className="bg-amber-50 border border-amber-200 rounded-lg px-4 py-3 text-sm text-amber-800">
        <strong>Prototype data:</strong> Processing-unit operational data shown here is synthetic and generated
        for system demonstration and validation. Source:{' '}
        <code className="text-xs">processing_unit_dataset_v3_verified.csv</code> (180 days, 2026-03-24 to
        2026-09-19).
      </div>

      {loading && <div className="text-slate-500 text-sm">Loading…</div>}
      {error && <div className="text-red-500 text-sm">{error}</div>}

      {!loading && metrics && (
        <>
          {/* Period info */}
          <p className="text-xs text-slate-400">
            Period: {metrics.date_range.start} → {metrics.date_range.end} · {metrics.days_with_data} days
            with data
          </p>

          {/* Scorecards */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <Scorecard
              label="Avg Process Yield"
              value={fmt(agg?.avg_process_yield_pct, 1, '%')}
              sub="Threshold: ≥ 82%"
              color={
                (agg?.avg_process_yield_pct ?? 0) >= 82
                  ? 'bg-teal'
                  : 'bg-red-500'
              }
              icon={TrendingUp}
            />
            <Scorecard
              label="Avg Downtime"
              value={fmt(agg?.avg_downtime_pct, 1, '%')}
              sub="Threshold: ≤ 15%"
              color={
                (agg?.avg_downtime_pct ?? 99) <= 15
                  ? 'bg-teal'
                  : 'bg-red-500'
              }
              icon={TrendingDown}
            />
            <Scorecard
              label="Energy Intensity"
              value={fmt(agg?.period_energy_intensity_kwh_per_kg, 3, ' kWh/kg')}
              sub="SUM(kWh) / SUM(good output)"
              color="bg-blue-500"
              icon={Zap}
            />
            <Scorecard
              label="Avg Rejection Rate"
              value={fmt(agg?.avg_rejection_pct, 2, '%')}
              sub="Threshold: ≤ 3%"
              color={
                (agg?.avg_rejection_pct ?? 99) <= 3
                  ? 'bg-teal'
                  : 'bg-red-500'
              }
              icon={AlertTriangle}
            />
          </div>

          {/* Sum metrics row */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { label: 'Net Good Output', value: fmt(agg?.total_net_good_output_kg, 0, ' kg') },
              { label: 'Total Rejected', value: fmt(agg?.total_rejected_kg, 0, ' kg') },
              { label: 'Total Profit', value: fmtINR(agg?.total_profit_inr) },
              { label: 'Waste Loss', value: fmtINR(agg?.total_waste_loss_inr) },
            ].map(({ label, value }) => (
              <div key={label} className="bg-white rounded-xl p-4 shadow-sm border border-slate-100">
                <p className="text-xs text-slate-500">{label}</p>
                <p className="text-lg font-bold text-navy mt-1">{value}</p>
              </div>
            ))}
          </div>

          {/* Trend charts */}
          {metrics.trend.length > 0 && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <TrendChart
                data={metrics.trend}
                dataKey="process_yield_pct"
                label="Process Yield % (daily)"
                color="#0d9488"
                refLine={82}
                refLabel="Min 82%"
              />
              <TrendChart
                data={metrics.trend}
                dataKey="downtime_pct"
                label="Downtime % (daily)"
                color="#f59e0b"
                refLine={15}
                refLabel="Max 15%"
              />
              <TrendChart
                data={metrics.trend}
                dataKey="rejection_pct"
                label="Rejection % (daily)"
                color="#ef4444"
                refLine={3}
                refLabel="Max 3%"
              />
              <TrendChart
                data={metrics.trend}
                dataKey="energy_intensity_kwh_per_kg"
                label="Energy Intensity (kWh/kg daily)"
                color="#6366f1"
                suffix=" kWh/kg"
              />
            </div>
          )}

          {/* Flagged days */}
          {flagged && (
            <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
              <div className="p-5 border-b border-slate-100">
                <h2 className="font-bold text-navy">
                  Flagged Days{' '}
                  <span className="ml-2 px-2 py-0.5 text-xs bg-red-100 text-red-600 rounded-full font-semibold">
                    {flagged.total_flagged_days} total
                  </span>
                </h2>
                <p className="text-xs text-slate-400 mt-1">
                  Yield &lt; 82% · Downtime &gt; 15% · Rejection &gt; 3%
                </p>
              </div>
              <div className="divide-y divide-slate-50 max-h-72 overflow-y-auto">
                {flagged.flagged_days.slice(0, 20).map((fd) => (
                  <div key={fd.date} className="px-5 py-3 hover:bg-slate-50">
                    <div className="flex items-center justify-between">
                      <div>
                        <span className="text-sm font-medium text-navy">
                          {fd.date}
                        </span>
                        <span className="ml-2 text-xs text-slate-400">{fd.day_of_week}</span>
                        <span className="ml-2 text-xs text-amber-600 font-medium">{fd.root_cause}</span>
                      </div>
                      <span className="text-xs text-slate-500">
                        {fmtINR(fd.daily_profit_inr)} profit
                      </span>
                    </div>
                    <div className="flex gap-2 mt-1 flex-wrap">
                      {fd.failed_metrics.map((fm) => (
                        <span
                          key={fm.metric}
                          className="text-xs px-2 py-0.5 bg-red-50 text-red-600 rounded-full"
                        >
                          {fm.metric}: {fm.value} ({fm.threshold})
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
