import re

with open('frontend/src/app/processing-unit/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("bg-white text-slate-600 border border-slate-200", "bg-ink-surface text-content-secondary border border-ink-raised")
code = code.replace("bg-white rounded-xl p-4 shadow-sm border border-ink-raised", "bg-ink-surface rounded-sm p-4 border border-ink-raised shadow-none")

with open('frontend/src/app/processing-unit/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
