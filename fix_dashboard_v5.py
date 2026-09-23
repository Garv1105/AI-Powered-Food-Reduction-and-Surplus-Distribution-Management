import re

with open('frontend/src/app/dashboard/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix state initialization
code = code.replace("const [productionPlan, setProductionPlan] = useState<any[]>([]);", "const [productionPlan, setProductionPlan] = useState<any | null>(null);")

# Fix map block
old_map = '''                  {productionPlan.map((cat) => (
                    <tr key={cat.category} className="hover:bg-white/5 transition-colors">
                      <td className="px-5 py-4 font-medium text-content-primary">{cat.category}</td>
                      <td className="px-5 py-4 text-content-secondary">{cat.forecast_qty} {cat.unit}</td>
                      <td className="px-5 py-4 text-content-secondary">
                        <span className="bg-black/30 px-2 py-1 rounded-md border border-white/5">
                          {(cat.buffer_pct * 100).toFixed(1)}%
                        </span>
                      </td>
                      <td className="px-5 py-4 font-bold text-accent-secondary tracking-tight text-base">
                        {cat.recommended_production_qty} <span className="text-xs opacity-70">{cat.unit}</span>
                      </td>
                    </tr>
                  ))}'''

new_map = '''                  {productionPlan?.categories?.map((cat: any) => (
                    <tr key={cat.category_id} className="hover:bg-white/5 transition-colors">
                      <td className="px-5 py-4 font-medium text-content-primary capitalize">{cat.category_name}</td>
                      <td className="px-5 py-4 text-content-secondary">{cat.predicted_qty} {cat.unit}</td>
                      <td className="px-5 py-4 text-content-secondary">
                        <span className="bg-black/30 px-2 py-1 rounded-md border border-white/5" title={cat.buffer_reasoning}>
                          {(cat.buffer_pct * 100).toFixed(1)}%
                        </span>
                      </td>
                      <td className="px-5 py-4 font-bold text-accent-secondary tracking-tight text-base">
                        {cat.recommended_production_qty} <span className="text-xs opacity-70">{cat.unit}</span>
                      </td>
                    </tr>
                  ))}'''

code = code.replace(old_map, new_map)

with open('frontend/src/app/dashboard/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('Dashboard updated to fix mapping error')
