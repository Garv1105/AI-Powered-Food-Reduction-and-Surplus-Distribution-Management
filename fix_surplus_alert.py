import re

with open('frontend/src/components/dashboard/SurplusAlertList.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Make it use SpotlightCard and better spacing
if "SpotlightCard" not in code:
    code = code.replace("import { SurplusEvent } from '@/lib/api';", "import { SurplusEvent } from '@/lib/api';\nimport SpotlightCard from '@/components/ui/SpotlightCard';")

code = code.replace('<div className="glass-premium p-6 rounded-3xl border border-white/5 shadow-lg shadow-black/20 flex flex-col h-full">', '<SpotlightCard className="p-8 shadow-2xl shadow-black/50 flex flex-col h-full">')
code = code.replace('</div>\n    </div>\n  );\n}', '</SpotlightCard>\n  );\n}')

# Update typography inside SurplusAlertList
code = code.replace('className="text-lg font-display text-content-primary uppercase tracking-wide flex items-center gap-2"', 'className="text-lg font-display text-content-primary uppercase tracking-wide flex items-center gap-3"')

code = code.replace('className="w-2 h-2 rounded-full bg-status-warning animate-pulse"', 'className="w-2 h-2 rounded-full bg-status-warning animate-pulse shadow-[0_0_10px_rgba(232,163,61,0.8)]"')

code = code.replace('className="bg-ink-surface/60 rounded-xl p-4 border border-ink-raised shadow-sm flex items-start justify-between"', 'className="bg-black/20 rounded-2xl p-5 border border-white/5 hover:bg-black/30 transition-colors flex items-start justify-between relative overflow-hidden group"')

with open('frontend/src/components/dashboard/SurplusAlertList.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('SurplusAlertList upgraded')
