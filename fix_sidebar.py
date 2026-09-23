import re

with open('frontend/src/components/layout/Sidebar.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Make sidebar glassmorphic
code = code.replace("className=\"w-64 h-screen bg-ink-surface border-r border-ink-raised fixed left-0 top-0 flex flex-col\"", "className=\"w-64 h-screen bg-ink-surface/80 backdrop-blur-xl border-r border-ink-raised fixed left-0 top-0 flex flex-col z-50\"")

# Add framer-motion import
if "import { motion }" not in code:
    code = code.replace("import clsx from 'clsx';", "import clsx from 'clsx';\nimport { motion } from 'framer-motion';")

# Re-write the links rendering
old_nav = '''      <nav className="flex-1 px-4 space-y-1">
        {links.map((link) => {
          const isActive = pathname === link.href;
          const Icon = link.icon;
          return (
            <Link 
              key={link.href} 
              href={link.href}
              className={clsx(
                "flex items-center gap-3 px-3 py-2 rounded-sm text-sm font-medium transition-colors font-mono tracking-wide uppercase",
                isActive 
                  ? "bg-ink-raised text-accent-primary" 
                  : "text-content-secondary hover:bg-ink-raised hover:text-content-primary"
              )}
            >
              <Icon size={18} className={isActive ? 'opacity-100' : 'opacity-70'} />
              {link.label}
              {link.hasAlerts && (
                <span className="ml-auto flex h-2 w-2 relative">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-status-critical opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-status-critical"></span>
                </span>
              )}
            </Link>
          );
        })}
      </nav>'''

new_nav = '''      <nav className="flex-1 px-4 space-y-1.5 relative">
        {links.map((link) => {
          const isActive = pathname === link.href;
          const Icon = link.icon;
          return (
            <Link 
              key={link.href} 
              href={link.href}
              className={clsx(
                "relative flex items-center gap-3 px-3 py-2.5 rounded-sm text-[11px] font-bold transition-colors font-mono tracking-widest uppercase z-10 group",
                isActive 
                  ? "text-content-primary" 
                  : "text-content-secondary hover:text-content-primary"
              )}
            >
              {isActive && (
                <motion.div
                  layoutId="active-sidebar-pill"
                  className="absolute inset-0 bg-ink-raised border border-ink-raised rounded-sm z-[-1]"
                  transition={{ type: "spring", stiffness: 350, damping: 30 }}
                />
              )}
              {isActive && (
                <motion.div
                  layoutId="active-sidebar-indicator"
                  className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-1/2 bg-accent-primary rounded-r-full z-[-1]"
                  transition={{ type: "spring", stiffness: 350, damping: 30 }}
                />
              )}
              <Icon size={16} className={clsx("transition-transform duration-300 group-hover:scale-110", isActive ? 'text-accent-primary' : 'opacity-70')} />
              <span className="truncate">{link.label}</span>
              {link.hasAlerts && (
                <span className="ml-auto flex h-1.5 w-1.5 relative">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-status-critical opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-full w-full bg-status-critical"></span>
                </span>
              )}
            </Link>
          );
        })}
      </nav>'''

code = code.replace(old_nav, new_nav)

with open('frontend/src/components/layout/Sidebar.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('Sidebar updated')
