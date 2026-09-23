with open('frontend/src/app/processing-unit/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# I will replace all </motion.div> with </div> EXCEPT the one in Scorecard, and the one that actually matches <motion.div...
# Actually, the easiest is to revert all </motion.div> to </div>.
code = code.replace('</motion.div>', '</div>')

# Then I'll replace the one in Scorecard back to </motion.div>
# Wait, I also had <motion.div> in the main page grid container:
# <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ staggerChildren: 0.1 }} className="grid grid-cols-2 lg:grid-cols-4 gap-4">
# So that container needs to be closed with </motion.div>.
# Let's do it carefully.
