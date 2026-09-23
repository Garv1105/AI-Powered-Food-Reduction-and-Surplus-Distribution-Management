"""Fix the leftover regex artifacts in fmt/fmtINR and also fix the daily_profit span"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/app/processing-unit/page.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

rupee = '\u20B9'
dash = '\u2014'
nbsp = '\u00A0'

# Print lines 28-42 for debug
for i, line in enumerate(lines[27:42], start=28):
    print(f"{i}: {repr(line)}")
