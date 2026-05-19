"""Generate contact sheets for visual cover selection.
Extracts MORE pages from each PDF (up to 30) and creates one contact sheet per slug.
"""
import fitz
from PIL import Image
from pathlib import Path
import io

BOOKS_ROOT = Path(r"C:\Users\jpcji\OneDrive\Desktop\MOURA DUBEUX\BAHIA")
OUT_DIR = Path(__file__).parent / "_contact_sheets"
OUT_DIR.mkdir(exist_ok=True)

FOLDERS = {
    "beach-class-bahia": "Beach Class Bahia",
    "beach-class-jaguaribe": "Beach Class Jaguaribe",
    "beach-class-rio-vermelho": "Beach Class Rio Vermelho",
    "casa-sombreiros": "Casa Sombreiros",
    "dumare": "Dumare",
    "elleve-horto": "Elleve",
    "horto-essence": "Horto Essence",
    "infinity-salvador": "Infinity Salvador",
    "mirat-martins-de-sa": "Mirat Martins de Sá",
    "mood-club": "Mood Club",
    "mood-colina": "Mood Colina",
    "mood-costa-azul": "Mood Costa Azul",
    "poeme-horto": "Poème Horto",
    "rive": "Rivê",
    "vivant-caminho-das-arvores": "Vivant",
}

MAX_PAGES = 30  # capture more options
THUMB_W = 320
COLS = 5

def pick_book_pdf(folder: Path, slug: str) -> Path | None:
    pdfs = list(folder.glob("*.pdf"))
    if not pdfs:
        return None
    kw = slug.replace("-", " ").split()[0].lower()
    def score(p: Path) -> int:
        n = p.name.lower()
        s = 0
        if "esp" in n or "especif" in n or "memorial" in n: s -= 100
        if "book" in n: s += 10
        if "digital" in n: s += 5
        if kw in n: s += 8
        return s
    return max(pdfs, key=score)

for slug, fname in FOLDERS.items():
    folder = BOOKS_ROOT / fname
    if not folder.exists():
        for p in BOOKS_ROOT.iterdir():
            if p.is_dir() and slug.split("-")[0].lower() in p.name.lower():
                folder = p; break
    pdf = pick_book_pdf(folder, slug) if folder.exists() else None
    if not pdf:
        print(f"NO PDF {slug}"); continue

    doc = fitz.open(pdf)
    n = min(len(doc), MAX_PAGES)
    print(f"{slug}: {n} pages from {pdf.name}")
    thumbs = []
    for i in range(n):
        pix = doc[i].get_pixmap(matrix=fitz.Matrix(80/72, 80/72), alpha=False)
        img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        # resize keep aspect
        ratio = THUMB_W / img.width
        img = img.resize((THUMB_W, int(img.height * ratio)), Image.LANCZOS)
        thumbs.append((i+1, img))
    doc.close()

    if not thumbs: continue
    rows = (len(thumbs) + COLS - 1) // COLS
    th = max(t[1].height for t in thumbs)
    label_h = 26
    canvas_w = THUMB_W * COLS
    canvas_h = (th + label_h) * rows
    sheet = Image.new("RGB", (canvas_w, canvas_h), "white")
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arialbd.ttf", 18)
    except:
        font = ImageFont.load_default()
    for idx, (page_num, img) in enumerate(thumbs):
        r, c = divmod(idx, COLS)
        x = c * THUMB_W
        y = r * (th + label_h)
        # label
        draw.rectangle([x, y, x+THUMB_W, y+label_h], fill="#000")
        draw.text((x+8, y+3), f"PAGE {page_num}", fill="white", font=font)
        sheet.paste(img, (x, y + label_h))
    out_path = OUT_DIR / f"{slug}.jpg"
    sheet.save(out_path, "JPEG", quality=78)
    print(f"  -> {out_path.name} ({sheet.size})")
