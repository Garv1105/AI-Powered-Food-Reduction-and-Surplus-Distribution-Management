import re

with open('frontend/src/app/anumaan/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace button classes
code = re.sub(r'className=\{clsx\([^)]+\)\}',
              r'''className={clsx(
                    "relative w-full py-5 text-[15px] font-display font-bold tracking-wide uppercase transition-all rounded-2xl overflow-hidden",
                    loading 
                      ? "bg-ink-raised text-content-secondary" 
                      : "bg-accent-primary text-ink-base glow-button-primary"
                  )}''', code)

with open('frontend/src/app/anumaan/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('Anumaan updated again')
