from fastapi import FastAPI
from pydantic import BaseModel
import os, time, pexpect, random
from uuid import uuid4

app = FastAPI()

class CodeRequest(BaseModel):
    code: str

@app.post("/render")
def render_terminal_typing(request: CodeRequest):
    code = request.code.strip()

    uid = uuid4().hex[:8]
    source_file = f"/tmp/code_{uid}.py"
    cast_file = f"/tmp/code_{uid}.cast"

    with open(source_file, "w") as f:
        f.write("")

    if os.path.exists(cast_file):
        os.remove(cast_file)

    child = pexpect.spawn(
        f"asciinema rec -c 'nvim {source_file}' {cast_file}",
        encoding='utf-8',
        dimensions=(30, 100),
        timeout=120
    )

    child.delaybeforesend = 0.05  # slow down slightly, fastapi makes timing sensitive
    time.sleep(1.0)

    # Enter insert mode cleanly
    child.send("i")

    def type_line(child, line, prev_indent=0):
        indent_unit = 4
        is_blank = line.strip() == ""
        current_indent = len(line) - len(line.lstrip()) if not is_blank else prev_indent

        # Handle dedent
        if not is_blank and current_indent < prev_indent:
            dedents_needed = (prev_indent - current_indent) // indent_unit
            for _ in range(dedents_needed):
                child.sendcontrol('d')
                time.sleep(0.1)

        # Handle indent
        if not is_blank and current_indent > prev_indent:
            indents_needed = (current_indent - prev_indent) // indent_unit
            for _ in range(indents_needed):
                child.send('\t')
                time.sleep(0.1)

        # Type line content
        for char in line.lstrip():
            child.send(char)
            time.sleep(random.uniform(0.015, 0.045))

        # Always finish line with newline
        child.send('\r')
        time.sleep(0.1)

        return current_indent if not is_blank else prev_indent

    prev_indent = 0
    for line in code.splitlines():
        prev_indent = type_line(child, line, prev_indent)

    # Finish insert mode
    child.send('\x1b')
    time.sleep(0.2)
    child.send(":wq\r")
    time.sleep(0.5)
    child.expect(pexpect.EOF)

    time.sleep(0.5)
    child.sendcontrol('d')
    time.sleep(1)


    gif_file = f"/tmp/code_{uid}.gif"
    child = pexpect.spawn(f"agg {cast_file} {gif_file}", encoding='utf-8')
    child.expect(pexpect.EOF)

    return {
        "cast_file": cast_file,
        "source_file": source_file,
        "gif_file": gif_file
    }
