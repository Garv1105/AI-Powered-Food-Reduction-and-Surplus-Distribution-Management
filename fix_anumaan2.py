import re

with open('frontend/src/app/anumaan/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Soften layout
code = code.replace("rounded-sm", "rounded-2xl")
code = code.replace("rgba(27,33,43,0.7)', backdropFilter: 'blur(12px)', WebkitBackdropFilter: 'blur(12px)',", "rgba(27, 33, 43, 0.4)', backdropFilter: 'blur(20px)', WebkitBackdropFilter: 'blur(20px)', border: '1px solid rgba(255, 255, 255, 0.05)', boxShadow: '0 4px 30px rgba(0, 0, 0, 0.1)',")
code = code.replace("border-l border-ink-raised", "border-l border-white/5")

# Massive text glows
code = code.replace('className="text-xl font-display font-bold uppercase tracking-widest text-content-primary mb-1 text-glow"', 'className="text-3xl font-display font-bold tracking-tighter text-content-primary mb-1 drop-shadow-[0_0_20px_rgba(255,255,255,0.3)]"')

# Button
code = code.replace('className={clsx(\n                    "relative w-full py-4 text-[13px] font-mono font-bold tracking-widest uppercase transition-all rounded-sm overflow-hidden",\n                    loading \n                      ? "bg-ink-raised text-content-secondary" \n                      : "bg-accent-primary text-ink-base hover:shadow-[0_0_20px_rgba(232,163,61,0.4)]"\n                  )}', 'className={clsx(\n                    "relative w-full py-5 text-[15px] font-display font-bold tracking-wide uppercase transition-all rounded-2xl overflow-hidden",\n                    loading \n                      ? "bg-ink-raised text-content-secondary" \n                      : "bg-accent-primary text-ink-base glow-button-primary"\n                  )}')

with open('frontend/src/app/anumaan/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('Anumaan updated')
