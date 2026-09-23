import re

with open('frontend/src/app/reports/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Layouts
code = code.replace("bg-white p-5 rounded-xl shadow-sm border border-slate-100", "bg-ink-surface p-5 rounded-sm border border-ink-raised shadow-none")
code = code.replace("bg-white rounded-xl shadow-sm border border-slate-100", "bg-ink-surface rounded-sm border border-ink-raised shadow-none")
code = code.replace("bg-white rounded-xl p-5 shadow-sm border border-slate-100", "bg-ink-surface rounded-sm p-5 border border-ink-raised shadow-none")

# Colors
code = code.replace("text-navy", "text-content-primary")
code = code.replace("text-slate-500", "text-content-secondary")
code = code.replace("text-slate-400", "text-content-secondary")
code = code.replace("text-slate-700", "text-content-primary")
code = code.replace("border-slate-100", "border-ink-raised")
code = code.replace("border-slate-200", "border-ink-raised")
code = code.replace("bg-slate-100", "bg-ink-raised")
code = code.replace("bg-slate-50/50", "bg-ink-base/50")
code = code.replace("bg-slate-50", "bg-ink-base")
code = code.replace("bg-white", "bg-ink-surface")

# Specific elements
code = code.replace("text-2xl font-bold", "text-3xl font-display font-bold uppercase tracking-wide")
code = code.replace("font-bold text-content-primary", "font-display font-bold uppercase tracking-wide text-content-primary")
code = code.replace("text-sm font-semibold text-content-secondary", "font-mono text-xs uppercase tracking-widest text-content-secondary")
code = code.replace("text-2xl font-bold text-content-primary", "text-3xl font-mono font-bold text-accent-secondary")
code = code.replace("bg-teal/10 text-teal border-teal/20", "bg-accent-secondary/10 text-accent-secondary border-accent-secondary/20 font-mono tracking-widest")
code = code.replace("bg-ink-raised text-content-primary border-ink-raised", "bg-ink-raised text-content-secondary border-ink-raised font-mono tracking-widest")
code = code.replace("text-teal", "text-accent-secondary")
code = code.replace("text-green-600", "text-status-success")
code = code.replace("text-blue-600", "text-accent-primary")
code = code.replace("text-amber-500", "text-status-warning")
code = code.replace("text-amber-800", "text-status-warning")
code = code.replace("bg-amber-50 border border-amber-200", "bg-status-warning/10 border border-status-warning/20")
code = code.replace("bg-red-50 text-red-600", "bg-status-critical/10 text-status-critical border border-status-critical/20 font-mono")
code = code.replace("border-red-100", "border-status-critical/20")
code = code.replace("text-sm font-medium text-content-secondary", "font-mono text-xs text-content-secondary uppercase tracking-widest")

# Prose text
code = code.replace("prose prose-slate max-w-none text-content-primary", "max-w-none text-content-primary font-sans text-[15px] leading-8")

with open('frontend/src/app/reports/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
