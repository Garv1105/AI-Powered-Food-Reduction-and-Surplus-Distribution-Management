import re

with open('frontend/src/app/anumaan/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix DocketInput
code = re.sub(r'(function DocketInput.*?background:\s*\')[^\']+(\'.*?border:\s*\')1px solid [^\']+(\')', r'\g<1>#232B38\g<2>1px solid #3A4255\g<3>', code, flags=re.DOTALL)

# Fix DocketSelect
code = re.sub(r'(function DocketSelect.*?background:\s*\')[^\']+(\'.*?border:\s*\')1px solid [^\']+(\')', r'\g<1>#232B38\g<2>1px solid #3A4255\g<3>', code, flags=re.DOTALL)

# Fix Form background if missed
code = code.replace("background: 'transparent'", "background: '#14181F'")
code = code.replace("'#E8E0D0'", "'#232B38'") 

# Text colors
code = code.replace("color: '#4A5568'", "color: '#9AA3B2'")
code = code.replace("color: '#1C1917'", "color: '#F2F0EA'")

# Right side KDS result panel light theme fix
code = code.replace("background: result ? '#1B212B' : '#1B212B'", "background: '#1B212B'")
code = code.replace("background: result ? '#1C1917' : '#F4EFE6'", "background: '#1B212B'")
code = code.replace("background: result ? '#1B212B' : '#14181F'", "background: '#1B212B'")

with open('frontend/src/app/anumaan/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('Fixed Anumaan inputs')
