'use client';

import { useState, useEffect, useRef } from 'react';
import { api, PredictDemandRequest, PredictDemandResponse } from '@/lib/api';
import {
  BrainCircuit, Loader2, ChevronDown, ChevronUp,
  Thermometer, CloudRain, CalendarDays, MapPin,
  Star, Users, TrendingUp, ShoppingCart, Zap, AlertCircle
} from 'lucide-react';
import clsx from 'clsx';

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const LOCATIONS = Array.from({ length: 26 }, (_, i) => `Loc_${i + 1}`);

// Tomorrow's date in YYYY-MM-DD
function tomorrowStr() {
  const d = new Date();
  d.setDate(d.getDate() + 1);
  return d.toISOString().split('T')[0];
}

const EXAMPLE: PredictDemandRequest = {
  locationId: 'Loc_3',
  date: '2026-09-22',
  isHoliday: 0,
  tempCelsius: 24.5,
  rainMm: 0,
  localEvent: 0,
  activePromotion: 1,
  competitorPromo: 0,
  cpiIndex: 142.3,
  onlineRating: 4.2,
  reservations: 125,
  demandYesterday: 410,
  demand7DaysAgo: 395,
  demandMa7: 402.7,
};

// ---------------------------------------------------------------------------
// Animated counter
// ---------------------------------------------------------------------------

function AnimatedNumber({ target }: { target: number }) {
  const [display, setDisplay] = useState(0);
  const ref = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    const start = 0;
    const duration = 900;
    const steps = 40;
    const increment = (target - start) / steps;
    let current = start;
    let step = 0;
    ref.current = setInterval(() => {
      step++;
      current += increment;
      if (step >= steps) {
        setDisplay(target);
        clearInterval(ref.current!);
      } else {
        setDisplay(Math.round(current));
      }
    }, duration / steps);
    return () => clearInterval(ref.current!);
  }, [target]);

  return <>{display.toLocaleString()}</>;
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function Toggle({
  label, value, onChange
}: { label: string; value: number; onChange: (v: number) => void }) {
  return (
    <button
      type="button"
      onClick={() => onChange(value === 1 ? 0 : 1)}
      className={clsx(
        'flex items-center justify-between w-full px-3 py-2.5 rounded-lg border text-sm font-medium transition-all',
        value === 1
          ? 'bg-teal-500/10 border-teal-500/40 text-teal-700'
          : 'bg-slate-50 border-slate-200 text-slate-500'
      )}
    >
      <span>{label}</span>
      <span className={clsx(
        'w-9 h-5 rounded-full relative transition-colors',
        value === 1 ? 'bg-teal-500' : 'bg-slate-300'
      )}>
        <span className={clsx(
          'absolute top-0.5 w-4 h-4 bg-white rounded-full shadow transition-transform',
          value === 1 ? 'translate-x-4' : 'translate-x-0.5'
        )} />
      </span>
    </button>
  );
}

function FieldError({ msg }: { msg?: string }) {
  if (!msg) return null;
  return <p className="text-xs text-red-500 mt-1 flex items-center gap-1"><AlertCircle size={11} />{msg}</p>;
}

// ---------------------------------------------------------------------------
// Main page
// ---------------------------------------------------------------------------

type FormErrors = Partial<Record<keyof PredictDemandRequest, string>>;

function validate(f: PredictDemandRequest): FormErrors {
  const err: FormErrors = {};
  if (!f.locationId) err.locationId = 'Required';
  if (!f.date) err.date = 'Required';
  if (f.tempCelsius < -20 || f.tempCelsius > 60)
    err.tempCelsius = 'Must be between -20 and 60 °C';
  if (f.rainMm < 0)
    err.rainMm = 'Must be ≥ 0';
  if (f.cpiIndex <= 0)
    err.cpiIndex = 'Must be > 0';
  if (f.onlineRating < 1 || f.onlineRating > 5)
    err.onlineRating = 'Must be between 1.0 and 5.0';
  if (f.reservations < 0)
    err.reservations = 'Must be ≥ 0';
  if (f.demandYesterday < 0)
    err.demandYesterday = 'Must be ≥ 0';
  if (f.demand7DaysAgo < 0)
    err.demand7DaysAgo = 'Must be ≥ 0';
  if (f.demandMa7 < 0)
    err.demandMa7 = 'Must be ≥ 0';
  return err;
}

