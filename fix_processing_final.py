with open('frontend/src/app/processing-unit/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix fmtINR function - the rupee sign rupee U+20B9 + non-breaking-space is there but the closing is broken
# Replace the entire fmtINR function
old_fmtINR = '''function fmtINR(n: number | null | undefined) {
  if (n == null) return '\u2014';
  return '\u20b9\xa0' + n.toLocaleString('en-IN', { maximumFractionDigits: 0 });
})};\n}'''

new_fmtINR = '''function fmtINR(n: number | null | undefined) {
  if (n == null) return '\u2014';
  return '\u20b9' + n.toLocaleString('en-IN', { maximumFractionDigits: 0 });
}'''

code = code.replace(old_fmtINR, new_fmtINR)

# Fix garbled rupee in flagged days
code = code.replace('\xe2\x82\xb9', '\u20b9')
# The HTML entity version that may appear
code = code.replace('â\x82¹', '\u20b9')
# Specific garbled version seen in source
code = code.replace('â‚¹', '\u20b9')

# Also fix flagged days profit colors to use design tokens
code = code.replace('text-emerald-600', 'text-status-success')
code = code.replace('text-rose-600', 'text-status-critical')

# Fix amber-600 to accent tokens
code = code.replace('text-amber-600', 'text-status-warning')

with open('frontend/src/app/processing-unit/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('Done fixing processing unit')
