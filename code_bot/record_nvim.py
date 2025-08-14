import os
import time
import pexpect
import random

# Code to type (raw string for indentation)
code = """\

import time

def countdown(start=5):
    print("Starting countdown:")
    for i in range(start, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("Liftoff!! 🚀")

countdown()

"""

# File setup
source_file = "counter.py"
cast_file = "counter.cast"

with open(source_file, "w") as f:
    f.write("")  # start empty

if os.path.exists(cast_file):
    os.remove(cast_file)

# Start asciinema recording into nvim
rec_cmd = f"asciinema rec -c 'nvim {source_file}' {cast_file}"
child = pexpect.spawn(rec_cmd, encoding='utf-8')

# Wait for nvim to be ready
time.sleep(1)


# Step 1: Enter insert mode
# Disable auto-indent
child.send('i')
def type_line(child, line, prev_indent=0):
    indent_unit = 4
    is_blank = line.strip() == ""
    current_indent = len(line) - len(line.lstrip()) if not is_blank else prev_indent

    # Calculate dedents only if the line isn't blank
    if not is_blank and current_indent < prev_indent:
        dedents_needed = (prev_indent - current_indent) // indent_unit
        for _ in range(dedents_needed):
            # child.send('\x04')  # <C-d>
            child.send('\x7f')
            time.sleep(0.2)

    stripped = line.lstrip()

    if random.random() < 0.25:
        time.sleep(random.uniform(0.2, 0.6))

    for char in stripped:
        child.send(char)
        time.sleep(random.uniform(0.015, 0.045))

    child.send('\r')
    time.sleep(0.1)

    return current_indent if not is_blank else prev_indent



# Step 2: Type the code
prev_indent = 0
for line in code.strip().splitlines():
    prev_indent = type_line(child, line, prev_indent)

# Step 3: Exit insert mode
child.send('\x1b')  # ESC
time.sleep(0.3)

# Step 4: Save and quit
child.send(":q!\r")
time.sleep(0.5)

child.expect(pexpect.EOF)
print("✅ Typed into nvim and recorded to counter.cast")
