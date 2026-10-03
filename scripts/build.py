"""Publish one Markdown specification as HTML and an unchanged source file."""

from pathlib import Path
import shutil

import markdown

ROOT = Path(__file__).resolve().parent.parent
source = ROOT / "mutex-md-spec.md"
output = ROOT / "_site"
output.mkdir(exist_ok=True)
renderer = markdown.Markdown(
    extensions=["tables", "fenced_code", "toc", "sane_lists"],
    output_format="html",
)
# Render literal placeholders such as <task> instead of treating them as HTML.
renderer.preprocessors.deregister("html_block")
renderer.inlinePatterns.deregister("html")
content = renderer.convert(source.read_text(encoding="utf-8"))
template = (ROOT / "site" / "template.html").read_text(encoding="utf-8")
(output / "index.html").write_text(template.replace("<!-- SPECIFICATION -->", content), encoding="utf-8")
shutil.copyfile(source, output / source.name)
shutil.copyfile(ROOT / "site" / "style.css", output / "style.css")
(output / ".nojekyll").touch()
print(f"Published {source.name} as {output / 'index.html'} and raw Markdown")
