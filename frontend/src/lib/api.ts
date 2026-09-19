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
  name: string;
  address: string;
  contact_name: string;
  food_preference: string;
  capacity_kg: number;
  distance_km: number;
  match_score: number;
  capacity_match: boolean;
  food_pref_match: boolean;
  lat: number;
  lng: number;
}

export interface Waypoint {
  lat: number;
  lng: number;
  label: string;
  type: string;
}

export interface RouteResponse {
  delivery_id: number;
  waypoints: Waypoint[];
  total_distance_km: number;
  eta_minutes: number;
  route_polyline: number[][];
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

const BASE_URL = 'http://localhost:8000';

async function fetchWithCheck(url: string, options?: RequestInit) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }
  return response.json();
}

export const api = {
  getForecast: (category?: string, daysAhead?: number): Promise<ForecastResponse> => {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (daysAhead) params.append('days_ahead', daysAhead.toString());
    const query = params.toString() ? `?${params.toString()}` : '';
    return fetchWithCheck(`${BASE_URL}/forecast${query}`);
  },

  getSurplus: (status?: string): Promise<SurplusEvent[]> => {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    const query = params.toString() ? `?${params.toString()}` : '';
    return fetchWithCheck(`${BASE_URL}/surplus${query}`);
  },

  getMatches: (surplusEventId: number): Promise<NGOMatch[]> => {
    return fetchWithCheck(`${BASE_URL}/match`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ surplus_event_id: surplusEventId }),
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
};
