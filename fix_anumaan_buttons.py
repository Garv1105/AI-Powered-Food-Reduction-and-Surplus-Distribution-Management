with open('frontend/src/app/anumaan/page.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# I replaced EVERY </button> with </motion.button>. Let's revert the one in Toggle and the layout ones.
old_toggle = '''      </span>
    </motion.button>
  );
}'''
new_toggle = '''      </span>
    </button>
  );
}'''
code = code.replace(old_toggle, new_toggle)

# Let's also check for any other </motion.button> that shouldn't be there.
# Only the handlePredict button should be motion.button.
# What about "Clear" or "Reset" buttons?

with open('frontend/src/app/anumaan/page.tsx', 'w', encoding='utf-8') as f:
    f.write(code)

print('Fixed Anumaan buttons')
