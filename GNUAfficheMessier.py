import os
import re
import io
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass

from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

# ================== CONFIGURATION ==================
ROOT_DIR = r"F:\MyWorks"
OUTPUT_PDF = r"F:\MyWorks\Affiche_Objets_Messier_24x36.pdf"

POSTER_W_IN = 24
POSTER_H_IN = 36

COLS = 11
ROWS = 10  # 110 cases (M001..M110)

MARGIN_IN = 0.4
GAP_IN = 0.08
LABEL_H_IN = 0.23
LABEL_PAD_IN = 0.04
TITLE_AREA_IN = 1.9  # zone réservée au titre/auteur

FONT_MAIN = "Helvetica"
FONT_BOLD = "Helvetica-Bold"

POSTER_TITLE = "Les objets Messier"
POSTER_AUTHOR = "Steve Prud’Homme"

# ================== NOMS MESSIER (FR) - COMPLET 1..110 ==================
MESSIER_NAMES: Dict[int, str] = {
    1: "Nébuleuse du Crabe",
    2: "Amas globulaire",
    3: "Amas globulaire",
    4: "Amas globulaire",
    5: "Amas globulaire",
    6: "Amas du Papillon",
    7: "Amas de Ptolémée",
    8: "Nébuleuse de la Lagune",
    9: "Amas globulaire",
    10: "Amas globulaire",
    11: "Amas du Canard sauvage",
    12: "Amas globulaire",
    13: "Amas d’Hercule",
    14: "Amas globulaire",
    15: "Amas globulaire",
    16: "Nébuleuse de l’Aigle",
    17: "Nébuleuse Oméga",
    18: "Amas ouvert",
    19: "Amas globulaire",
    20: "Nébuleuse Trifide",
    21: "Amas ouvert",
    22: "Amas du Sagittaire",
    23: "Amas ouvert",
    24: "Nuage stellaire du Sagittaire",
    25: "Amas ouvert",
    26: "Amas ouvert",
    27: "Nébuleuse de l’Haltère",
    28: "Amas globulaire",
    29: "Amas ouvert",
    30: "Amas globulaire",
    31: "Galaxie d’Andromède",
    32: "Galaxie naine d’Andromède",
    33: "Galaxie du Triangle",
    34: "Amas ouvert",
    35: "Amas ouvert",
    36: "Amas ouvert",
    37: "Amas ouvert",
    38: "Amas ouvert",
    39: "Amas ouvert",
    40: "Étoile double",
    41: "Amas ouvert",
    42: "Nébuleuse d’Orion",
    43: "Nébuleuse de De Mairan",
    44: "Amas de la Crèche",
    45: "Pléiades",
    46: "Amas ouvert",
    47: "Amas ouvert",
    48: "Amas ouvert",
    49: "Galaxie elliptique",
    50: "Amas ouvert",
    51: "Galaxie du Tourbillon",
    52: "Amas ouvert",
    53: "Amas globulaire",
    54: "Amas globulaire",
    55: "Amas globulaire",
    56: "Amas globulaire",
    57: "Nébuleuse de l’Anneau",
    58: "Galaxie spirale",
    59: "Galaxie elliptique",
    60: "Galaxie elliptique",
    61: "Galaxie spirale",
    62: "Amas globulaire",
    63: "Galaxie du Tournesol",
    64: "Galaxie de l’Œil Noir",
    65: "Galaxie spirale",
    66: "Galaxie spirale",
    67: "Amas ouvert",
    68: "Amas globulaire",
    69: "Amas globulaire",
    70: "Amas globulaire",
    71: "Amas globulaire",
    72: "Amas globulaire",
    73: "Astérisme",
    74: "Galaxie spirale",
    75: "Amas globulaire",
    76: "Petite nébuleuse de l’Haltère",
    77: "Galaxie spirale",
    78: "Nébuleuse par réflexion",
    79: "Amas globulaire",
    80: "Amas globulaire",
    81: "Galaxie de Bode",
    82: "Galaxie du Cigare",
    83: "Galaxie du Moulinet austral",
    84: "Galaxie elliptique",
    85: "Galaxie lenticulaire",
    86: "Galaxie lenticulaire",
    87: "Virgo A",
    88: "Galaxie spirale",
    89: "Galaxie elliptique",
    90: "Galaxie spirale",
    91: "Galaxie spirale barrée",
    92: "Amas globulaire",
    93: "Amas ouvert",
    94: "Galaxie spirale",
    95: "Galaxie spirale barrée",
    96: "Galaxie spirale",
    97: "Nébuleuse du Hibou",
    98: "Galaxie spirale",
    99: "Galaxie spirale",
    100: "Galaxie spirale",
    101: "Galaxie du Moulinet",
    102: "Galaxie lenticulaire (galaxie du Fuseau)",
    103: "Amas ouvert",
    104: "Galaxie du Sombrero",
    105: "Galaxie elliptique",
    106: "Galaxie spirale",
    107: "Amas globulaire",
    108: "Galaxie spirale",
    109: "Galaxie spirale",
    110: "Galaxie naine d’Andromède",
}

