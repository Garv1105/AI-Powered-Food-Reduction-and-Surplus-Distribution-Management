import re

with open('frontend/src/app/processing-unit/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("bg-white rounded-xl p-5 shadow-sm border border-slate-100", "bg-ink-surface rounded-sm p-5 border border-ink-raised shadow-none")
code = code.replace("bg-white rounded-xl shadow-sm border border-slate-100", "bg-ink-surface rounded-sm border border-ink-raised shadow-none")
code = code.replace("bg-slate-50", "bg-ink-raised")
code = code.replace("border-slate-100", "border-ink-raised")
code = code.replace("border-slate-50", "border-ink-raised")

code = code.replace("text-navy", "text-content-primary")
code = code.replace("text-slate-500", "text-content-secondary")
code = code.replace("text-slate-400", "text-content-secondary")

code = code.replace("text-2xl font-bold text-content-primary", "text-3xl font-mono font-bold text-accent-secondary")
code = code.replace("text-sm text-content-secondary font-medium", "font-mono text-xs uppercase tracking-widest text-content-secondary")

code = code.replace("stroke=\"#e2e8f0\"", "stroke=\"#232B38\"")
code = code.replace("stroke=\"#94a3b8\"", "stroke=\"#9AA3B2\"")
code = code.replace("contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,.1)', fontSize: 12 }}", "contentStyle={{ backgroundColor: '#232B38', border: '1px solid #1B212B', borderRadius: '4px', color: '#F2F0EA', fontSize: 12 }} itemStyle={{ color: '#F2F0EA' }}")
code = code.replace("stroke=\"#ef4444\"", "stroke=\"#E8A33D\"")
code = code.replace("fill: '#ef4444'", "fill: '#E8A33D'")
code = code.replace("text-sm font-semibold text-content-primary", "font-display font-bold uppercase tracking-wide text-content-primary")

code = code.replace("bg-red-100 text-red-600", "bg-status-critical/10 text-status-critical border border-status-critical/20 font-mono")
code = code.replace("bg-red-50 text-red-600", "bg-status-critical/10 text-status-critical border border-status-critical/20 font-mono tracking-widest uppercase")
code = code.replace("hover:bg-ink-raised", "hover:bg-ink-raised transition-colors")

# Also need to fix Page title
code = code.replace("text-2xl font-bold text-content-primary", "text-3xl font-display font-bold text-content-primary tracking-wide uppercase")

with open('frontend/src/app/processing-unit/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
