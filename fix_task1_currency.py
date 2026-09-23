"""
TASK 1: Fix currency symbol bug in processing-unit/page.tsx
"""
import re

with open('frontend/src/app/processing-unit/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

rupee = '\u20B9'
dash = '\u2014'
nbsp = '\u00A0'

# Replace the entire fmtINR function using regex
pattern = r'function fmtINR\(n: number \| null \| undefined\) \{[^}]+\}'
replacement = (
    "function fmtINR(n: number | null | undefined) {\n"
    "  if (n == null) return '" + dash + "';\n"
    "  return '" + rupee + nbsp + "' + n.toLocaleString('en-IN', { maximumFractionDigits: 0 });\n"
    "}"
)
new_code = re.sub(pattern, replacement, code, flags=re.DOTALL)
if new_code != code:
    code = new_code
    print("Replaced fmtINR function")
else:
    print("WARNING: fmtINR not found with expected pattern, trying to find it")
    idx = code.find('fmtINR')
    print(f"  fmtINR found at index: {idx}")
    print(f"  Context: {repr(code[idx:idx+200])}")

# Replace the fmt function null return
pattern2 = r'function fmt\(n: number \| null \| undefined, decimals = 1, suffix = \'\'\) \{[^}]+\}'
replacement2 = (
    "function fmt(n: number | null | undefined, decimals = 1, suffix = '') {\n"
    "  if (n == null) return '" + dash + "';\n"
    "  return `${n.toFixed(decimals)}${suffix}`;\n"
    "}"
)
new_code2 = re.sub(pattern2, replacement2, code, flags=re.DOTALL)
if new_code2 != code:
    code = new_code2
    print("Replaced fmt function null return")

# Fix the garbled rupee in flagged days section
# Pattern: garbled_chars{Math.abs(fd.daily_profit_inr ?? 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })} {profit/loss}
# Find the span with daily profit in flagged days and fix it
# We'll use a targeted replacement
old_profit_span = re.search(
    r'<span className=\{`text-xs font-medium.*?`\}>\s*[^<{]+\{Math\.abs\(fd\.daily_profit_inr',
    code,
    re.DOTALL
)
if old_profit_span:
    print(f"Found profit span context: {repr(code[old_profit_span.start():old_profit_span.end()+100])}")

# Simple targeted fix: replace any non-ASCII chars preceding Math.abs in JSX
# Find the exact pattern in the file
code = re.sub(
    r'>[^\x00-\x7F]+\{Math\.abs\(fd\.daily_profit_inr \?\? 0\)\.toLocaleString\(\'en-IN\', \{ maximumFractionDigits: 0 \}\)\} \{',
    ">{'" + rupee + nbsp + "' + Math.abs(fd.daily_profit_inr ?? 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })} {",
    code
)
print("Fixed flagged days profit span")

# Fix garbled threshold sub texts in Scorecard calls
# Pattern: sub="Threshold: GARBLED 82%"
code = re.sub(
    r'sub="Threshold: [^\x00-\x7F]+%[^\x00-\x7F]+ (\d+%)"',
    lambda m: f'sub="Threshold: {chr(8805)} {m.group(1)}"',
    code
)
code = re.sub(
    r'sub="Threshold: [^\x00-\x7F]+%[^\x00-\x7E ]+ (\d+%)"',
    lambda m: f'sub="Threshold: {chr(8804)} {m.group(1)}"',
    code
)

# Fix garbled in the period info line
code = re.sub(r'\{metrics\.date_range\.start\} [^\x00-\x7E]+\+ \{metrics\.date_range\.end\}', 
              '{metrics.date_range.start} \u2192 {metrics.date_range.end}', code)
code = re.sub(r'\{metrics\.days_with_data\} days\s*\n\s*with data', '{metrics.days_with_data} days with data', code)
code = re.sub(r'\} [^\x00-\x7E]+\{metrics\.days_with_data\}', '} \u2022 {metrics.days_with_data}', code)

# Fix header subtitle garbled chars
code = re.sub(r'Central Processing Unit [^\x00-\x7E]+[^\x00-\x7F]+ Maize/Pulse', 
              'Central Processing Unit \u2014 Maize/Pulse', code)

# Fix Flagged Days description garbled
code = re.sub(r'Yield [^\x00-\x7E]+ 82% [^\x00-\x7E]+ Downtime [^\x00-\x7E]+ 15% [^\x00-\x7E]+ Rejection [^\x00-\x7E]+ 3%',
              'Yield \u003c 82% \u2022 Downtime \u003e 15% \u2022 Rejection \u003e 3%', code)
# In JSX these should be &lt; &gt;
code = code.replace('Yield \u003c 82%', 'Yield &lt; 82%')
code = code.replace('Downtime \u003e 15%', 'Downtime &gt; 15%')
code = code.replace('Rejection \u003e 3%', 'Rejection &gt; 3%')

# Fix loading message garbled
code = re.sub(r'Loading[^\x00-\x7E]+\.\.\.</div>', 'Loading...</div>', code)

with open('frontend/src/app/processing-unit/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Task 1 done: processing-unit/page.tsx fixed")
