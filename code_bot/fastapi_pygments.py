from fastapi import FastAPI
from pydantic import BaseModel
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import SvgFormatter
from uuid import uuid4

app = FastAPI()

class CodeRequest(BaseModel):
    code: str

@app.post("/render")
def render_code_svg(request: CodeRequest):
    code = request.code.strip()
    uid = uuid4().hex[:8]
    svg_file = f"/tmp/code_{uid}.svg"

    formatter = SvgFormatter(
        fontfamily="monospace",
        line_numbers=True,
        style="monokai",
        full=True,             # wrap in full <svg> document
        wrapcode=True          # adds <code> tag
    )

    highlighted = highlight(code, PythonLexer(), formatter)

    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(highlighted)

    return {
        "svg_file": svg_file
    }
