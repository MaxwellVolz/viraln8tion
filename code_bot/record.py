import os
import time
import pexpect

# Code to type (use raw string to preserve indents)
code = """\
import time

def countdown(start=5):
    print("Starting countdown:")
    for i in range(start, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("Liftoff! 🚀")

countdown()
"""

# Output .py and .cast file
with open("counter.py", "w") as f:
    f.write(code)

cast_file = "counter.cast"
if os.path.exists(cast_file):
    os.remove(cast_file)

# Start REPL recording session
rec_cmd = f"asciinema rec -c 'python3 -i' {cast_file}"
child = pexpect.spawn(rec_cmd, encoding='utf-8')

child.expect_exact(">>>")  # Wait for prompt

# Simulate typing code into REPL
for line in code.strip().splitlines():
    for char in line:
        child.send(char)
        time.sleep(0.03)  # Typing speed per char
    child.send('\r')  # "Enter" after line
    time.sleep(0.1)

# Send final newline to finish multiline block
child.send('\r')
time.sleep(1)

# Exit cleanly
child.sendline("exit()")
child.expect(pexpect.EOF)

print("✅ Typing + recording complete.")
