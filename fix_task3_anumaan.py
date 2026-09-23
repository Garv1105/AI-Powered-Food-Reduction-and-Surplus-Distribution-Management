"""
TASK 3: Fix Anumaan page dark theme
Target the specific light-theme strings identified in the file read.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/app/anumaan/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

original = code

# ============================================================
# 1. DocketLabel: steel color #4A5568 -> content-secondary
# ============================================================
code = code.replace(
    "style={{ color: '#4A5568', fontFamily: \"var(--font-sans), sans-serif\" }}",
    "style={{ color: '#9AA3B2', fontFamily: \"var(--font-sans), sans-serif\" }}"
)

# ============================================================
# 2. DocketInput: border '#E8E0D0' -> '#3A4255' (dark raised border)
# ============================================================
code = code.replace(
    "border: '1px solid #E8E0D0',\n        borderRadius: '3px',\n        padding: '7px 10px',\n        fontSize: '13px',\n        fontFamily: \"var(--font-mono), monospace\",\n        color: '#F2F0EA',\n        outline: 'none',\n        ...props.style,",
    "border: '1px solid #3A4255',\n        borderRadius: '3px',\n        padding: '7px 10px',\n        fontSize: '13px',\n        fontFamily: \"var(--font-mono), monospace\",\n        color: '#F2F0EA',\n        background: '#232B38',\n        outline: 'none',\n        ...props.style,"
)

# ============================================================
# 3. DocketSelect: border '#E8E0D0' -> '#3A4255'
# ============================================================
code = code.replace(
    "border: '1px solid #E8E0D0',\n        borderRadius: '3px',\n        padding: '7px 10px',\n        fontSize: '13px',\n        fontFamily: \"var(--font-mono), monospace\",\n        color: '#F2F0EA',\n        outline: 'none',\n        cursor: 'pointer',\n        appearance: 'none',",
    "border: '1px solid #3A4255',\n        borderRadius: '3px',\n        padding: '7px 10px',\n        fontSize: '13px',\n        fontFamily: \"var(--font-mono), monospace\",\n        color: '#F2F0EA',\n        background: '#232B38',\n        outline: 'none',\n        cursor: 'pointer',\n        appearance: 'none',"
)

# ============================================================
# 4. Toggle: inactive color '#4A5568' -> '#9AA3B2'
# ============================================================
code = code.replace(
    "color: value === 1 ? '#F2F0EA' : '#4A5568',",
    "color: value === 1 ? '#F2F0EA' : '#9AA3B2',"
)

# ============================================================
# 5. Rule divider: border '#E8E0D0' -> '#3A4255'
# ============================================================
code = code.replace(
    "{ borderTop: '1px solid #E8E0D0', margin: '20px 0' }",
    "{ borderTop: '1px solid #3A4255', margin: '20px 0' }"
)

# ============================================================
# 6. Page header border bottom: '#E8E0D0' -> '#3A4255'
# ============================================================
code = code.replace(
    "borderBottom: '1px solid #E8E0D0',\n          padding: '20px 32px',",
    "borderBottom: '1px solid #3A4255',\n          padding: '20px 32px',"
)

# ============================================================
# 7. Page header background: '#1B212B' is correct, keep it
# But also fix the subtitle text color '#4A5568' -> '#9AA3B2'
# ============================================================
code = code.replace(
    "fontSize: '13px',\n              color: '#4A5568',\n              marginLeft: '12px',",
    "fontSize: '13px',\n              color: '#9AA3B2',\n              marginLeft: '12px',"
)

# ============================================================
# 8. Load sample button border '#E8E0D0' -> '#3A4255' and color '#4A5568' -> '#9AA3B2'
# ============================================================
code = code.replace(
    "color: '#4A5568',\n              background: 'transparent',\n              border: '1px solid #E8E0D0',",
    "color: '#9AA3B2',\n              background: 'transparent',\n              border: '1px solid #3A4255',"
)

# ============================================================
# 9. Form body: border right '#E8E0D0' -> '#3A4255'
# ============================================================
code = code.replace(
    "borderRight: '1px solid #E8E0D0',",
    "borderRight: '1px solid #3A4255',"
)

# ============================================================
# 10. Docket container: border '#D5CCBC' -> '#3A4255'
# ============================================================
code = code.replace(
    "border: '1px solid #D5CCBC',",
    "border: '1px solid #3A4255',"
)

# ============================================================
# 11. KDS right panel: background when no result should be '#14181F' (ink-base)
# But result state background '#F2F0EA' should become dark too
# ============================================================
code = code.replace(
    "background: result ? '#F2F0EA' : '#14181F',",
    "background: '#1B212B',"
)

# ============================================================
# 12. The result number color was '#14181F' (dark text on light bg)
# Now it should be '#E8A33D' (accent primary) on dark bg
# ============================================================
code = code.replace(
    "fontSize: '80px',\n                    fontWeight: 600,\n                    color: '#14181F',",
    "fontSize: '80px',\n                    fontWeight: 600,\n                    color: '#E8A33D',"
)

# ============================================================
# 13. Recommended production number same fix
# ============================================================
code = code.replace(
    "fontSize: '28px',\n                      fontWeight: 600,\n                      color: '#14181F',",
    "fontSize: '28px',\n                      fontWeight: 600,\n                      color: '#F2F0EA',"
)

# ============================================================
# 14. Result section border separator '#2C2521' -> '#3A4255'
# ============================================================
code = code.replace("'1px solid #2C2521'", "'1px solid #3A4255'")

# ============================================================
# 15. apiError box: light bg '#FEF2F0' and border '#F5C6B8' -> dark equivalents
# ============================================================
code = code.replace(
    "background: '#FEF2F0',\n                    border: '1px solid #F5C6B8',\n                    borderRadius: '3px',\n                    color: '#E8A33D',",
    "background: 'rgba(217,86,74,0.1)',\n                    border: '1px solid rgba(217,86,74,0.3)',\n                    borderRadius: '3px',\n                    color: '#D9564A',"
)

changed = sum(1 for a, b in zip(original, code) if a != b)
if code == original:
    print("WARNING: No changes were made. Check string matching.")
else:
    print(f"Made changes (approx {changed} chars changed)")

with open('frontend/src/app/anumaan/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print("Task 3 done: anumaan/page.tsx dark theme fixed")
