import pdfplumber


def iter_text_from_pdf(path: str):
    with pdfplumber.open(path) as pdf:
        for i, p in enumerate(pdf.pages, start=1):
            t = p.extract_text() or ""
            if t.strip():
                yield i, t
