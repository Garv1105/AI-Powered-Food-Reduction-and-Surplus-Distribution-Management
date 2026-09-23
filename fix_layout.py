import re

with open('frontend/src/app/layout.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Add Particles import
if "import Particles" not in code:
    code = code.replace("import Sidebar from '@/components/layout/Sidebar';", "import Sidebar from '@/components/layout/Sidebar';\nimport Particles from '@/components/layout/Particles';")

# Replace bg-grid-pattern with Particles
old_grid = '<div className="absolute inset-0 bg-grid-pattern pointer-events-none z-0" />'
new_grid = '<Particles />'
code = code.replace(old_grid, new_grid)

with open('frontend/src/app/layout.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('Layout updated')