# ================== TABLE NGC -> MESSIER ==================
# (Partielle mais utile; tu peux l'étendre. Le DEBUG te dira combien ont été récupérés via NGC.)
NGC_TO_MESSIER: Dict[int, int] = {
    1952: 1, 7089: 2, 5272: 3, 6121: 4, 5904: 5,
    6405: 6, 6475: 7, 6523: 8, 6333: 9, 6254: 10,
    6705: 11, 6218: 12, 6205: 13, 6402: 14, 7078: 15,
    6611: 16, 6618: 17, 6613: 18, 6273: 19, 6514: 20,
    6531: 21, 6656: 22, 6494: 23, 6603: 24, 4725: 25,
    6694: 26, 6853: 27, 6626: 28, 6913: 29, 7099: 30,
    224: 31, 221: 32, 598: 33, 1039: 34, 2168: 35,
    1960: 36, 2099: 37, 1912: 38, 7092: 39,
    2287: 41, 1976: 42, 1982: 43, 2632: 44,
    2437: 46, 2422: 47, 2548: 48, 4472: 49, 2323: 50,
    5194: 51, 7654: 52, 5024: 53, 6715: 54, 6809: 55,
    6779: 56, 6720: 57, 4579: 58, 4621: 59, 4649: 60,
    4303: 61, 6266: 62, 5055: 63, 4826: 64, 3623: 65,
    3627: 66, 2682: 67, 4590: 68, 6637: 69, 6681: 70,
    6838: 71, 6981: 72, 628: 74, 6864: 75, 650: 76,
    1068: 77, 2068: 78, 1904: 79, 6093: 80, 3031: 81,
    3034: 82, 5236: 83, 4374: 84, 4382: 85, 4406: 86,
    4486: 87, 4501: 88, 4552: 89, 4569: 90, 4548: 91,
    6341: 92, 2447: 93, 4736: 94, 3351: 95, 3368: 96,
    3587: 97, 4192: 98, 4254: 99, 4321: 100, 5457: 101,
    5866: 102, 581: 103, 4594: 104, 3379: 105, 4258: 106,
    6171: 107, 3556: 108, 3992: 109, 205: 110,
}

# ================== DÉTECTION ==================
MESSIER_RE = re.compile(r"(?i)(?:\bM\s*0*(\d{1,3})\b|\bMESSIER\s*[-_ ]?\s*0*(\d{1,3})\b)")
NGC_RE = re.compile(r"(?i)\bNGC\s*[-_ ]?\s*0*(\d{1,5})\b")

def is_final_jpeg(filename: str) -> bool:
    fn = filename.lower()
    if not (fn.endswith(".jpg") or fn.endswith(".jpeg")):
        return False
    if "_sub" in fn or "-sub" in fn:
        return False
    if fn.endswith("_thn.jpg") or fn.endswith("_thn.jpeg"):
        return False
    return True

def detect_m_number(text: str) -> Optional[int]:
    m = MESSIER_RE.search(text)
    if not m:
        return None
    val = int(m.group(1) or m.group(2))
    return val if 1 <= val <= 110 else None

def detect_ngc_number(text: str) -> Optional[int]:
    m = NGC_RE.search(text)
    if not m:
        return None
    return int(m.group(1))

def find_messier_images(root: str) -> Dict[int, str]:
    """
    Retourne {messier_num: path_image}
    - détecte d'abord Mxx
    - sinon tente NGC->Messier via table
    - garde le plus gros fichier si doublons
    """
    found: Dict[int, str] = {}
    stats = {
        "final_jpeg": 0,
        "m_direct": 0,
        "ngc_seen": 0,
        "ngc_mapped": 0,
        "ngc_no_map": 0,
        "non_messier": 0,
    }

    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if not is_final_jpeg(fn):
                continue
            stats["final_jpeg"] += 1

            full = os.path.join(dirpath, fn)

            # 1) Messier direct
            mnum = detect_m_number(fn) or detect_m_number(full)
            source = "M"

            # 2) Fallback NGC->M
            if not mnum:
                ngc = detect_ngc_number(fn) or detect_ngc_number(full)
                if ngc is not None:
                    stats["ngc_seen"] += 1
                    mapped = NGC_TO_MESSIER.get(ngc)
                    if mapped is not None:
                        mnum = mapped
                        source = "NGC"
                        stats["ngc_mapped"] += 1
                    else:
                        stats["ngc_no_map"] += 1

            if not mnum:
                stats["non_messier"] += 1
                continue

            # garde le plus gros
            try:
                if mnum not in found or os.path.getsize(full) > os.path.getsize(found[mnum]):
                    found[mnum] = full
            except OSError:
                pass

            if source == "M":
                stats["m_direct"] += 1

    # ===== DEBUG =====
    print(f"[DEBUG] JPEG finaux détectés (hors sub/thn): {stats['final_jpeg']}")
    print(f"[DEBUG] Messier matchés au total: {len(found)}/110")
    print(f"[DEBUG] Match direct Mxx: {stats['m_direct']}")
    print(f"[DEBUG] NGC détectés (dans noms/chemins): {stats['ngc_seen']}")
    print(f"[DEBUG] Match via NGC→M: {stats['ngc_mapped']}")
    print(f"[DEBUG] NGC sans correspondance: {stats['ngc_no_map']}")
    print(f"[DEBUG] Fichiers non Messier (ni Mxx ni NGC→M): {stats['non_messier']}")

    if found:
        print("[DEBUG] Exemples matchés (jusqu'à 10):")
        for m in sorted(found.keys())[:10]:
            print(f"   M{m:03d} -> {found[m]}")

    missing = [m for m in range(1, 111) if m not in found]
    print(f"[DEBUG] Messier manquants: {len(missing)}")
    if missing:
        print("[DEBUG] Liste manquants (compact):")
        chunks = []
        start = prev = missing[0]
        for x in missing[1:]:
            if x == prev + 1:
                prev = x
                continue
            chunks.append((start, prev))
            start = prev = x
        chunks.append((start, prev))
        txt = ", ".join([f"M{a:03d}" if a == b else f"M{a:03d}-M{b:03d}" for a, b in chunks])
        print("   " + txt)

    return found

