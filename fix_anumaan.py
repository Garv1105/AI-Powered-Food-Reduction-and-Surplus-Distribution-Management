import re

with open('frontend/src/app/anumaan/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("background: '#F4EFE6'", "background: 'transparent'")
code = code.replace("'#F9F7F4'", "'#1B212B'")
code = code.replace("'#D5CCBC'", "'#232B38'")
code = code.replace("'#E8E0D0'", "'#232B38'")
code = code.replace("'#1C1917'", "'#F2F0EA'")
code = code.replace("'#5C4F3E'", "'#F2F0EA'")
code = code.replace("'#8B7355'", "'#9AA3B2'")
code = code.replace("'#8B9AAA'", "'#9AA3B2'")
code = code.replace("'#C2440E'", "'#E8A33D'")
code = code.replace("borderTop: '1px dashed #E8E0D0'", "borderTop: '1px dashed #232B38'")
code = code.replace("'#F4EFE6'", "'#14181F'")
code = code.replace("'IBM Plex Mono', monospace", "var(--font-mono), monospace")
code = code.replace("'IBM Plex Sans', sans-serif", "var(--font-sans), sans-serif")
code = code.replace("border: '1px solid #C2440E'", "border: '1px solid #E8A33D'")
code = code.replace("boxShadow: '0 0 0 1px #C2440E'", "boxShadow: '0 0 0 1px #E8A33D'")
code = code.replace("color: '#F4EFE6'", "color: '#F2F0EA'")
# result panel right background logic
code = code.replace("background: result ? '#1C1917' : '#F4EFE6'", "background: result ? '#1B212B' : '#14181F'")
code = code.replace("'#2C2521'", "'#232B38'")

with open('frontend/src/app/anumaan/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
