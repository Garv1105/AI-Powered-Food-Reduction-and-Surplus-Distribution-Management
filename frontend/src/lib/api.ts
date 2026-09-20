export interface ForecastPoint {
  date: string;
  predicted_kg: number;
  confidence_lower: number;
  confidence_upper: number;
}

export interface ForecastResponse {
  kitchen_id: number;
  category: string;
  unit: string;
  generated_at: string;
  predictions: ForecastPoint[];
}

export interface SurplusEvent {
  id: number;
  kitchen_id: number;
  kitchen_name: string;
  category: string;
  is_vegetarian: boolean;
  quantity_kg: number;
  detected_at: string;
  expiry_at: string;
  rescue_window_hours: number;
  urgency_level: string;
  status: string;
}

export interface NGOMatch {
  ngo_id: number;
  ngo_name: string;
  contact_name: string;
  contact_phone: string;
  match_score: number;
  distance_km: number;
  eta_minutes: number;
  match_reason: string;
}

export interface Waypoint {
  lat: number;
  lng: number;
  label: string;
  type: string;
}

export interface RouteResponse {
  delivery_id?: number;
  waypoints: Waypoint[];
  total_distance_km: number;
  eta_minutes: number;
  route_polyline: number[][];
  route_geometry?: any;
}

export interface DailyStat {
  date: string;
  kg_rescued: number;
  kg_wasted: number;
  meals_served: number;
  co2_saved_kg: number;
}

export interface DashboardSummary {
  kg_rescued_today: number;
  kg_wasted_today: number;
  active_surplus_count: number;
  ngos_served_this_month: number;
  forecast_accuracy_pct: number;
  co2_saved_today_kg: number;
  cost_saved_today_inr: number;
  weekly_trend: DailyStat[];
}

// ---------------------------------------------------------------------------
// Anumaan — Demand Prediction
// ---------------------------------------------------------------------------

/** Frontend form state — camelCase */
export interface PredictDemandRequest {
  locationId: string;       // → location_id
  date: string;             // → date  (same)
  isHoliday: number;        // → is_holiday
  tempCelsius: number;      // → temp_celsius
  rainMm: number;           // → rain_mm
  localEvent: number;       // → local_event
  activePromotion: number;  // → active_promotion
  competitorPromo: number;  // → competitor_promo
  cpiIndex: number;         // → cpi_index
  onlineRating: number;     // → online_rating
  reservations: number;     // → reservations  (same)
  demandYesterday: number;  // → demand_yesterday
  demand7DaysAgo: number;   // → demand_7_days_ago
  demandMa7: number;        // → demand_ma7
}

/** Backend response — mirrors PredictDemandResponse Pydantic schema */
export interface PredictDemandResponse {
  predicted_customers: number;
  recommended_production: number | null;  // stub — always null for now
  expected_surplus: number | null;         // stub — always null for now
  location_id: string;
  date: string;
  derived_features: Record<string, number>;
}

const BASE_URL = 'http://localhost:8002';

async function fetchWithCheck(url: string, options?: RequestInit) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }
  return response.json();
}

export const api = {
  getForecast: async (kitchenId: string, startDate: string, daysAhead: number = 7): Promise<ForecastResponse> => {
    // Generate dates
    const dates: string[] = [];
    const start = new Date(startDate);
    for (let i = 0; i < daysAhead; i++) {
      const d = new Date(start);
      d.setDate(d.getDate() + i);
      dates.push(d.toISOString().split('T')[0]);
    }

    // Fetch predictions in parallel
    const promises = dates.map(date => {
      const params = new URLSearchParams({ kitchen_id: kitchenId, date: date });
      return fetchWithCheck(`${BASE_URL}/anumaan/forecast?${params.toString()}`);
    });

    const responses: PredictDemandResponse[] = await Promise.all(promises);

    // Map to old expected format for the chart
    const predictions: ForecastPoint[] = responses.map(res => {
      return {
        date: res.date,
        // The chart expects kg, we are returning customers. 
        // For demo purposes, let's just map customers to kg (e.g. 1 customer = 0.5kg) or just pass it as is.
        // Let's pass it as is and the chart can just show the raw number.
        predicted_kg: res.predicted_customers,
        confidence_lower: res.predicted_customers * 0.9,
        confidence_upper: res.predicted_customers * 1.1
      };
    });

    return {
      kitchen_id: 1,
      category: 'Overall Demand (Customers)',
      unit: 'customers',
      generated_at: new Date().toISOString(),
      predictions: predictions
    };
  },

  getSurplus: (status?: string): Promise<SurplusEvent[]> => {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    const query = params.toString() ? `?${params.toString()}` : '';
    return fetchWithCheck(`${BASE_URL}/surplus${query}`);
  },

  getMatches: (surplusEventId: number): Promise<NGOMatch[]> => {
    return fetchWithCheck(`${BASE_URL}/surplus/${surplusEventId}/matches`);
  },
  
  optimizeRoute: (kitchenId: number, deliveryIds: number[]): Promise<RouteResponse> => {
    return fetchWithCheck(`${BASE_URL}/route/optimize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ kitchen_id: kitchenId, delivery_ids: deliveryIds }),
    });
  },

  getRoute: (deliveryId?: number): Promise<RouteResponse> => {
    const params = new URLSearchParams();
    if (deliveryId) params.append('delivery_id', deliveryId.toString());
    const query = params.toString() ? `?${params.toString()}` : '';
    return fetchWithCheck(`${BASE_URL}/route${query}`);
  },

  getDashboardSummary: (): Promise<DashboardSummary> => {
    return fetchWithCheck(`${BASE_URL}/dashboard/summary`);
  },

  getProductionPlan: (kitchenId: string, date: string): Promise<any> => {
    return fetchWithCheck(`${BASE_URL}/production-plan/generate?kitchen_id=${kitchenId}&date=${date}`);
  },

  saveProductionPlan: (plan: any): Promise<any> => {
    return fetchWithCheck(`${BASE_URL}/production-plan/save`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(plan),
    });
  },

  /**
   * POST /anumaan/predict-demand
   *
   * Explicit camelCase → snake_case mapping (matches PredictDemandRequest Pydantic schema exactly):
   *   locationId       → location_id
   *   date             → date
   *   isHoliday        → is_holiday
   *   tempCelsius      → temp_celsius
   *   rainMm           → rain_mm
   *   localEvent       → local_event
   *   activePromotion  → active_promotion
   *   competitorPromo  → competitor_promo
   *   cpiIndex         → cpi_index
   *   onlineRating     → online_rating
   *   reservations     → reservations
   *   demandYesterday  → demand_yesterday
   *   demand7DaysAgo   → demand_7_days_ago
   *   demandMa7        → demand_ma7
   */
  predictDemand: (req: PredictDemandRequest): Promise<PredictDemandResponse> => {
    const body = {
      location_id:       req.locationId,
      date:              req.date,
      is_holiday:        req.isHoliday,
      temp_celsius:      req.tempCelsius,
      rain_mm:           req.rainMm,
      local_event:       req.localEvent,
      active_promotion:  req.activePromotion,
      competitor_promo:  req.competitorPromo,
      cpi_index:         req.cpiIndex,
      online_rating:     req.onlineRating,
      reservations:      req.reservations,
      demand_yesterday:  req.demandYesterday,
      demand_7_days_ago: req.demand7DaysAgo,
      demand_ma7:        req.demandMa7,
    };
    return fetchWithCheck(`${BASE_URL}/anumaan/predict-demand`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
  },
};

