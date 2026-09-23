import re

with open('frontend/src/app/surplus/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Add SpotlightCard
if "SpotlightCard" not in code:
    code = code.replace("import NGOMatchList from '@/components/surplus/NGOMatchList';", "import NGOMatchList from '@/components/surplus/NGOMatchList';\nimport SpotlightCard from '@/components/ui/SpotlightCard';\nimport { motion } from 'framer-motion';")

# Upgrade Layout
code = code.replace('<div className="p-6 md:p-10 h-[100vh] flex flex-col pb-6">', '<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="p-6 md:p-10 h-[100vh] flex flex-col pb-6">')
code = code.replace('</div>\n    </div>\n  );\n}', '</SpotlightCard>\n        </div>\n      </div>\n    </motion.div>\n  );\n}')

# Fix Header
code = code.replace('''      <header className="mb-6 flex justify-between items-end border-b border-ink-raised pb-4">
        <div>
          <h1 className="text-3xl font-display font-bold text-content-primary uppercase tracking-wide">Surplus & Matching</h1>
          <p className="text-content-secondary mt-1 font-mono text-sm tracking-wide">Triage Queue - Dispatch Control</p>
        </div>
      </header>''', '''      <header className="mb-8 flex justify-between items-end border-b border-white/10 pb-6">
        <div>
          <motion.h1 initial={{ y: -10, opacity: 0 }} animate={{ y: 0, opacity: 1 }} className="text-4xl font-display font-bold text-white tracking-tight glow-text-primary">Surplus & Matching</motion.h1>
          <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1 }} className="text-content-secondary mt-2 font-mono text-xs tracking-widest uppercase">Triage Queue - Dispatch Control</motion.p>
        </div>
      </header>''')

# Fix left column container
code = code.replace('<div className="w-1/2 flex flex-col bg-ink-surface rounded-sm border border-ink-raised h-full">', '<SpotlightCard className="w-1/2 flex flex-col h-full shadow-2xl shadow-black/50">')

# Fix Triage header
code = code.replace('<h2 className="text-lg font-display text-content-primary uppercase tracking-wide flex items-center gap-2">', '<h2 className="text-lg font-display text-content-primary uppercase tracking-wide flex items-center gap-3">')
code = code.replace('<span className="bg-ink-raised text-accent-primary font-mono text-[10px] py-0.5 px-1.5 rounded-sm">', '<span className="bg-black/30 text-accent-primary font-mono font-bold text-[10px] py-1 px-2 rounded-md border border-white/5">')
code = code.replace('<div className="p-4 border-b border-ink-raised flex justify-between items-center">', '<div className="p-6 border-b border-white/10 flex justify-between items-center">')

# Fix Manual Entry
code = code.replace('<div className="p-4 border-t border-ink-raised bg-ink-base rounded-b-sm">', '<div className="p-6 border-t border-white/10 bg-black/20 rounded-b-3xl">')
code = code.replace('<select name="category" className="flex-1 p-2 bg-ink-surface border border-ink-raised rounded-sm text-xs font-mono text-content-primary" required defaultValue="Rice">', '<select name="category" className="flex-1 p-2 bg-black/30 border border-white/10 rounded-lg text-xs font-mono text-content-primary focus:border-accent-primary" required defaultValue="Rice">')
code = code.replace('className="w-20 p-2 bg-ink-surface border border-ink-raised rounded-sm text-xs font-mono text-content-primary focus:border-accent-primary focus:outline-none"', 'className="w-20 p-2 bg-black/30 border border-white/10 rounded-lg text-xs font-mono text-content-primary focus:border-accent-primary focus:outline-none"')
code = code.replace('className="bg-ink-raised text-accent-primary border border-accent-primary/50 hover:bg-accent-primary hover:text-ink-base px-3 py-1.5 rounded-sm text-xs font-mono uppercase tracking-widest transition-colors"', 'className="glow-button-primary text-ink-base px-4 py-2 rounded-lg text-xs font-bold font-mono uppercase tracking-widest transition-all"')

# Right Column container
code = code.replace('<div className="w-1/2 flex flex-col h-full bg-ink-base rounded-sm border border-ink-raised">', '<SpotlightCard className="w-1/2 flex flex-col h-full shadow-2xl shadow-black/50 ml-6">')

with open('frontend/src/app/surplus/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('surplus updated')
