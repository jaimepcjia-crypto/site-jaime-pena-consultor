"""Extract images from Moura Dubeux PDF books with MANUALLY CHOSEN facade covers.

For each slug, COVER_PAGE specifies the PDF page (1-indexed) to use as the
property card thumbnail. Remaining gallery pages are filtered by content
heuristics and ordered by original page number.
"""
import fitz
import io
import json
import statistics
from pathlib import Path
from PIL import Image

BOOKS_ROOT = Path(r"C:\Users\jpcji\OneDrive\Desktop\MOURA DUBEUX\BAHIA")
PROJECT = Path(__file__).parent
OUTPUT_ROOT = PROJECT / "public" / "images" / "empreendimentos"
JSON_PATH = PROJECT / "src" / "data" / "empreendimentos.json"

# slug -> (folder_name, cover_page_number_1indexed)
EMPREENDIMENTOS = {
    "beach-class-bahia":             ("Beach Class Bahia",        11),
    "beach-class-jaguaribe":         ("Beach Class Jaguaribe",     5),
    "beach-class-rio-vermelho":      ("Beach Class Rio Vermelho", 10),
    "casa-sombreiros":               ("Casa Sombreiros",           8),
    "dumare":                        ("Dumare",                    8),
    "elleve-horto":                  ("Elleve",                    3),
    "horto-essence":                 ("Horto Essence",             8),
    "infinity-salvador":             ("Infinity Salvador",         8),
    "mirat-martins-de-sa":           ("Mirat Martins de Sá",       8),
    "mood-club":                     ("Mood Club",                 7),
    "mood-colina":                   ("Mood Colina",               6),
    "mood-costa-azul":               ("Mood Costa Azul",           6),
    "poeme-horto":                   ("Poème Horto",              11),
    "rive":                          ("Rivê",                     14),
    "vivant-caminho-das-arvores":    ("Vivant",                   19),
}

MAX_GALLERY = 11   # gallery images (in addition to cover = 12 total)
DPI = 130

def is_content_page(pix_bytes: bytes) -> tuple[bool, str]:
    img = Image.open(io.BytesIO(pix_bytes)).convert("RGB")
    img.thumbnail((300, 420))
    pixels = list(img.getdata())
    n = len(pixels)
    grays = [int(0.299*r + 0.587*g + 0.114*b) for (r, g, b) in pixels]
    stdev = statistics.pstdev(grays)
    near_white = sum(1 for g in grays if g >= 235) / n
    near_black = sum(1 for g in grays if g <= 25) / n
    uniform = near_white + near_black
    buckets = set()
    for (r, g, b) in pixels[::13]:
        buckets.add((r >> 4, g >> 4, b >> 4))
    bucket_ratio = len(buckets) / (n / 13)
    if stdev < 38: return False, f"low-var({stdev:.0f})"
    if uniform > 0.78: return False, f"uniform({uniform:.2f})"
    if bucket_ratio < 0.06: return False, f"few-colors({bucket_ratio:.2f})"
    return True, "OK"

def pick_pdf(folder: Path, slug: str) -> Path | None:
    pdfs = list(folder.glob("*.pdf"))
    if not pdfs: return None
    kw = slug.replace("-", " ").split()[0].lower()
    def score(p: Path) -> int:
        n = p.name.lower(); s = 0
        if "esp" in n or "especif" in n or "memorial" in n: s -= 100
        if "book" in n: s += 10
        if "digital" in n: s += 5
        if kw in n: s += 8
        return s
    return max(pdfs, key=score)


OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
mat = fitz.Matrix(DPI/72, DPI/72)
preview_mat = fitz.Matrix(60/72, 60/72)
results = {}

for slug, (folder_name, cover_page) in EMPREENDIMENTOS.items():
    folder = BOOKS_ROOT / folder_name
    if not folder.exists():
        for p in BOOKS_ROOT.iterdir():
            if p.is_dir() and slug.split("-")[0].lower() in p.name.lower():
                folder = p; break
    pdf = pick_pdf(folder, slug) if folder.exists() else None
    if not pdf:
        print(f"  ! NO PDF {slug}"); continue

    out_dir = OUTPUT_ROOT / slug
    if out_dir.exists():
        for f in out_dir.glob("*.jpg"): f.unlink()
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf)
    print(f"\n>> {slug}  (cover=p{cover_page}, pdf={pdf.name})")

    # 1) Cover (forced page)
    cover_idx = cover_page - 1
    cover_pix = doc[cover_idx].get_pixmap(matrix=mat, alpha=False)
    cover_pix.save(str(out_dir / "01.jpg"), jpg_quality=82)
    images = [f"/images/empreendimentos/{slug}/01.jpg"]

    # 2) Gallery — filtered pages, excluding the cover page
    gallery = []
    for i in range(len(doc)):
        if i == cover_idx: continue
        if len(gallery) >= MAX_GALLERY: break
        prev = doc[i].get_pixmap(matrix=preview_mat, alpha=False)
        keep, reason = is_content_page(prev.tobytes("png"))
        # also exclude first 2 pages (book covers/title spreads) from gallery
        if not keep or i < 2: continue
        pix = doc[i].get_pixmap(matrix=mat, alpha=False)
        idx = len(gallery) + 2
        fn = f"{idx:02d}.jpg"
        pix.save(str(out_dir / fn), jpg_quality=82)
        gallery.append(f"/images/empreendimentos/{slug}/{fn}")

    # FALLBACK: if filter rejected everything, take pages 3+ unconditionally
    if len(gallery) == 0:
        for i in range(2, len(doc)):
            if i == cover_idx: continue
            if len(gallery) >= MAX_GALLERY: break
            pix = doc[i].get_pixmap(matrix=mat, alpha=False)
            idx = len(gallery) + 2
            fn = f"{idx:02d}.jpg"
            pix.save(str(out_dir / fn), jpg_quality=82)
            gallery.append(f"/images/empreendimentos/{slug}/{fn}")

    doc.close()
    images.extend(gallery)
    results[slug] = images
    print(f"   total={len(images)} (cover + {len(gallery)} gallery)")

# Update JSON
data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
for entry in data:
    if entry["slug"] in results:
        entry["images"] = results[entry["slug"]]
JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\n[DONE] {sum(len(v) for v in results.values())} images across {len(results)} empreendimentos")
