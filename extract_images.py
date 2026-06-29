"""Render every page from each Moura Dubeux book into the site galleries.

Each PDF page is exported as a full-page JPG, including covers and text pages,
in the exact order used by the source book. Existing root gallery images are
left untouched because some are used by hero/card images.
"""
import json
import shutil
import sys
from pathlib import Path

import fitz


BOOKS_ROOT = Path(r"C:\Users\jpcji\OneDrive\Desktop\Todos os books")
PROJECT = Path(__file__).parent
OUTPUT_ROOT = PROJECT / "public" / "images" / "empreendimentos"
JSON_PATH = PROJECT / "src" / "data" / "empreendimentos.json"

DPI = 216
JPG_QUALITY = 95

# slug -> PDF filename
BOOKS = {
    "beach-class-bahia": "Beach Class Bahia.pdf",
    "beach-class-jaguaribe": "Beach Class Jaguaribe.pdf",
    "beach-class-rio-vermelho": "Beach Class Rio Vermelho.pdf",
    "casa-sombreiros": "Casa Sombreiros.pdf",
    "cyano": "CYANO.pdf",
    "dumare": "Dumare.pdf",
    "elleve-horto": "ELLEVE.pdf",
    "horto-essence": "HORTO ESSENCE.pdf",
    "infinity-salvador": "Infinity.pdf",
    "mirat-martins-de-sa": "Mirat.pdf",
    "mood-club": "Mood Club.pdf",
    "mood-colina": "Mood Colina.pdf",
    "mood-costa-azul": "Mood Costa Azul.pdf",
    "poeme-horto": "Poème.pdf",
    "rive": "RIVE.pdf",
    "salvador-220": "SALVADOR 220.pdf",
    "vivant-caminho-das-arvores": "Vivant.pdf",
}

SOURCE_OVERRIDES = {
    "elleve-horto": Path(r"C:\Users\jpcji\OneDrive\Desktop\MOURA DUBEUX\Empreendimentos\Elleve\ELLEVE.pdf"),
    "mood-club": Path(r"C:\Users\jpcji\OneDrive\Desktop\MOURA DUBEUX\Empreendimentos\Mood Club\MOOD CLUB.pdf"),
    "mood-colina": Path(r"C:\Users\jpcji\OneDrive\Desktop\MOURA DUBEUX\Empreendimentos\Mood Colina\MOOD COLINA.pdf"),
    "mood-costa-azul": Path(r"C:\Users\jpcji\OneDrive\Desktop\MOURA DUBEUX\Empreendimentos\Mood Costa Azul\MOOD COSTA AZUL.pdf"),
}

# These pages currently depend on images[0] as the hero fallback. Pin them
# before replacing images with the full book-page sequence.
HERO_FALLBACKS = {
    "dumare": "/images/empreendimentos/dumare/01.jpg",
    "mood-costa-azul": "/images/empreendimentos/mood-costa-azul/01.jpg",
}


def pdf_path_for(slug: str, pdf_name: str) -> Path:
    return SOURCE_OVERRIDES.get(slug, BOOKS_ROOT / pdf_name)


def render_book(slug: str, pdf_name: str) -> list[str]:
    pdf_path = pdf_path_for(slug, pdf_name)
    if not pdf_path.exists():
        raise FileNotFoundError(f"Missing PDF for {slug}: {pdf_path}")

    out_dir = OUTPUT_ROOT / slug / "book-pages"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    matrix = fitz.Matrix(DPI / 72, DPI / 72)
    images = []

    try:
        print(f">> {slug}: {pdf_path.name} ({len(doc)} pages)")
        for page_index, page in enumerate(doc, start=1):
            file_name = f"{page_index:02d}.jpg"
            output_path = out_dir / file_name
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            pix.save(str(output_path), jpg_quality=JPG_QUALITY)
            images.append(f"/images/empreendimentos/{slug}/book-pages/{file_name}")
    finally:
        doc.close()

    return images


def update_data(results: dict[str, list[str]]) -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    known_slugs = set(results)

    for entry in data:
        slug = entry["slug"]
        if slug not in known_slugs:
            continue
        if slug in HERO_FALLBACKS and not entry.get("heroImage"):
            entry["heroImage"] = HERO_FALLBACKS[slug]
        entry["images"] = results[slug]

    missing = known_slugs - {entry["slug"] for entry in data}
    if missing:
        raise ValueError(f"Mapped books without data entries: {sorted(missing)}")

    JSON_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def selected_books() -> dict[str, str]:
    requested = sys.argv[1:]
    if not requested:
        return BOOKS

    unknown = sorted(set(requested) - set(BOOKS))
    if unknown:
        raise ValueError(f"Unknown slug(s): {unknown}")

    return {slug: BOOKS[slug] for slug in requested}


def main() -> None:
    books = selected_books()
    results = {slug: render_book(slug, pdf_name) for slug, pdf_name in books.items()}
    update_data(results)

    total = sum(len(images) for images in results.values())
    print(f"\n[DONE] {total} rendered book pages across {len(results)} empreendimentos")


if __name__ == "__main__":
    main()
