import re

with open('frontend/src/app/map/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

if "import { motion }" not in code:
    code = code.replace("import clsx from 'clsx';", "import clsx from 'clsx';\nimport { motion } from 'framer-motion';")

# Map NGO sidebar
old_sidebar = '''        {/* Overlay Sidebar */}
        <div className="absolute top-4 right-4 w-80 max-h-[calc(100%-32px)] bg-ink-surface rounded-sm border border-ink-raised flex flex-col overflow-hidden z-10 shadow-[0_8px_30px_rgb(0,0,0,0.5)]">'''
new_sidebar = '''        {/* Overlay Sidebar */}
        <motion.div 
          initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 }}
          className="absolute top-4 right-4 w-80 max-h-[calc(100%-32px)] bg-ink-surface/80 backdrop-blur-xl rounded-sm border border-ink-raised flex flex-col overflow-hidden z-10 shadow-[0_8px_30px_rgb(0,0,0,0.5)]"
        >'''
code = code.replace(old_sidebar, new_sidebar)
code = re.sub(r'</div>\s*</div>\s*</div>\s*\);\s*\}', r'</motion.div>\n      </div>\n    </div>\n  );\n}', code)

with open('frontend/src/app/map/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

with open('frontend/src/app/reports/page.tsx', 'r', encoding='utf-8') as f:
    code2 = f.read()

if "import { motion }" not in code2:
    code2 = code2.replace("import clsx from 'clsx';", "import clsx from 'clsx';\nimport { motion } from 'framer-motion';")

code2 = code2.replace("<div className=\"p-8 max-w-5xl mx-auto space-y-6\">", "<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className=\"p-8 max-w-5xl mx-auto space-y-6\">")
code2 = code2.replace("<div className=\"bg-ink-surface p-8 rounded-sm border border-ink-raised shadow-sm\">", "<motion.div initial={{ y: 10, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.1 }} className=\"bg-ink-surface/80 backdrop-blur-md p-8 rounded-sm border border-ink-raised shadow-lg shadow-black/20\">")
code2 = code2.replace("<div className=\"grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4\">", "<motion.div initial={{ y: 10, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.2, staggerChildren: 0.1 }} className=\"grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4\">")
code2 = code2.replace("          {report.kpis.map((kpi, i) => (", "          {report.kpis.map((kpi, i) => (")

old_kpi = '''            <div key={i} className="bg-ink-surface p-4 rounded-sm border border-ink-raised">'''
new_kpi = '''            <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} whileHover={{ scale: 1.02 }} className="bg-ink-surface/60 backdrop-blur-md p-4 rounded-sm border border-ink-raised relative overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />'''
code2 = code2.replace(old_kpi, new_kpi)

code2 = re.sub(r'</div>\s*\)\s*\}\s*</div>\s*</div>\s*\);\s*\}', r'</motion.div>\n          ))}\n        </motion.div>\n      </motion.div>\n    </motion.div>\n  );\n}', code2)
code2 = code2.replace("</motion.div>\n      </motion.div>\n    </motion.div>\n  );\n}", "</motion.div>\n      </div>\n    </motion.div>\n  );\n}") # Need to make sure the end tags match.

# Fix the end tags for reports correctly
code2 = code2.replace("</div>\n          ))}\n        </div>", "</motion.div>\n          ))}\n        </motion.div>")
code2 = code2.replace("      </div>\n    </div>\n  );\n}", "      </motion.div>\n    </motion.div>\n  );\n}")

with open('frontend/src/app/reports/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code2)

print('Map & Reports updated with motion')
