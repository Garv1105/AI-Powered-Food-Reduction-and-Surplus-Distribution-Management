# -*- coding: utf-8 -*-
import re

with open('frontend/src/app/anumaan/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Add Framer motion imports
if "import { motion }" not in code:
    code = code.replace("import clsx from 'clsx';", "import clsx from 'clsx';\nimport { motion, AnimatePresence } from 'framer-motion';")

# Replace standard wrappers with motion
code = code.replace("<div className=\"grid lg:grid-cols-2 min-h-screen\">", "<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className=\"grid lg:grid-cols-2 min-h-[calc(100vh-64px)]\">")

# Add glassmorphism to form container
code = code.replace("background: '#1B212B',", "background: 'rgba(27,33,43,0.7)', backdropFilter: 'blur(12px)', WebkitBackdropFilter: 'blur(12px)',")

# Left form header (using regex to avoid exact match failures on special chars)
code = re.sub(r'<h1 className="text-xl font-display font-bold uppercase tracking-widest text-content-primary mb-1">.*?</h1>',
              r'''<motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
              <h1 className="text-xl font-display font-bold uppercase tracking-widest text-content-primary mb-1 text-glow">
                Demand Forecast Engine
              </h1>''', code, flags=re.DOTALL)

code = re.sub(r'<p className="text-\[11px\] font-mono text-content-secondary uppercase tracking-widest">.*?</p>',
              r'''<p className="text-[11px] font-mono text-content-secondary uppercase tracking-widest flex items-center gap-2">
                <span className="flex h-1.5 w-1.5 relative">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent-secondary opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-accent-secondary"></span>
                </span>
                Anumaan XGBoost Engine
              </p>
            </motion.div>''', code, flags=re.DOTALL)

# Run Prediction button glow
code = re.sub(r'<button\s+disabled=\{loading\}\s+className=\{clsx\([^)]+\)\}\s+onClick=\{handlePredict\}\s+>',
              r'''<motion.button
                whileHover={!loading ? { scale: 1.01 } : {}}
                whileTap={!loading ? { scale: 0.98 } : {}}
                disabled={loading}
                className={clsx(
                  "relative w-full py-4 text-[13px] font-mono font-bold tracking-widest uppercase transition-all rounded-sm overflow-hidden",
                  loading 
                    ? "bg-ink-raised text-content-secondary" 
                    : "bg-accent-primary text-ink-base hover:shadow-[0_0_20px_rgba(232,163,61,0.4)]"
                )}
                onClick={handlePredict}
              >
                {!loading && <div className="absolute inset-0 bg-white/20 -translate-x-full hover:animate-[shimmer_1s_infinite] skew-x-12" />}''', code, flags=re.DOTALL)

code = code.replace("</button>", "</motion.button>")

# KDS Panel
old_kds = '''      <div 
        style={{ 
          padding: '24px', 
          background: '#1B212B', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          borderLeft: '1px solid #232B38'
        }}
      >'''
new_kds = '''      <motion.div 
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.2 }}
        style={{ 
          padding: '24px', 
          background: 'rgba(20,24,31,0.6)', 
          backdropFilter: 'blur(12px)',
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          borderLeft: '1px solid #232B38',
          position: 'relative'
        }}
      >
        <div className="absolute inset-0 bg-grid-pattern opacity-50 pointer-events-none" />'''
code = code.replace(old_kds, new_kds)

# Fix the end tags correctly using regex
code = re.sub(r'      </div>\s*</div>\s*\);\s*\}', r'      </motion.div>\n    </motion.div>\n  );\n}', code)

with open('frontend/src/app/anumaan/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('Anumaan updated with motion')
