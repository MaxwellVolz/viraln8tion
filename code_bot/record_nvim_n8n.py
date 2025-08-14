#!/home/narfa/_git/viraln8tion/.venv/bin/python


import os
import sys
import time
import random
import argparse
import pexpect


def record_typing_to_cast(code: str, source_file: str, cast_file: str) -> None:
    def type_line(child, line, prev_indent=0):
        indent_unit = 4
        is_blank = line.strip() == ""
        current_indent = len(line) - len(line.lstrip()) if not is_blank else prev_indent

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

    with open(source_file, "w") as f:
        f.write("")

    if os.path.exists(cast_file):
        os.remove(cast_file)

    rec_cmd = f"asciinema rec -c 'nvim {source_file}' {cast_file}"
    child = pexpect.spawn(rec_cmd, encoding='utf-8')
    time.sleep(1)
    child.send('i')

    prev_indent = 0
    for line in code.strip().splitlines():
        prev_indent = type_line(child, line, prev_indent)

    child.send('\x1b')
    time.sleep(0.3)
    child.send(":q!\r")
    time.sleep(0.5)
    child.expect(pexpect.EOF)
    print(f"✅ Recorded typing into {cast_file}")


def read_code(args) -> str:
    if args.codefile:
        with open(args.codefile, "r") as f:
            return f.read()
    else:
        return sys.stdin.read()


def main():
    parser = argparse.ArgumentParser(description="Type Python code into nvim and record as .cast")
    parser.add_argument("--codefile", help="Path to Python file to type")
    parser.add_argument("--source", default="counter.py", help="Temporary .py file to type into")
    parser.add_argument("--cast", default="counter.cast", help="Path to output .cast file")

    args = parser.parse_args()
    code = read_code(args)
    if not code.strip():
        print("❌ No code provided via --codefile or stdin", file=sys.stderr)
        sys.exit(1)

    record_typing_to_cast(code, args.source, args.cast)


if __name__ == "__main__":
    main()
