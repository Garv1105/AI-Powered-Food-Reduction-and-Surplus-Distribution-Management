import re

with open('frontend/src/app/map/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix layout colors
code = code.replace("bg-white border-b border-slate-200", "bg-ink-base border-b border-ink-raised")
code = code.replace("text-navy", "text-content-primary")
code = code.replace("bg-teal text-white", "bg-accent-primary text-ink-base font-mono uppercase tracking-widest text-xs")
code = code.replace("text-2xl font-bold", "text-3xl font-display font-bold uppercase tracking-wide")
code = code.replace("bg-slate-50", "bg-ink-surface")
code = code.replace("border-slate-200", "border-ink-raised")
code = code.replace("text-slate-500", "text-content-secondary font-mono tracking-widest uppercase")
code = code.replace("font-bold text-navy", "font-mono font-bold text-accent-secondary text-lg")
code = code.replace("text-slate-400", "text-content-secondary")
code = code.replace("bg-navy/10 text-navy", "bg-ink-raised text-accent-secondary")
code = code.replace("bg-navy text-white", "bg-ink-raised text-content-primary")
code = code.replace("bg-teal/10 text-teal border border-teal/20", "bg-accent-secondary/10 text-accent-secondary border border-accent-secondary/20")
code = code.replace("text-slate-300", "text-ink-raised")

# The overlay sidebar
code = code.replace("bg-white rounded-xl shadow-lg border border-slate-200", "bg-ink-surface rounded-sm border border-ink-raised shadow-none")
code = code.replace("bg-navy text-white", "bg-ink-surface text-content-primary border-b border-ink-raised")
code = code.replace("font-bold", "font-display font-bold uppercase tracking-widest text-sm")
code = code.replace("border-slate-100", "border-ink-raised")
code = code.replace("hover:bg-slate-50", "hover:bg-ink-raised")
code = code.replace("text-sm text-navy", "font-display text-content-primary uppercase tracking-wide text-sm")
code = code.replace("text-teal bg-teal/10", "text-accent-primary bg-ink-raised font-mono border border-ink-raised")

with open('frontend/src/app/map/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
