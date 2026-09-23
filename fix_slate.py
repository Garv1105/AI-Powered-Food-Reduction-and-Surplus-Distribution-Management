import re

with open('frontend/src/app/dashboard/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("bg-slate-200", "bg-ink-raised")

with open('frontend/src/app/dashboard/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

with open('frontend/src/app/map/page.tsx', 'r', encoding='utf-8') as f:
    code2 = f.read()

code2 = code2.replace("bg-slate-100", "bg-ink-base")
code2 = code2.replace("text-slate-500", "text-content-secondary")

with open('frontend/src/app/map/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code2)

print('Fixed slate')
