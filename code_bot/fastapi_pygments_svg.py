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
        linenos=True,       # ensures line numbers are rendered
        style="dracula",        # or 'dracula', 'native', etc.
        full=True,              # wraps in full SVG document
        wrapcode=True,          # wraps <code> tag (for embedding)
        noclasses=True,         # ensures inline CSS instead of class references
        line_number_fg="#aaa",  # tweak if needed
        line_number_bg="#2e2e2e"
    )
    svg = highlight(code, PythonLexer(), formatter)

    # ✅ Force background manually (Pyments bug workaround)
    # This line below directly injects background style into <svg>
    svg = svg.replace(
        '<svg',
        '<svg style="background-color:#272822;"'
    )

    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(svg)

    return {
        "svg_file": svg_file
    }
