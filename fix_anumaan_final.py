import re
import io

with io.open('frontend/src/app/anumaan/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Make outer wrapper dark
code = code.replace("background: 'transparent'", "background: '#14181F'")
code = code.replace("backgroundColor: 'transparent'", "backgroundColor: '#14181F'")

# Make form container dark surface
code = code.replace("background: '#1B212B'", "background: '#1B212B'") # Ensure it wasn't partially changed
# In case it's still #F9F7F4 from earlier versions
code = code.replace("'#F9F7F4'", "'#1B212B'")
code = code.replace("border: '1px solid #232B38'", "border: '1px solid #232B38'")
code = code.replace("'#D5CCBC'", "'#232B38'")

# Section labels
code = code.replace("color: '#9AA3B2'", "color: '#9AA3B2'") 
# Was color: '#5C4F3E'
code = code.replace("'#5C4F3E'", "'#9AA3B2'")

# Input styles
code = code.replace("background: 'transparent'", "background: '#232B38'")
code = code.replace("'#E8E0D0'", "'#3A4255'") # border color for inputs
code = code.replace("'#4A5568'", "'#9AA3B2'") # label colors

# Button styles
code = code.replace("'#C2440E'", "'#E8A33D'")

# Right panel (KDS)
code = code.replace("background: result ? '#1B212B' : '#14181F'", "background: '#1B212B'")
code = code.replace("background: result ? '#1C1917' : '#F4EFE6'", "background: '#1B212B'")

# Header
code = code.replace("bg-white", "bg-ink-base")
code = code.replace("border-slate-200", "border-ink-raised")
code = code.replace("text-navy", "text-content-primary")

with io.open('frontend/src/app/anumaan/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('Done fixing Anumaan')
