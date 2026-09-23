import re

with open('frontend/src/app/map/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix header
code = code.replace('>Nearby NGOs</h3>', '>NGO Dispatch Queue</h3>')

# Add NEAREST tag to the first element
old_map = '{ngos.map(ngo => ('
new_map = '{ngos.map((ngo, index) => ('

old_div = '<div key={ngo.ngo_id} className="p-3 border-b border-ink-raised last:border-0 hover:bg-ink-raised transition-colors">'
new_div = '''<div key={ngo.ngo_id} className={p-3 border-b border-ink-raised last:border-0 transition-colors }>
                {index === 0 && (
                  <div className="mb-2 inline-flex items-center gap-1 text-[9px] font-mono font-bold uppercase tracking-widest text-accent-secondary bg-accent-secondary/10 px-1.5 py-0.5 rounded-sm">
                    <span className="w-1.5 h-1.5 rounded-full bg-accent-secondary animate-pulse" />
                    Optimal Match
                  </div>
                )}'''

code = code.replace(old_map, new_map)
code = code.replace(old_div, new_div)

with open('frontend/src/app/map/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('Done fixing Map NGO list')
