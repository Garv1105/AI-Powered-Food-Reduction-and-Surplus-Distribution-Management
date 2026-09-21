'use client';

import { ForecastPoint } from '@/lib/api';
import { ResponsiveContainer, ComposedChart, Line, Area, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from 'recharts';

interface ForecastChartProps {
  data: ForecastPoint[];
  category: string;
}

export default function ForecastChart({ data, category }: ForecastChartProps) {
  const formattedData = data.map((d) => {
    const date = new Date(d.date);
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    return {
      ...d,
      displayDate: `${monthNames[date.getMonth()]} ${String(date.getDate()).padStart(2, '0')}`
    };
  });

  if (!data || data.length === 0) {
    return <div className="p-4 bg-red-50 text-red-600 rounded">No forecast data available from API.</div>;
  }

  return (
    <div className="w-full h-full flex flex-col">
      <h3 className="text-lg font-bold text-navy mb-4 capitalize">Demand Forecast — {category}</h3>
      <div style={{ height: 350, width: '100%' }}>
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={formattedData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
            <XAxis dataKey="displayDate" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
            <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(val) => `${val} kg`} />
            <Tooltip 
              contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
              formatter={(value: number, name: string) => [
                `${value.toFixed(1)} kg`, 
                name === 'predicted_kg' ? 'Predicted' : name === 'confidence_upper' ? 'Upper Bound' : 'Lower Bound'
              ]}
            />
            <Legend verticalAlign="top" height={36} iconType="circle" />
            
            <Line 
              type="monotone" 
              dataKey="confidence_upper" 
              stroke="#99f6e4" 
              strokeWidth={1}
              strokeDasharray="3 3"
              dot={false} 
              name="Upper Bound" 
            />
            
            <Line 
              type="monotone" 
              dataKey="confidence_lower" 
              stroke="#99f6e4" 
              strokeWidth={1}
              strokeDasharray="3 3"
              dot={false} 
              name="Lower Bound" 
            />
            
            <Line 
              type="monotone" 
              dataKey="predicted_kg" 
              stroke="#0d9488" 
              strokeWidth={2} 
              dot={false} 
              name="Predicted Demand (kg)" 
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