export default function AnumaanPage() {
  const [form, setForm] = useState<PredictDemandRequest>({
    locationId: 'Loc_1',
    date: tomorrowStr(),
    isHoliday: 0,
    tempCelsius: 22,
    rainMm: 0,
    localEvent: 0,
    activePromotion: 0,
    competitorPromo: 0,
    cpiIndex: 105,
    onlineRating: 4.0,
    reservations: 80,
    demandYesterday: 400,
    demand7DaysAgo: 390,
    demandMa7: 395,
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);
  const [result, setResult] = useState<PredictDemandResponse | null>(null);
  const [showFeatures, setShowFeatures] = useState(false);

  function setField<K extends keyof PredictDemandRequest>(key: K, value: PredictDemandRequest[K]) {
    setForm(prev => ({ ...prev, [key]: value }));
    setErrors(prev => ({ ...prev, [key]: undefined }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const errs = validate(form);
    if (Object.keys(errs).length > 0) { setErrors(errs); return; }
    setLoading(true);
    setApiError(null);
    setResult(null);
    try {
      const res = await api.predictDemand(form);
      setResult(res);
    } catch (err: any) {
      setApiError(err.message ?? 'Prediction failed');
    } finally {
      setLoading(false);
    }
  }

  function loadExample() {
    setForm(EXAMPLE);
    setErrors({});
    setResult(null);
  }

  // Gauge: typical range 200–700, clamp result
  const gaugeMax = 700;
  const gaugePct = result ? Math.min(100, (result.predicted_customers / gaugeMax) * 100) : 0;
  const gaugeColor = result
    ? result.predicted_customers > 500 ? '#ef4444'
      : result.predicted_customers > 350 ? '#f59e0b'
      : '#0d9488'
    : '#0d9488';

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-teal-50/30 p-8">
      {/* Header */}
      <div className="mb-8 flex items-start justify-between">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <div className="w-10 h-10 bg-teal-500 rounded-xl flex items-center justify-center shadow-lg">
              <BrainCircuit size={20} className="text-white" />
            </div>
            <h1 className="text-2xl font-bold text-slate-800">Anumaan</h1>
          </div>
          <p className="text-slate-500 ml-13">AI-powered customer demand forecasting for kitchen managers</p>
        </div>
        <button
          type="button"
          onClick={loadExample}
          className="px-4 py-2 text-sm font-medium bg-white border border-slate-200 text-teal-600 rounded-lg hover:bg-teal-50 hover:border-teal-300 transition-all shadow-sm flex items-center gap-2"
        >
          <Zap size={14} />
          Load example inputs
        </button>
      </div>

      <div className="grid grid-cols-5 gap-8 items-start">
        {/* ------------------------------------------------------------------ */}
        {/* LEFT — Form (3 cols)                                                */}
        {/* ------------------------------------------------------------------ */}
        <form onSubmit={handleSubmit} className="col-span-3 space-y-5">

          {/* Location & Date */}
          <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 space-y-4">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-2">
              <MapPin size={14} />Identity
            </h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">Location</label>
                <select
                  id="anumaan-location"
                  value={form.locationId}
                  onChange={e => setField('locationId', e.target.value)}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent"
                >
                  {LOCATIONS.map(l => <option key={l} value={l}>{l}</option>)}
                </select>
                <FieldError msg={errors.locationId} />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5 flex items-center gap-1.5">
                  <CalendarDays size={13} />Prediction Date
                </label>
                <input
                  id="anumaan-date"
                  type="date"
                  value={form.date}
                  onChange={e => setField('date', e.target.value)}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-teal-400"
                />
                <FieldError msg={errors.date} />
              </div>
            </div>
          </div>

          {/* Weather */}
          <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 space-y-4">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-2">
              <Thermometer size={14} />Weather Forecast
            </h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">Temperature (°C)</label>
                <input
                  id="anumaan-temp"
                  type="number" step="0.1" min="-20" max="60"
                  value={form.tempCelsius}
                  onChange={e => setField('tempCelsius', parseFloat(e.target.value) || 0)}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400"
                />
                <FieldError msg={errors.tempCelsius} />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5 flex items-center gap-1">
                  <CloudRain size={13} />Rainfall (mm)
                </label>
                <input
                  id="anumaan-rain"
                  type="number" step="0.1" min="0"
                  value={form.rainMm}
                  onChange={e => setField('rainMm', parseFloat(e.target.value) || 0)}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400"
                />
                <FieldError msg={errors.rainMm} />
              </div>
            </div>
          </div>

          {/* Flags */}
          <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 space-y-4">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">Context Flags</h2>
            <div className="grid grid-cols-2 gap-3">
              <Toggle label="Public Holiday" value={form.isHoliday} onChange={v => setField('isHoliday', v)} />
              <Toggle label="Local Event" value={form.localEvent} onChange={v => setField('localEvent', v)} />
              <Toggle label="Active Promotion" value={form.activePromotion} onChange={v => setField('activePromotion', v)} />
              <Toggle label="Competitor Promo" value={form.competitorPromo} onChange={v => setField('competitorPromo', v)} />
            </div>
          </div>

          {/* Market */}
          <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 space-y-4">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-2">
              <TrendingUp size={14} />Market Signals
            </h2>
            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">CPI Index</label>
                <input
                  id="anumaan-cpi"
                  type="number" step="0.01" min="0.01"
                  value={form.cpiIndex}
                  onChange={e => setField('cpiIndex', parseFloat(e.target.value) || 0)}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400"
                />
                <FieldError msg={errors.cpiIndex} />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5 flex items-center gap-1">
                  <Star size={12} />Online Rating
                </label>
                <input
                  id="anumaan-rating"
                  type="number" step="0.1" min="1.0" max="5.0"
                  value={form.onlineRating}
                  onChange={e => setField('onlineRating', parseFloat(e.target.value) || 1)}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400"
                />
                <FieldError msg={errors.onlineRating} />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">Reservations</label>
                <input
                  id="anumaan-reservations"
                  type="number" step="1" min="0"
                  value={form.reservations}
                  onChange={e => setField('reservations', parseInt(e.target.value) || 0)}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400"
                />
                <FieldError msg={errors.reservations} />
              </div>
            </div>
          </div>

          {/* Lag Features */}
          <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 space-y-4">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-2">
              <Users size={14} />Historical Demand (same location)
            </h2>
            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">Yesterday</label>
                <input
                  id="anumaan-demand-yesterday"
                  type="number" step="1" min="0"
                  value={form.demandYesterday}
                  onChange={e => setField('demandYesterday', parseFloat(e.target.value) || 0)}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400"
                />
                <FieldError msg={errors.demandYesterday} />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">7 Days Ago</label>
                <input
                  id="anumaan-demand-7d"
                  type="number" step="1" min="0"
                  value={form.demand7DaysAgo}
                  onChange={e => setField('demand7DaysAgo', parseFloat(e.target.value) || 0)}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400"
                />
                <FieldError msg={errors.demand7DaysAgo} />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600 mb-1.5">7-Day Avg (MA7)</label>
                <input
                  id="anumaan-demand-ma7"
                  type="number" step="0.1" min="0"
                  value={form.demandMa7}
                  onChange={e => setField('demandMa7', parseFloat(e.target.value) || 0)}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400"
                />
                <FieldError msg={errors.demandMa7} />
              </div>
            </div>
          </div>

          {/* Submit */}
          <button
            id="anumaan-submit"
            type="submit"
            disabled={loading}
            className="w-full py-3.5 bg-teal-500 hover:bg-teal-600 disabled:bg-teal-300 text-white font-semibold rounded-xl shadow-md transition-all flex items-center justify-center gap-2 text-base"
          >
            {loading ? (
              <><Loader2 size={18} className="animate-spin" />Running Anumaan…</>
            ) : (
              <><BrainCircuit size={18} />Predict Demand</>
            )}
          </button>

          {apiError && (
            <div className="flex items-start gap-3 bg-red-50 border border-red-200 text-red-700 rounded-xl p-4 text-sm">
              <AlertCircle size={16} className="shrink-0 mt-0.5" />
              <span>{apiError}</span>
            </div>
          )}
        </form>

        {/* ------------------------------------------------------------------ */}
        {/* RIGHT — Results panel (2 cols)                                      */}
        {/* ------------------------------------------------------------------ */}
        <div className="col-span-2 sticky top-8 space-y-5">

          {!result && !loading && (
            <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-10 flex flex-col items-center justify-center text-center gap-4">
              <div className="w-16 h-16 bg-teal-50 rounded-2xl flex items-center justify-center">
                <BrainCircuit size={32} className="text-teal-400" />
              </div>
              <div>
                <p className="font-semibold text-slate-600">No prediction yet</p>
                <p className="text-sm text-slate-400 mt-1">Fill in the form and click<br />"Predict Demand" to run Anumaan.</p>
              </div>
            </div>
          )}

          {loading && (
            <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-10 flex flex-col items-center justify-center gap-4">
              <Loader2 size={40} className="text-teal-500 animate-spin" />
              <p className="text-slate-500 font-medium">Running Anumaan model…</p>
            </div>
          )}

          {result && !loading && (
            <>
              {/* Main result card */}
              <div className="bg-gradient-to-br from-teal-600 to-teal-700 rounded-2xl shadow-xl p-6 text-white">
                <p className="text-teal-200 text-sm font-medium mb-1">Predicted Customers</p>
                <p className="text-6xl font-black tracking-tight leading-none mb-1">
                  <AnimatedNumber target={result.predicted_customers} />
                </p>
                <p className="text-teal-200 text-sm">
                  {result.location_id} · {result.date}
                </p>

                {/* Gauge */}
                <div className="mt-5">
                  <div className="flex justify-between text-xs text-teal-200 mb-1.5">
                    <span>0</span><span>350</span><span>700+</span>
                  </div>
                  <div className="h-2.5 bg-teal-800/50 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-700"
                      style={{ width: `${gaugePct}%`, backgroundColor: gaugeColor }}
                    />
                  </div>
                  <p className="text-xs text-teal-200 mt-1.5">
                    {result.predicted_customers <= 350 ? '🟢 Low demand day' :
                     result.predicted_customers <= 500 ? '🟡 Moderate demand' : '🔴 High demand day'}
                  </p>
                </div>
              </div>

              {/* Production planning stub */}
              <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5">
                <div className="flex items-center gap-2 mb-3">
                  <ShoppingCart size={16} className="text-slate-400" />
                  <h3 className="text-sm font-semibold text-slate-600">Production Planning</h3>
                </div>
                {/* recommended_production is null — hide value, show coming-soon note */}
                {result.recommended_production !== null ? (
                  <p className="text-2xl font-bold text-slate-800">
                    {result.recommended_production.toLocaleString()} portions
                  </p>
                ) : (
                  <p className="text-sm text-slate-400 italic">
                    Coming soon — requires buffer % and inventory module.
                  </p>
                )}
                {result.expected_surplus !== null && (
                  <p className="text-xs text-slate-400 mt-1">
                    Expected surplus: {result.expected_surplus} portions
                  </p>
                )}
              </div>

              {/* Derived features accordion */}
              <div className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
                <button
                  type="button"
                  onClick={() => setShowFeatures(v => !v)}
                  className="w-full flex items-center justify-between px-5 py-4 text-sm font-semibold text-slate-600 hover:bg-slate-50 transition-colors"
                >
                  <span>Derived features used by model</span>
                  {showFeatures ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                </button>
                {showFeatures && (
                  <div className="border-t border-slate-100 px-5 py-4">
                    <div className="grid grid-cols-2 gap-x-6 gap-y-1.5">
                      {Object.entries(result.derived_features).map(([k, v]) => (
                        <div key={k} className="flex justify-between text-xs">
                          <span className="text-slate-400 font-mono">{k}</span>
                          <span className="text-slate-700 font-medium tabular-nums">
                            {typeof v === 'number' ? v.toFixed(4) : v}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
