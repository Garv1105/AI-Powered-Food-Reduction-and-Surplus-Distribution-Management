with open('frontend/src/app/processing-unit/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix the first one
old_1 = '''              />
            </div>

            {/* Sum metrics row */}'''
new_1 = '''              />
            </motion.div>

            {/* Sum metrics row */}'''
code = code.replace(old_1, new_1)

old_2 = '''                  <p className="text-lg font-bold text-content-primary mt-1">{value}</p>
                </div>
              ))}
            </div>

            {/* Trend charts */}'''
new_2 = '''                  <p className="text-lg font-bold text-content-primary mt-1">{value}</p>
                </div>
              ))}
            </motion.div>

            {/* Trend charts */}'''
code = code.replace(old_2, new_2)

with open('frontend/src/app/processing-unit/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('Fixed PU divs')
