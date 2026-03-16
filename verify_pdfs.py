import os
import pdfplumber

pdf_folder = r"data\documents"

results = []
for filename in os.listdir(pdf_folder):
    if not filename.endswith('.pdf'):
        continue
    path = os.path.join(pdf_folder, filename)
    try:
        with pdfplumber.open(path) as pdf:
            total_chars = 0
            for page in pdf.pages[:5]:
                text = page.extract_text()
                if text:
                    total_chars += len(text)
            pages = len(pdf.pages)
        status = "OK" if total_chars > 1000 else "SCANNED/EMPTY"
        results.append((status, pages, total_chars, filename))
    except Exception as e:
        results.append(("ERROR", 0, 0, f"{filename} — {e}"))

results.sort()
print(f"\n{'Status':<15} {'Pages':>6} {'Chars (5pg)':>12}  Filename")
print("-" * 80)
for status, pages, chars, name in results:
    print(f"{status:<15} {pages:>6} {chars:>12}  {name}")

ok_count = sum(1 for r in results if r[0] == "OK")
print(f"\n{ok_count}/{len(results)} PDFs usable")

