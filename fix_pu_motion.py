import re

with open('frontend/src/app/processing-unit/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

if "import { motion }" not in code:
    code = code.replace("import clsx from 'clsx';", "import clsx from 'clsx';\nimport { motion } from 'framer-motion';")

# Re-write the scorecards container
code = code.replace("<div className=\"grid grid-cols-2 lg:grid-cols-4 gap-4\">", "<motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ staggerChildren: 0.1 }} className=\"grid grid-cols-2 lg:grid-cols-4 gap-4\">")
code = code.replace("            </div>\n\n            {/* Sum metrics row */}", "            </motion.div>\n\n            {/* Sum metrics row */}")

# Scorecard component needs to use motion.div
code = code.replace("function Scorecard({", "function Scorecard({")

old_scorecard = '''  return (
    <div className="bg-ink-surface rounded-sm p-5 border border-ink-raised shadow-none flex flex-col justify-between">'''
new_scorecard = '''  return (
    <motion.div 
      variants={{ hidden: { opacity: 0, y: 10 }, visible: { opacity: 1, y: 0 } }}
      whileHover={{ scale: 1.02 }}
      className="bg-ink-surface/80 backdrop-blur-md rounded-sm p-5 border border-ink-raised shadow-sm flex flex-col justify-between group overflow-hidden relative"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />'''
code = code.replace(old_scorecard, new_scorecard)
code = re.sub(r'</div>\s*\);\s*\}', r'</motion.div>\n  );\n}', code)

with open('frontend/src/app/processing-unit/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('PU updated with motion')
