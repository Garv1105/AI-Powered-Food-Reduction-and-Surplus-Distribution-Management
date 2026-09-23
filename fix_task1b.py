"""Fix leftover artifacts in processing-unit/page.tsx fmt functions + daily_profit span"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/app/processing-unit/page.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

rupee = '\u20B9'
dash = '\u2014'
nbsp = '\u00A0'

# Remove line 33 ('}${suffix}`;\n' - leftover fragment)
# Remove line 38 ('})}`;' becomes just '}' - it should be removed)
# After removal: line indices shift by 1 for each removed line
# Line 33 (index 32): '}${suffix}`;\n'  -> DELETE
# Line 38 (index 37): '})}`;'            -> DELETE (it's now index 36 after first deletion)

new_lines = []
for i, line in enumerate(lines):
    if i == 32 and line.strip() == '}${suffix}`;':
        # skip this artifact line
        print(f"Removed line {i+1}: {repr(line)}")
        continue
    if i == 37 and line.strip() == '})}`;':
        # skip this artifact line
        print(f"Removed line {i+1}: {repr(line)}")
        continue
    new_lines.append(line)

# Also fix the daily_profit span in flagged days
# Look for the line with Math.abs(fd.daily_profit_inr
full = ''.join(new_lines)

import re

# Fix the profit span display - it may now have proper ₹ or garbled
# Find the exact pattern in context
profit_pattern = re.compile(
    r'>\s*[\u20B9₹][^\S\n]?\{Math\.abs\(fd\.daily_profit_inr.*?\}\s*\{',
    re.DOTALL
)
if profit_pattern.search(full):
    print("Profit span already has proper rupee")
else:
    # Try to fix garbled prefix
    full = re.sub(
        r'>[^\x00-\x7F]+\{Math\.abs\(fd\.daily_profit_inr \?\? 0\)\.toLocaleString\(\'en-IN\', \{ maximumFractionDigits: 0 \}\)\} \{',
        ">{'" + rupee + nbsp + "' + Math.abs(fd.daily_profit_inr ?? 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })} {",
        full
    )
    print("Fixed profit span")

# Fix flagged days table divider (uses divide-slate-50 which is wrong)
full = full.replace('divide-slate-50', 'divide-ink-raised')
print("Fixed divide-slate-50 -> divide-ink-raised")

# Fix the emerald/rose classes to design token colors
full = full.replace('"text-emerald-600"', '"text-status-success"')
full = full.replace('"text-rose-600"', '"text-status-critical"')
print("Fixed emerald/rose colors to design tokens")

# Fix amber-600 color in flagged days root_cause span
full = full.replace('text-amber-600', 'text-status-warning')
print("Fixed amber-600 -> text-status-warning")

with open('frontend/src/app/processing-unit/page.tsx', 'w', encoding='utf-8') as f:
    f.writelines(full if isinstance(full, list) else [full])

print("\nTask 1 complete: processing-unit/page.tsx fully fixed")
