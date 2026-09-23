import re

with open('frontend/src/app/anumaan/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix the KDS right panel container
code = code.replace("background: result ? '#F2F0EA' : '#14181F',", "background: 'transparent',")
code = code.replace("color: '#14181F',", "color: '#F2F0EA',")
code = code.replace("color: '#3A4255',", "color: '#F2F0EA',")
code = code.replace("borderBottom: '1px solid #E5E5E5'", "borderBottom: '1px solid rgba(255,255,255,0.1)'")
code = code.replace("borderBottom: '1px dashed #E5E5E5'", "borderBottom: '1px dashed rgba(255,255,255,0.1)'")
code = code.replace("background: '#1B212B', color: '#F2F0EA'", "background: 'rgba(27,33,43,0.4)', color: '#F2F0EA'")

# Update text colors in KDS
code = code.replace("color: '#5FAE6E'", "color: '#5FAE6E', textShadow: '0 0 10px rgba(95,174,110,0.5)'")
code = code.replace("fontSize: '80px',", "fontSize: '96px', textShadow: '0 0 30px rgba(255,255,255,0.3)',")
code = code.replace("color: '#E8A33D'", "color: '#E8A33D', textShadow: '0 0 10px rgba(232,163,61,0.5)'")

with open('frontend/src/app/anumaan/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('KDS updated')
