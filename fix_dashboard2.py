import re

with open('frontend/src/app/dashboard/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Soften all cards
code = code.replace("rounded-sm", "rounded-3xl")
code = code.replace("bg-ink-surface/60 backdrop-blur-md", "glass-premium")
code = code.replace("bg-ink-surface/80 backdrop-blur-md", "glass-premium")
code = code.replace("border-ink-raised", "border-white/5")

# Enhance typography
code = code.replace("text-2xl font-mono font-bold text-accent-secondary", "text-4xl font-display font-bold glow-text-secondary text-accent-secondary tracking-tight")
code = code.replace("text-2xl font-mono font-bold text-status-success", "text-4xl font-display font-bold text-status-success tracking-tight drop-shadow-[0_0_15px_rgba(95,174,110,0.5)]")
code = code.replace("text-2xl font-mono font-bold text-content-primary", "text-4xl font-display font-bold text-content-primary tracking-tight")

# Header
code = code.replace("text-3xl font-display font-bold text-content-primary", "text-5xl font-display font-bold text-content-primary tracking-tighter drop-shadow-md")
code = code.replace("text-sm text-content-secondary mt-1", "text-sm text-content-secondary mt-2 tracking-widest uppercase")

with open('frontend/src/app/dashboard/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('Dashboard updated')
