import json, re, html

from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

def slugify(s):
    s = s.strip().replace("/", "-").replace("\\", "-")
    s = re.sub(r"[\n\r\t]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    s = s.replace(":", " -")
    s = re.sub(r"[^\w\-. ]+", "", s, flags=re.UNICODE)
    return s.strip()

REMOVE_SELECTORS = [
    "#banner", "#breadcrumb", "#faixa", "#menu-lateral", "#menu-imagem",
    ".puv_box_info_compass", ".puv_box_info_lightbulb", ".puv_box_info_book"
]

DROP_TAGS = {"script", "style", "iframe", "img", "figure", "figcaption", "nav", "aside"}

IGNORE_LINE_PATTERNS = [
    r"^\s*↑\s*Voltar ao topo\s*$",
    r"^\s*Figura\s*\d+\s*[-–:].*$",
    r"^\s*Fonte\s*:?.*$",
    r"^\s*---\s*$",
]

IGNORE_RE = re.compile("|".join(f"(?:{p})" for p in IGNORE_LINE_PATTERNS), re.IGNORECASE)
IGNORE_HEADING_RE = re.compile(r"^\s*NESTA\s+SESS(?:ÃO|AO)\s*$", re.IGNORECASE)

def should_drop_line(line: str) -> bool:
    return bool(IGNORE_RE.match(line.strip()))

def text_inline(node):
    parts = []
    for child in node.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif isinstance(child, Tag):
            name = child.name.lower()
            if name in ("strong","b","em","i","span","u","small","abbr","code","sub","sup","mark"):
                parts.append(text_inline(child))
            elif name == "br":
                parts.append("\n")
            elif name == "a":
                parts.append(text_inline(child))
            else:
                parts.append(text_inline(child))
    return "".join(parts)

def table_to_text(tbl):
    lines = []
    for tr in tbl.find_all("tr"):
        cells = [text_inline(td).strip() for td in tr.find_all(["th","td"])]
        cells = [c for c in cells if c]
        if cells:
            lines.append(" | ".join(cells))
    if lines:
        lines.append("")
    return "\n".join(lines)

def html_to_text(html_text):
    html_text = html.unescape(html_text).replace("\xa0", " ")
    soup = BeautifulSoup(html_text, "html.parser")
    for sel in REMOVE_SELECTORS:
        for t in soup.select(sel):
            t.decompose()
    for t in soup.find_all(DROP_TAGS):
        t.decompose()
    out = []
    def walk(parent):
        for el in parent.children:
            if isinstance(el, NavigableString):
                t = str(el).strip()
                if t and not should_drop_line(t):
                    out.append(t)
                continue
            if not isinstance(el, Tag):
                continue
            name = el.name.lower()
            if name in ("h1","h2","h3","h4","h5","h6"):
                level = int(name[1])
                title = text_inline(el).strip()
                if title and not should_drop_line(title) and not IGNORE_HEADING_RE.match(title):
                    out.append("#"*level + " " + title)
                    out.append("")
            elif name == "p":
                txt = text_inline(el).strip()
                if txt and not should_drop_line(txt):
                    out.append(txt)
                    out.append("")
            elif name in ("ul","ol"):
                for li in el.find_all("li", recursive=False):
                    txt = text_inline(li).strip()
                    if txt and not should_drop_line(txt):
                        out.append("- " + txt)
                out.append("")
            elif name == "li":
                txt = text_inline(el).strip()
                if txt and not should_drop_line(txt):
                    out.append("- " + txt)
            elif name == "hr":
                pass
            elif name == "table":
                tx = table_to_text(el)
                if tx:
                    kept = []
                    for ln in tx.splitlines():
                        if not should_drop_line(ln):
                            kept.append(ln)
                    kept_text = "\n".join(kept).strip()
                    if kept_text:
                        out.append(kept_text)
                        out.append("")
            else:
                walk(el)
    walk(soup)
    text = "\n".join(out)
    text = "\n".join([ln for ln in text.splitlines() if not should_drop_line(ln)])
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"

def main():
    js_raw = Path("course-data.js").read_text(encoding="utf-8")
    raw = js_raw.replace("window.COURSE_DATA = ", "").strip()
    if raw.endswith(";"):
        raw = raw[:-1]
    data = json.loads(raw)
    title = data.get("title", "Curso")
    result = ["# " + title, ""]
    for mod in data.get("modules", []):
        for it in mod.get("items", []):
            if it.get("type") == "WikiPage":
                result.append("## " + it.get("title", "Página"))
                result.append("")
                result.append(html_to_text(it.get("content", "")))
    outname = Path(slugify(title) + ".md")
    outname.write_text("\n".join(result), encoding="utf-8")
    print("Markdown gerado:", outname.name)

if __name__ == "__main__":
    main()
