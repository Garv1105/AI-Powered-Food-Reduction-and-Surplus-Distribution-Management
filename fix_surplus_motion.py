import re

with open('frontend/src/app/surplus/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

if "import { motion }" not in code:
    code = code.replace("import clsx from 'clsx';", "import clsx from 'clsx';\nimport { motion } from 'framer-motion';")

# Stagger the events map
code = code.replace("        <div className=\"flex-1 overflow-y-auto pr-2 space-y-3\">", "        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ staggerChildren: 0.1 }} className=\"flex-1 overflow-y-auto pr-2 space-y-3\">")
code = code.replace("            return [...active, ...expired];\n              })().map((event) => {", "            return [...active, ...expired];\n              })().map((event, i) => {")

old_event = '''                  return (
                    <div 
                      key={event.id}'''
new_event = '''                  return (
                    <motion.div 
                      key={event.id}
                      initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}
                      whileHover={!isSelected ? { scale: 1.01 } : {}}'''
code = code.replace(old_event, new_event)
code = re.sub(r'</div>\s*\);\s*\}\)\}', r'</motion.div>\n                  );\n                })}', code)

code = code.replace("</div>\n              ) : events.length === 0", "</motion.div>\n              ) : events.length === 0")

with open('frontend/src/app/surplus/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

with open('frontend/src/components/surplus/NGOMatchList.tsx', 'r', encoding='utf-8') as f:
    code2 = f.read()

if "import { motion }" not in code2:
    code2 = code2.replace("import clsx from 'clsx';", "import clsx from 'clsx';\nimport { motion } from 'framer-motion';")

code2 = code2.replace("<div className=\"flex-1 overflow-y-auto pr-2 space-y-3 mt-4\">", "<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ staggerChildren: 0.1 }} className=\"flex-1 overflow-y-auto pr-2 space-y-3 mt-4\">")

old_ngo = '''              return (
                <div key={match.ngo_id} className={clsx("p-5 rounded-sm border transition-all", isBestMatch ? 
"bg-ink-raised border-accent-secondary" : "bg-ink-surface border-ink-raised")}>'''
new_ngo = '''              return (
                <motion.div 
                  key={match.ngo_id} 
                  initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: idx * 0.1 }}
                  whileHover={!isBestMatch ? { scale: 1.01 } : {}}
                  className={clsx("p-5 rounded-sm border transition-all relative overflow-hidden", isBestMatch ? 
"bg-ink-raised/80 backdrop-blur-md border-accent-secondary shadow-[0_0_15px_rgba(232,163,61,0.15)]" : "bg-ink-surface/60 backdrop-blur-md border-ink-raised hover:bg-ink-raised")}
                >
                  {isBestMatch && <div className="absolute inset-0 bg-gradient-to-br from-accent-secondary/5 to-transparent pointer-events-none" />}'''
code2 = code2.replace(old_ngo, new_ngo)
code2 = re.sub(r'</div>\s*\);\s*\}\)\}\s*</div>', r'</motion.div>\n              );\n            })}\n          </motion.div>', code2)

with open('frontend/src/components/surplus/NGOMatchList.tsx', 'w', encoding='utf-8') as f:
    f.write(code2)

print('Surplus updated with motion')
