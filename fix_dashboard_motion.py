import re

with open('frontend/src/app/dashboard/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Add Framer motion imports
if "import { motion }" not in code:
    code = code.replace("import Link from 'next/link';", "import Link from 'next/link';\nimport { motion } from 'framer-motion';")

# Re-write the main grid with motion
# Top KPI strip
old_kpi = '''        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="bg-ink-surface p-4 rounded-sm border border-ink-raised shadow-sm">
            <p className="text-[10px] font-mono text-content-secondary uppercase tracking-widest mb-1">Weekly Waste</p>
            <p className="text-2xl font-mono font-bold text-accent-secondary">2,410 <span className="text-sm font-sans font-normal text-content-secondary">kg</span></p>
          </div>
          <div className="bg-ink-surface p-4 rounded-sm border border-ink-raised shadow-sm">
            <p className="text-[10px] font-mono text-content-secondary uppercase tracking-widest mb-1">Rescue Rate</p>
            <p className="text-2xl font-mono font-bold text-status-success">84.2%</p>
          </div>
          <div className="bg-ink-surface p-4 rounded-sm border border-ink-raised shadow-sm">
            <p className="text-[10px] font-mono text-content-secondary uppercase tracking-widest mb-1">Avg Downtime</p>
            <p className="text-2xl font-mono font-bold text-content-primary">12.5%</p>
          </div>
          <div className="bg-ink-surface p-4 rounded-sm border border-ink-raised shadow-sm">
            <p className="text-[10px] font-mono text-content-secondary uppercase tracking-widest mb-1">Sys Health</p>
            <div className="flex items-center gap-2 mt-2">
              <span className="flex h-2 w-2 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-status-success opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-status-success"></span>
              </span>
              <span className="text-sm font-mono text-status-success tracking-widest">ONLINE</span>
            </div>
          </div>
        </div>'''

new_kpi = '''        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, staggerChildren: 0.1 }}
          className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6"
        >
          <motion.div 
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
            whileHover={{ scale: 1.02, backgroundColor: 'rgba(27,33,43,0.8)' }}
            className="bg-ink-surface/60 backdrop-blur-md p-4 rounded-sm border border-ink-raised shadow-sm relative overflow-hidden group"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-accent-secondary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
            <p className="text-[10px] font-mono text-content-secondary uppercase tracking-widest mb-1 relative z-10">Weekly Waste</p>
            <p className="text-2xl font-mono font-bold text-accent-secondary relative z-10">2,410 <span className="text-sm font-sans font-normal text-content-secondary">kg</span></p>
          </motion.div>
          
          <motion.div 
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
            whileHover={{ scale: 1.02, backgroundColor: 'rgba(27,33,43,0.8)' }}
            className="bg-ink-surface/60 backdrop-blur-md p-4 rounded-sm border border-ink-raised shadow-sm relative overflow-hidden group"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-status-success/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
            <p className="text-[10px] font-mono text-content-secondary uppercase tracking-widest mb-1 relative z-10">Rescue Rate</p>
            <p className="text-2xl font-mono font-bold text-status-success relative z-10">84.2%</p>
          </motion.div>
          
          <motion.div 
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
            whileHover={{ scale: 1.02, backgroundColor: 'rgba(27,33,43,0.8)' }}
            className="bg-ink-surface/60 backdrop-blur-md p-4 rounded-sm border border-ink-raised shadow-sm relative overflow-hidden group"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-content-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
            <p className="text-[10px] font-mono text-content-secondary uppercase tracking-widest mb-1 relative z-10">Avg Downtime</p>
            <p className="text-2xl font-mono font-bold text-content-primary relative z-10">12.5%</p>
          </motion.div>
          
          <motion.div 
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
            whileHover={{ scale: 1.02, backgroundColor: 'rgba(27,33,43,0.8)' }}
            className="bg-ink-surface/60 backdrop-blur-md p-4 rounded-sm border border-ink-raised shadow-sm relative overflow-hidden group"
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

code = code.replace(old_kpi, new_kpi)

# Chart section
old_chart = '''        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-ink-surface p-6 rounded-sm border border-ink-raised shadow-sm">'''

new_chart = '''        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="lg:col-span-2 space-y-6">
            <div className="bg-ink-surface/80 backdrop-blur-md p-6 rounded-sm border border-ink-raised shadow-lg shadow-black/20">'''

code = code.replace(old_chart, new_chart)

# End Chart div
old_chart_end = '''              <ForecastChart data={forecasts} />
            </div>'''
new_chart_end = '''              <ForecastChart data={forecasts} />
            </div>
          </motion.div>'''
code = code.replace(old_chart_end, new_chart_end)

# Right column
old_right = '''          <div className="space-y-6">
            <SurplusAlertList events={surplusEvents} />'''
new_right = '''          <motion.div initial={{ opacity: 0, x: 10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.5 }} className="space-y-6 h-full">
            <SurplusAlertList events={surplusEvents} />
          </motion.div>'''
code = code.replace(old_right, new_right)

# Table section
old_table = '''        <div className="mt-6">
          <div className="bg-ink-surface rounded-sm border border-ink-raised shadow-sm">'''
new_table = '''        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6 }} className="mt-6">
          <div className="bg-ink-surface/80 backdrop-blur-md rounded-sm border border-ink-raised shadow-lg shadow-black/20 overflow-hidden">'''
code = code.replace(old_table, new_table)
code = code.replace("</motion.div>\n        </div>\n      </div>", "        </div>\n      </motion.div>\n    </div>")

with open('frontend/src/app/dashboard/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('Dashboard updated with framer-motion')
