import re

with open('frontend/src/app/surplus/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

old_map = 'events.map((event) => {'
new_map = '''(() => {
                const active = events.filter(e => e.urgency_level.toUpperCase() !== 'EXPIRED');
                const expired = events.filter(e => e.urgency_level.toUpperCase() === 'EXPIRED').slice(0, 3);
                // Sort active by rescue_window_hours (lowest first)
                active.sort((a, b) => a.rescue_window_hours - b.rescue_window_hours);
                return [...active, ...expired];
              })().map((event) => {'''

code = code.replace(old_map, new_map)

with open('frontend/src/app/surplus/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('Updated surplus list sorting')