# ================== MISE EN PAGE ==================
@dataclass
class Cell:
    x: float
    y: float
    w: float
    h: float

def build_grid_cells(x0: float, y0: float, w: float, h: float) -> List[Tuple[int, Cell]]:
    gap = GAP_IN * inch
    cw = (w - (COLS - 1) * gap) / COLS
    ch = (h - (ROWS - 1) * gap) / ROWS
    cells: List[Tuple[int, Cell]] = []
    idx = 1
    for r in range(ROWS):
        for c in range(COLS):
            x = x0 + c * (cw + gap)
            y = y0 + (ROWS - 1 - r) * (ch + gap)
            cells.append((idx, Cell(x, y, cw, ch)))
            idx += 1
    return cells

def draw_title(c: canvas.Canvas, pw: float, ph: float):
    c.setFillColorRGB(1, 1, 1)  # blanc
    c.setFont(FONT_BOLD, 48)
    c.drawCentredString(pw / 2, ph - 0.95 * inch, POSTER_TITLE)
    c.setFont(FONT_MAIN, 16)
    c.drawCentredString(pw / 2, ph - 1.38 * inch, POSTER_AUTHOR)

def draw_black_rect(c: canvas.Canvas, cell: Cell):
    c.setFillColorRGB(0, 0, 0)
    c.rect(cell.x, cell.y, cell.w, cell.h, fill=1, stroke=0)

def draw_label(c: canvas.Canvas, cell: Cell, text: str):
    lh = LABEL_H_IN * inch
    pad = LABEL_PAD_IN * inch
    c.setFillColorRGB(0, 0, 0)
    c.rect(cell.x, cell.y, cell.w, lh, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont(FONT_MAIN, 8)
    c.drawString(cell.x + pad, cell.y + 6, text[:120])

def draw_image_robust(c: canvas.Canvas, path: str, cell: Cell):
    lh = LABEL_H_IN * inch
    avail_w = cell.w
    avail_h = cell.h - lh
    ix, iy = cell.x, cell.y + lh

    with Image.open(path) as im:
        im = im.convert("RGB")
        w, h = im.size
        if w <= 0 or h <= 0:
            return

        scale = min(avail_w / w, avail_h / h)
        nw, nh = w * scale, h * scale
        x = ix + (avail_w - nw) / 2
        y = iy + (avail_h - nh) / 2

        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=92)
        buf.seek(0)

        c.drawImage(ImageReader(buf), x, y, nw, nh)

def make_poster_pdf():
    pw, ph = POSTER_W_IN * inch, POSTER_H_IN * inch
    margin = MARGIN_IN * inch
    title_area = TITLE_AREA_IN * inch

    # ===== scan + debug =====
    images = find_messier_images(ROOT_DIR)

    c = canvas.Canvas(OUTPUT_PDF, pagesize=(pw, ph))

    # fond noir global
    c.setFillColorRGB(0, 0, 0)
    c.rect(0, 0, pw, ph, fill=1, stroke=0)

    grid_x = margin
    grid_y = margin
    grid_w = pw - 2 * margin
    grid_h = ph - 2 * margin - title_area

    for mnum, cell in build_grid_cells(grid_x, grid_y, grid_w, grid_h):
        draw_black_rect(c, cell)

        p = images.get(mnum)
        if p:
            try:
                draw_image_robust(c, p, cell)
            except Exception as e:
                print(f"[WARN] Insertion image échouée pour M{mnum:03d}: {e}")

        label = f"M{mnum:03d} — {MESSIER_NAMES.get(mnum, 'Objet Messier')}"
        draw_label(c, cell, label)

    # titre par-dessus tout
    draw_title(c, pw, ph)

    c.showPage()
    c.save()
    print(f"[OK] PDF généré : {OUTPUT_PDF}")

if __name__ == "__main__":
    make_poster_pdf()
