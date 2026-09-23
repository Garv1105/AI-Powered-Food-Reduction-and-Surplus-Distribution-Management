import re

with open('frontend/src/app/dashboard/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Add imports
if "SpotlightCard" not in code:
    code = code.replace("import { motion } from 'framer-motion';", "import { motion } from 'framer-motion';\nimport SpotlightCard from '@/components/ui/SpotlightCard';\nimport AnimatedCounter from '@/components/ui/AnimatedCounter';")

# Replace KPI cards
old_kpi = '''        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, staggerChildren: 0.1 }}
          className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6"
        >
          <motion.div 
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
            whileHover={{ scale: 1.02, backgroundColor: 'rgba(27,33,43,0.8)' }}
            className="glass-premium p-4 rounded-3xl border border-white/5 shadow-sm relative overflow-hidden group"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-accent-secondary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
            <p className="text-[10px] font-mono text-content-secondary uppercase tracking-widest mb-1 relative z-10">Weekly Waste</p>
            <p className="text-4xl font-display font-bold glow-text-secondary text-accent-secondary tracking-tight relative z-10">2,410 <span className="text-sm font-sans font-normal text-content-secondary">kg</span></p>
          </motion.div>
          
          <motion.div 
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
            whileHover={{ scale: 1.02, backgroundColor: 'rgba(27,33,43,0.8)' }}
            className="glass-premium p-4 rounded-3xl border border-white/5 shadow-sm relative overflow-hidden group"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-status-success/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
            <p className="text-[10px] font-mono text-content-secondary uppercase tracking-widest mb-1 relative z-10">Rescue Rate</p>
            <p className="text-4xl font-display font-bold text-status-success tracking-tight drop-shadow-[0_0_15px_rgba(95,174,110,0.5)] relative z-10">84.2%</p>
          </motion.div>
          
          <motion.div 
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
            whileHover={{ scale: 1.02, backgroundColor: 'rgba(27,33,43,0.8)' }}
            className="glass-premium p-4 rounded-3xl border border-white/5 shadow-sm relative overflow-hidden group"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-content-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
            <p className="text-[10px] font-mono text-content-secondary uppercase tracking-widest mb-1 relative z-10">Avg Downtime</p>
            <p className="text-4xl font-display font-bold text-content-primary tracking-tight relative z-10">12.5%</p>
          </motion.div>
          
          <motion.div 
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
            whileHover={{ scale: 1.02, backgroundColor: 'rgba(27,33,43,0.8)' }}
            className="glass-premium p-4 rounded-3xl border border-white/5 shadow-sm relative overflow-hidden group"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-status-success/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
            <p className="text-[10px] font-mono text-content-secondary uppercase tracking-widest mb-1 relative z-10">Sys Health</p>
            <div className="flex items-center gap-2 mt-2 relative z-10">
              <span className="flex h-1.5 w-1.5 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-status-success opacity-75"></span>
                <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-status-success"></span>
              </span>
              <span className="text-xs font-mono text-status-success tracking-widest uppercase">SYS_ONLINE</span>
            </div>
          </motion.div>
        </motion.div>'''

new_kpi = '''        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, staggerChildren: 0.1 }}
          className="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
        >
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
            <SpotlightCard className="p-6">
              <p className="text-[10px] font-mono text-content-secondary uppercase tracking-widest mb-2 opacity-70">Weekly Waste</p>
              <p className="text-5xl font-display font-bold glow-text-secondary text-accent-secondary tracking-tighter">
                <AnimatedCounter value={2410} suffix=" kg" />
              </p>
            </SpotlightCard>
          </motion.div>
          
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
            <SpotlightCard className="p-6">
              <p className="text-[10px] font-mono text-content-secondary uppercase tracking-widest mb-2 opacity-70">Rescue Rate</p>
              <p className="text-5xl font-display font-bold text-status-success tracking-tighter drop-shadow-[0_0_20px_rgba(95,174,110,0.6)]">
                <AnimatedCounter value={84} suffix=".2%" />
              </p>
            </SpotlightCard>
          </motion.div>
          
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
            <SpotlightCard className="p-6">
              <p className="text-[10px] font-mono text-content-secondary uppercase tracking-widest mb-2 opacity-70">Avg Downtime</p>
              <p className="text-5xl font-display font-bold text-content-primary tracking-tighter drop-shadow-lg">
                <AnimatedCounter value={12} suffix=".5%" />
              </p>
            </SpotlightCard>
          </motion.div>
          
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
            <SpotlightCard className="p-6 flex flex-col justify-between h-full">
              <p className="text-[10px] font-mono text-content-secondary uppercase tracking-widest mb-2 opacity-70">System Core</p>
              <div className="flex items-center gap-3">
                <span className="flex h-3 w-3 relative">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-status-success opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-status-success shadow-[0_0_15px_rgba(95,174,110,1)]"></span>
                </span>
                <span className="text-sm font-display font-bold text-status-success tracking-widest uppercase drop-shadow-[0_0_10px_rgba(95,174,110,0.5)]">ONLINE</span>
              </div>
            </SpotlightCard>
          </motion.div>
        </motion.div>'''
code = code.replace(old_kpi, new_kpi)

# Chart section - swap glass-premium div to SpotlightCard
old_chart = '''<div className="glass-premium p-6 rounded-3xl border border-white/5 shadow-lg shadow-black/20">'''
new_chart = '''<SpotlightCard className="p-6 shadow-2xl shadow-black/50">'''
code = code.replace(old_chart, new_chart)

code = code.replace('</div>\n          </motion.div>', '</SpotlightCard>\n          </motion.div>')
code = code.replace('<div className="glass-premium rounded-3xl border border-white/5 shadow-lg shadow-black/20 overflow-hidden">', '<SpotlightCard className="shadow-2xl shadow-black/50">')

# Wait, there's a second </div>\n      </motion.div> that corresponds to the table. Let's do it via regex.
code = re.sub(r'</div>\s*</motion\.div>\s*</div>\s*</main>', r'</SpotlightCard>\n        </motion.div>\n      </div>\n    </main>', code)

with open('frontend/src/app/dashboard/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('Dashboard upgraded to v3')
