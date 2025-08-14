def chunk_text(text: str, max_chars: int = 900, overlap: int = 100):
    out = []
    i, n = 0, len(text)
    while i < n:
        end = min(i + max_chars, n)
        out.append(text[i:end])
        i = max(end - overlap, 0)
    return out
