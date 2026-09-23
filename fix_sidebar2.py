import re

with open('frontend/src/components/layout/Sidebar.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Make sidebar even cleaner
code = code.replace("bg-ink-surface/80 backdrop-blur-xl border-r border-ink-raised", "glass-premium border-r border-white/5")

# Pill styling
code = code.replace("rounded-sm text-[11px]", "rounded-xl text-[12px]")
code = code.replace("rounded-sm z-[-1]", "rounded-xl z-[-1] shadow-[0_0_15px_rgba(232,163,61,0.15)] bg-ink-surface border-accent-primary/20")

with open('frontend/src/components/layout/Sidebar.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('Sidebar updated')
