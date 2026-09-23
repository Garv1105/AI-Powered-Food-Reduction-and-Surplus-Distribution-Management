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
  if (n == null) return 'â€”';
  return `${n.toFixed(decimals)}${suffix}`;
}
function fmtINR(n: number | null | undefined) {
  if (n == null) return 'â€”';
  return `â‚¹${n.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`;
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
    <div className="bg-ink-surface rounded-sm p-5 border border-ink-raised shadow-none">
      <div className="flex items-center justify-between mb-2">
        <p className="font-mono text-xs uppercase tracking-widest text-content-secondary">{label}</p>
        <div className={`p-2 rounded-lg ${color}`}>
          <Icon size={16} className="text-white" />
        </div>
      </div>
      <p className="text-3xl font-mono font-bold text-accent-secondary">{value}</p>
      {sub && <p className="text-xs text-content-secondary mt-1">{sub}</p>}
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
    <div className="bg-ink-surface rounded-sm p-5 border border-ink-raised shadow-none">
      <h3 className="font-display font-bold uppercase tracking-wide text-content-primary mb-3">{label}</h3>
      <div className="h-[180px]">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={formatted} margin={{ top: 4, right: 8, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#232B38" />
            <XAxis
              dataKey="displayDate"
              stroke="#9AA3B2"
              fontSize={10}
              tickLine={false}
              axisLine={false}
              interval="preserveStartEnd"
            />
            <YAxis
              stroke="#9AA3B2"
              fontSize={10}
              tickLine={false}
              axisLine={false}
              tickFormatter={(v) => `${v}${suffix}`}
              width={40}
            />
            <Tooltip
              contentStyle={{ backgroundColor: '#232B38', border: '1px solid #1B212B', borderRadius: '4px', color: '#F2F0EA', fontSize: 12 }} itemStyle={{ color: '#F2F0EA' }}
              formatter={(v: number) => [`${v.toFixed(2)}${suffix}`, label]}
            />
            {refLine != null && (
              <ReferenceLine y={refLine} stroke="#E8A33D" strokeDasharray="4 4" label={{ value: refLabel, position: 'insideTopRight', fontSize: 10, fill: '#E8A33D' }} />
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
          <h1 className="text-3xl font-display font-bold text-content-primary">Processing Unit Efficiency</h1>
          <p className="text-sm text-content-secondary mt-1">
            Central Processing Unit â€” Maize/Pulse Line Â· Peenya Industrial Area, Bengaluru
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
                  : 'bg-ink-surface text-content-secondary border border-ink-raised hover:bg-ink-raised transition-colors'
              }`}
            >
              {r}
            </button>
          ))}
        </div>
      </div>



      {loading && <div className="text-content-secondary text-sm">Loadingâ€¦</div>}
      {error && <div className="text-red-500 text-sm">{error}</div>}

      {!loading && metrics && (
        <>
          {/* Period info */}
          <p className="text-xs text-content-secondary">
            Period: {metrics.date_range.start} â†’ {metrics.date_range.end} Â· {metrics.days_with_data} days
            with data
          </p>

          {/* Scorecards */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <Scorecard
              label="Avg Process Yield"
              value={fmt(agg?.avg_process_yield_pct, 1, '%')}
              sub="Threshold: â‰¥ 82%"
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
              sub="Threshold: â‰¤ 15%"
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
              sub="Threshold: â‰¤ 3%"
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
              <div key={label} className="bg-ink-surface rounded-sm p-4 border border-ink-raised shadow-none">
                <p className="text-xs text-content-secondary">{label}</p>
                <p className="text-lg font-bold text-content-primary mt-1">{value}</p>
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
            <div className="bg-ink-surface rounded-sm border border-ink-raised shadow-none overflow-hidden">
              <div className="p-5 border-b border-ink-raised">
                <h2 className="font-bold text-content-primary">
                  Flagged Days{' '}
                  <span className="ml-2 px-2 py-0.5 text-xs bg-status-critical/10 text-status-critical border border-status-critical/20 font-mono rounded-full font-semibold">
                    {flagged.total_flagged_days} total
                  </span>
                </h2>
                <p className="text-xs text-content-secondary mt-1">
                  Yield &lt; 82% Â· Downtime &gt; 15% Â· Rejection &gt; 3%
                </p>
              </div>
              <div className="divide-y divide-slate-50 max-h-72 overflow-y-auto">
                {flagged.flagged_days.slice(0, 20).map((fd) => (
                  <div key={fd.date} className="px-5 py-3 hover:bg-ink-raised transition-colors">
                    <div className="flex items-center justify-between">
                      <div>
                        <span className="text-sm font-medium text-content-primary">
                          {fd.date}
                        </span>
                        <span className="ml-2 text-xs text-content-secondary">{fd.day_of_week}</span>
                        <span className="ml-2 text-xs text-amber-600 font-medium">{fd.root_cause}</span>
                      </div>
                      <span className={`text-xs font-medium ${(fd.daily_profit_inr ?? 0) >= 0 ? "text-emerald-600" : "text-rose-600"}`}>
                        â‚¹{Math.abs(fd.daily_profit_inr ?? 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })} {(fd.daily_profit_inr ?? 0) >= 0 ? 'profit' : 'loss'}
                      </span>
                    </div>
                    <div className="flex gap-2 mt-1 flex-wrap">
                      {fd.failed_metrics.map((fm) => (
                        <span
                          key={fm.metric}
                          className="text-xs px-2 py-0.5 bg-status-critical/10 text-status-critical border border-status-critical/20 font-mono tracking-widest uppercase rounded-full"
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
