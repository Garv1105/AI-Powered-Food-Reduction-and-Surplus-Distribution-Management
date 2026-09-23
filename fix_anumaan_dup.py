with open('frontend/src/app/anumaan/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix duplicate border
old_dup = '''background: 'rgba(27, 33, 43, 0.4)', backdropFilter: 'blur(20px)', WebkitBackdropFilter: 'blur(20px)', border: '1px solid rgba(255, 255, 255, 0.05)', boxShadow: '0 4px 30px rgba(0, 0, 0, 0.1)',
              border: '1px solid #D5CCBC',
              borderRadius: '4px','''
new_dup = '''background: 'rgba(27, 33, 43, 0.4)', backdropFilter: 'blur(20px)', WebkitBackdropFilter: 'blur(20px)', border: '1px solid rgba(255, 255, 255, 0.05)', boxShadow: '0 4px 30px rgba(0, 0, 0, 0.1)',
              borderRadius: '24px','''
code = code.replace(old_dup, new_dup)

with open('frontend/src/app/anumaan/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)
