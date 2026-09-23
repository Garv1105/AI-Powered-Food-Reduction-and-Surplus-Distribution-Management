import re

with open('frontend/src/app/processing-unit/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix the mojibake thresholds
code = code.replace('A?A 82%', '\u2265 82%')
code = code.replace('A?A  15%', '\u2264 15%')
code = code.replace('A?A  3%', '\u2264 3%')
code = code.replace('A??T', '-')
code = code.replace('A,A', '|')

# New Scorecard component
scorecard_old = '''function Scorecard({
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
        <div className={p-2 rounded-lg }>
          <Icon size={16} className="text-white" />
        </div>
      </div>
      <p className="text-3xl font-mono font-bold text-accent-secondary">{value}</p>
      {sub && <p className="text-xs text-content-secondary mt-1">{sub}</p>}
    </div>
  );
}'''

scorecard_new = '''function Scorecard({
  label,
  value,
  sub,
  color,
  icon: Icon,
  progressPct,
  statusClass,
}: {
  label: string;
  value: string;
  sub?: string;
  color: string;
  icon: React.ElementType;
  progressPct?: number;
  statusClass?: string;
}) {
  return (
    <div className="bg-ink-surface rounded-sm p-5 border border-ink-raised shadow-none flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between mb-4">
          <p className="font-mono text-[10px] uppercase tracking-widest text-content-secondary">{label}</p>
          <Icon size={16} className="text-content-secondary opacity-50" />
        </div>
        <p className="text-3xl font-mono font-bold text-accent-secondary tabular-nums tracking-tight">{value}</p>
      </div>
      <div className="mt-4">
        {progressPct !== undefined && (
          <div className="h-0.5 bg-ink-raised rounded-full overflow-hidden mb-1.5 w-full">
            <div 
              className={h-full transition-all }
              style={{ width: ${Math.min(100, progressPct)}% }}
            />
          </div>
        )}
        {sub && <p className="text-[10px] font-mono tracking-widest uppercase text-content-secondary">{sub}</p>}
      </div>
    </div>
  );
}'''

code = code.replace(scorecard_old, scorecard_new)

# Now fix the usage of Scorecard
yield_old = '''<Scorecard
              label="Avg Process Yield"
              value={fmt(agg?.avg_process_yield_pct, 1, '%')}
              sub="Threshold: \\u2265 82%"
              color={
                (agg?.avg_process_yield_pct ?? 0) >= 82
                  ? 'bg-teal'
                  : 'bg-red-500'
              }
              icon={TrendingUp}
            />'''

yield_new = '''<Scorecard
              label="Avg Process Yield"
              value={fmt(agg?.avg_process_yield_pct, 1, '%')}
              sub="Threshold: \\u2265 82%"
              color=""
              icon={TrendingUp}
              progressPct={Math.min(100, ((agg?.avg_process_yield_pct ?? 0) / 100) * 100)}
              statusClass={(agg?.avg_process_yield_pct ?? 0) >= 82 ? 'bg-status-success' : 'bg-status-critical'}
            />'''
code = code.replace(yield_old, yield_new)

downtime_old = '''<Scorecard
              label="Avg Downtime"
              value={fmt(agg?.avg_downtime_pct, 1, '%')}
              sub="Threshold: \\u2264 15%"
              color={
                (agg?.avg_downtime_pct ?? 99) <= 15
                  ? 'bg-teal'
                  : 'bg-red-500'
              }
              icon={TrendingDown}
            />'''

downtime_new = '''<Scorecard
              label="Avg Downtime"
              value={fmt(agg?.avg_downtime_pct, 1, '%')}
              sub="Threshold: \\u2264 15%"
              color=""
              icon={TrendingDown}
              progressPct={Math.min(100, ((agg?.avg_downtime_pct ?? 0) / 15) * 100)}
              statusClass={(agg?.avg_downtime_pct ?? 99) <= 15 ? 'bg-status-success' : 'bg-status-critical'}
            />'''
code = code.replace(downtime_old, downtime_new)

energy_old = '''<Scorecard
              label="Energy Intensity"
              value={fmt(agg?.period_energy_intensity_kwh_per_kg, 3, ' kWh/kg')}
              sub="SUM(kWh) / SUM(good output)"
              color="bg-blue-500"
              icon={Zap}
            />'''
energy_new = '''<Scorecard
              label="Energy Intensity"
              value={fmt(agg?.period_energy_intensity_kwh_per_kg, 3, ' kWh/kg')}
              sub="SUM(kWh) / SUM(good output)"
              color=""
              icon={Zap}
              progressPct={50}
              statusClass="bg-accent-secondary"
            />'''
code = code.replace(energy_old, energy_new)

rej_old = '''<Scorecard
              label="Avg Rejection Rate"
              value={fmt(agg?.avg_rejection_pct, 2, '%')}
              sub="Threshold: \\u2264 3%"
              color={
                (agg?.avg_rejection_pct ?? 99) <= 3
                  ? 'bg-teal'
                  : 'bg-red-500'
              }
              icon={AlertTriangle}
            />'''
rej_new = '''<Scorecard
              label="Avg Rejection Rate"
              value={fmt(agg?.avg_rejection_pct, 2, '%')}
              sub="Threshold: \\u2264 3%"
              color=""
              icon={AlertTriangle}
              progressPct={Math.min(100, ((agg?.avg_rejection_pct ?? 0) / 3) * 100)}
              statusClass={(agg?.avg_rejection_pct ?? 99) <= 3 ? 'bg-status-success' : 'bg-status-critical'}
            />'''
code = code.replace(rej_old, rej_new)

with open('frontend/src/app/processing-unit/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('Done fixing Scorecards')
