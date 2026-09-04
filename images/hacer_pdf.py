"""Catálogo PDF: fotos JPEG comprimidas + texto vectorial."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Brand:
    out_name: str
    pdf_title: str
    pdf_author: str
    header_left: str
    cover_title: str
    cover_sub: str
    cover_kicker: str
    notes: tuple[str, ...]
    edition: str
    cover_footer_left: str
    cover_footer_right: str
    lots_kicker: str
    lots_blurb: str
    lots_footer_left: str
    use_logo: bool
    handmade: str


YANA = Brand(
    out_name="catalogo.pdf",
    pdf_title="Yana Yavorskaya · Selección privada · Septiembre 2026",
    pdf_author="Yana Yavorskaya Atelier",
    header_left="YANA YAVORSKAYA",
    cover_title="SELECCIÓN PRIVADA",
    cover_sub="MODA  Y  CALZADO",
    cover_kicker="PRECIOS NEGOCIABLES  ·  MADRID",
    notes=("Precios abiertos a ofertas", "Envío o entrega en mano", "Medidas exactas bajo petición"),
    edition="EDICIÓN PRIVADA  ·  SEPTIEMBRE 2026",
    cover_footer_left="Yana Yavorskaya Atelier",
    cover_footer_right="Contacto bajo petición",
    lots_kicker="PACK EXCLUSIVO",
    lots_blurb=(
        "Los precios de ficha siguen abiertos a oferta. El lote completo se cierra a precio de liquidación, "
        "a convenir. Para medidas, envío o entrega en mano: contacto bajo petición."
    ),
    lots_footer_left="Yana Yavorskaya Atelier",
    use_logo=True,
    handmade="Confección propia",
)

WALLAPOP = Brand(
    out_name="catalogo-wallapop.pdf",
    pdf_title="Venta particular · Ropa y calzado · Madrid",
    pdf_author="Venta particular",
    header_left="VENTA PARTICULAR",
    cover_title="ROPA Y CALZADO",
    cover_sub="VENTA PARTICULAR",
    cover_kicker="MADRID  ·  PRECIOS NEGOCIABLES",
    notes=(
        "Soy particular, no empresa",
        "Envío por Wallapop o entrega en Madrid",
        "Dudas y ofertas por el chat",
    ),
    edition="SEPTIEMBRE 2026",
    cover_footer_left="Particular · Madrid",
    cover_footer_right="Chat de Wallapop",
    lots_kicker="SI TE LLEVAS VARIOS",
    lots_blurb=(
        "Precios abiertos a oferta. Si te llevas más de una cosa, se puede hablar. "
        "Envío por Wallapop o quedamos en Madrid. Pregunta por el chat."
    ),
    lots_footer_left="Particular · Madrid",
    use_logo=False,
    handmade="Hecha a mano",
)
PAGE_W, PAGE_H = A4
MARGIN = 42
INK = HexColor("#1c1916")
GOLD = HexColor("#b08968")
GOLD_DEEP = HexColor("#8a6a4e")
MUTED = HexColor("#6a635a")
LINE = HexColor("#ddd6cb")
PAPER = HexColor("#fbfaf7")
FRAME_BG = HexColor("#efebe3")

WIN = Path(r"C:\Windows\Fonts")
pdfmetrics.registerFont(TTFont("Georgia", str(WIN / "georgia.ttf")))
pdfmetrics.registerFont(TTFont("Georgia-Bold", str(WIN / "georgiab.ttf")))
pdfmetrics.registerFont(TTFont("Georgia-Italic", str(WIN / "georgiai.ttf")))
pdfmetrics.registerFont(TTFont("Calibri", str(WIN / "calibri.ttf")))
pdfmetrics.registerFont(TTFont("Calibri-Bold", str(WIN / "calibrib.ttf")))
pdfmetrics.registerFont(TTFont("Calibri-Italic", str(WIN / "calibrii.ttf")))


_JPEG_CACHE: dict[str, bytes] = {}


def jpeg_bytes(path: Path, quality: int = 70, max_side: int = 1100) -> bytes:
    key = str(path)
    if key in _JPEG_CACHE:
        return _JPEG_CACHE[key]
    with Image.open(path) as im:
        im = im.convert("RGB")
        w, h = im.size
        longest = max(w, h)
        if longest > max_side:
            scale = max_side / longest
            im = im.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.Resampling.LANCZOS)
        buf = BytesIO()
        im.save(buf, format="JPEG", quality=quality, optimize=True, progressive=True, subsampling=2)
    data = buf.getvalue()
    _JPEG_CACHE[key] = data
    return data


def draw_header(c: canvas.Canvas, brand: Brand, right: str) -> None:
    y = PAGE_H - 36
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(MARGIN, y - 10, PAGE_W - MARGIN, y - 10)
    c.setFillColor(GOLD_DEEP)
    c.setFont("Calibri", 8)
    c.drawString(MARGIN, y, brand.header_left)
    c.setFillColor(GOLD)
    c.setFont("Calibri-Italic", 8)
    c.drawRightString(PAGE_W - MARGIN, y, right)


def draw_footer(c: canvas.Canvas, left: str, num: str, right: str) -> None:
    y = 28
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(MARGIN, y + 12, PAGE_W - MARGIN, y + 12)
    c.setFillColor(HexColor("#b8b0a4"))
    c.setFont("Calibri", 7)
    c.drawString(MARGIN, y, left.upper())
    c.drawRightString(PAGE_W - MARGIN, y, right.upper())
    c.setFillColor(GOLD)
    c.drawCentredString(PAGE_W / 2, y, num)


def contain(path: Path, box_w: float, box_h: float) -> tuple[float, float]:
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(box_w / iw, box_h / ih)
    return iw * scale, ih * scale


def draw_photo(c: canvas.Canvas, path: Path, x: float, y: float, box_w: float, box_h: float) -> None:
    c.setFillColor(Color(1, 1, 1))
    c.rect(x, y, box_w, box_h, fill=1, stroke=0)
    dw, dh = contain(path, box_w - 8, box_h - 8)
    ix = x + (box_w - dw) / 2
    iy = y + (box_h - dh) / 2
    img = ImageReader(BytesIO(jpeg_bytes(path)))
    c.drawImage(img, ix, iy, width=dw, height=dh, preserveAspectRatio=True, anchor="c", mask="auto")


def product_page(
    c: canvas.Canvas,
    brand: Brand,
    *,
    kicker: str,
    title: str,
    tags: list[str],
    images: list[str],
    desc: str,
    price: str,
    ref: str,
    header_right: str,
    footer_left: str,
    num: str,
    footer_right: str,
) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_header(c, brand, header_right)

    y = PAGE_H - 68
    c.setFillColor(GOLD_DEEP)
    c.setFont("Calibri", 8)
    c.drawString(MARGIN, y, kicker.upper())
    y -= 26
    c.setFillColor(INK)
    c.setFont("Georgia-Bold", 24)
    c.drawString(MARGIN, y, title)

    y -= 22
    x = MARGIN
    for tag in tags:
        c.setStrokeColor(LINE)
        c.setFillColor(GOLD_DEEP)
        c.setFont("Calibri", 7.5)
        tw = c.stringWidth(tag.upper(), "Calibri", 7.5)
        c.rect(x, y - 4, tw + 14, 14, fill=0, stroke=1)
        c.drawString(x + 7, y, tag.upper())
        x += tw + 22

    gallery_top = y - 18
    gallery_h = 430
    gallery_y = gallery_top - gallery_h
    inner_w = PAGE_W - 2 * MARGIN
    c.setFillColor(FRAME_BG)
    c.rect(MARGIN - 6, gallery_y - 6, inner_w + 12, gallery_h + 12, fill=1, stroke=0)

    paths = [ROOT / name for name in images]
    if len(paths) == 1:
        draw_photo(c, paths[0], MARGIN, gallery_y, inner_w, gallery_h)
    else:
        gap = 8
        col_w = (inner_w - gap) / 2
        draw_photo(c, paths[0], MARGIN, gallery_y, col_w, gallery_h)
        draw_photo(c, paths[1], MARGIN + col_w + gap, gallery_y, col_w, gallery_h)

    y = gallery_y - 22
    c.setFillColor(HexColor("#4d473f"))
    c.setFont("Georgia-Italic", 11)
    for line in _wrap(c, desc, "Georgia-Italic", 11, inner_w):
        c.drawString(MARGIN, y, line)
        y -= 15

    y -= 8
    c.setStrokeColor(LINE)
    c.setDash(1, 2)
    c.line(MARGIN, y + 10, PAGE_W - MARGIN, y + 10)
    c.setDash()
    c.setFillColor(INK)
    c.setFont("Georgia-Bold", 26)
    c.drawString(MARGIN, y - 12, price)
    c.setFillColor(GOLD)
    c.setFont("Calibri", 9)
    c.drawString(MARGIN + c.stringWidth(price, "Georgia-Bold", 26) + 10, y - 6, "NEGOCIABLE")
    c.drawRightString(PAGE_W - MARGIN, y - 6, ref.upper())

    draw_footer(c, footer_left, num, footer_right)
    c.showPage()


def _wrap(c: canvas.Canvas, text: str, font: str, size: float, width: float) -> list[str]:
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if c.stringWidth(trial, font, size) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def cover(c: canvas.Canvas, brand: Brand) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    title_y = PAGE_H / 2 + 52
    if brand.use_logo:
        logo = ROOT.parent / "logo-yy.png"
        if logo.exists():
            with Image.open(logo) as im:
                lw, lh = im.size
            dw = 64
            dh = dw * lh / lw
            c.drawImage(str(logo), (PAGE_W - dw) / 2, PAGE_H / 2 + 110, width=dw, height=dh, mask="auto")

    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(PAGE_W / 2 - 28, title_y + 40, PAGE_W / 2 + 28, title_y + 40)

    c.setFillColor(INK)
    c.setFont("Georgia", 28)
    c.drawCentredString(PAGE_W / 2, title_y, brand.cover_title)
    c.setFillColor(GOLD)
    c.setFont("Georgia", 12)
    c.drawCentredString(PAGE_W / 2, title_y - 22, brand.cover_sub)

    c.setStrokeColor(GOLD)
    c.line(PAGE_W / 2 - 28, title_y - 36, PAGE_W / 2 + 28, title_y - 36)

    c.setFillColor(GOLD_DEEP)
    c.setFont("Calibri", 9)
    c.drawCentredString(PAGE_W / 2, title_y - 60, brand.cover_kicker)

    c.setStrokeColor(LINE)
    c.line(PAGE_W / 2 - 140, title_y - 92, PAGE_W / 2 + 140, title_y - 92)
    c.setFillColor(MUTED)
    c.setFont("Calibri", 10)
    ny = title_y - 110
    for n in brand.notes:
        c.drawCentredString(PAGE_W / 2, ny, n)
        ny -= 16
    c.setStrokeColor(LINE)
    c.line(PAGE_W / 2 - 140, ny - 4, PAGE_W / 2 + 140, ny - 4)

    c.setFillColor(HexColor("#b8b0a4"))
    c.setFont("Calibri", 8)
    c.drawCentredString(PAGE_W / 2, 56, brand.edition)
    draw_footer(c, brand.cover_footer_left, "01", brand.cover_footer_right)
    c.showPage()


def lots_page(c: canvas.Canvas, brand: Brand) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_header(c, brand, "Ofertas por lote")

    box_y = PAGE_H / 2 - 20
    c.setFillColor(HexColor("#f3efe7"))
    c.setStrokeColor(LINE)
    c.rect(MARGIN, box_y, PAGE_W - 2 * MARGIN, 220, fill=1, stroke=1)

    c.setFillColor(INK)
    c.setFont("Georgia", 20)
    c.drawCentredString(PAGE_W / 2, box_y + 175, "OFERTAS POR LOTE")
    c.setFillColor(GOLD)
    c.setFont("Calibri", 8)
    c.drawCentredString(PAGE_W / 2, box_y + 158, brand.lots_kicker)

    cards = [
        ("PACK 2 FALDAS", "35 €", "Combinación libre"),
        ("PACK CALZADO", "85 €", "Los tres pares"),
        ("LOTE COMPLETO", "Consultar", "Precio de liquidación"),
    ]
    gap = 12
    card_w = (PAGE_W - 2 * MARGIN - 48 - 2 * gap) / 3
    cx = MARGIN + 24
    for name, val, note in cards:
        c.setFillColor(Color(1, 1, 1))
        c.setStrokeColor(LINE)
        c.rect(cx, box_y + 28, card_w, 110, fill=1, stroke=1)
        c.setFillColor(GOLD_DEEP)
        c.setFont("Calibri", 7.5)
        c.drawCentredString(cx + card_w / 2, box_y + 112, name)
        c.setFillColor(INK)
        c.setFont("Georgia-Bold", 22)
        c.drawCentredString(cx + card_w / 2, box_y + 72, val)
        c.setFillColor(MUTED)
        c.setFont("Calibri-Italic", 8)
        c.drawCentredString(cx + card_w / 2, box_y + 48, note)
        cx += card_w + gap

    c.setFillColor(HexColor("#4d473f"))
    c.setFont("Georgia-Italic", 11)
    text = brand.lots_blurb
    y = box_y - 36
    for line in _wrap(c, text, "Georgia-Italic", 11, PAGE_W - 2 * MARGIN):
        c.drawString(MARGIN, y, line)
        y -= 16

    draw_footer(c, brand.lots_footer_left, "12", "Septiembre 2026")
    c.showPage()


def main(brand: Brand = YANA) -> None:
    out = ROOT / brand.out_name
    c = canvas.Canvas(str(out), pagesize=A4)
    c.setTitle(brand.pdf_title)
    c.setAuthor(brand.pdf_author)

    products = [
        dict(
            kicker="Blusa",
            title="Blusa Camuflaje",
            tags=["Talla M", "Excelente estado"],
            images=["blusa-camuflaje.jpeg"],
            desc="Diseño casual, tejido fluido y estampado militar en tonos rosa, azul y marrón.",
            price="20 €",
            ref="Ref. 01",
            header_right="Prendas · Ref. 01",
            footer_left="Prendas de vestir",
            num="02",
            footer_right="Envío · Entrega en mano",
        ),
        dict(
            kicker="Falda",
            title="Falda Tejano Corazones",
            tags=["Talla M", "Nueva · Confección propia"],
            images=["falda-tejano-1.jpeg", "falda-tejano-2.jpeg"],
            desc="Corte en A, pieza artesanal en denim con estampado de corazones y bajo deshilachado.",
            price="20 €",
            ref="Ref. 02",
            header_right="Prendas · Ref. 02",
            footer_left="Prendas de vestir",
            num="03",
            footer_right="Envío · Entrega en mano",
        ),
        dict(
            kicker="Falda",
            title="Falda Estampada Azul",
            tags=["Talla L", "Nueva"],
            images=["falda-estampada-azul.jpeg"],
            desc="Estampado de puntos azules y violetas, ligera y con forro interior.",
            price="20 €",
            ref="Ref. 03",
            header_right="Prendas · Ref. 03",
            footer_left="Prendas de vestir",
            num="04",
            footer_right="Medidas exactas bajo petición",
        ),
        dict(
            kicker="Falda",
            title="Falda Espiga Lana",
            tags=["Talla M", "Muy bien cuidada"],
            images=["falda-espiga-1.jpeg", "falda-espiga-2.jpeg"],
            desc="Lana de alta calidad, detalle de volantes y cinta inferior en tono oscuro.",
            price="20 €",
            ref="Ref. 04",
            header_right="Prendas · Ref. 04",
            footer_left="Prendas de vestir",
            num="05",
            footer_right="Medidas exactas bajo petición",
        ),
        dict(
            kicker="Falda",
            title="Falda Floral Crema",
            tags=["Talla M", "Excelente estado"],
            images=["falda-floral-1.jpeg", "falda-floral-2.jpeg"],
            desc="Talle alto con abotonadura frontal y vuelo romántico, estampado floral en rosa y verde.",
            price="20 €",
            ref="Ref. 05",
            header_right="Prendas · Ref. 05",
            footer_left="Prendas de vestir",
            num="06",
            footer_right="Medidas exactas bajo petición",
        ),
        dict(
            kicker="Falda",
            title="Falda Patchwork Boho",
            tags=["Talla M", "Excelente · Confección propia"],
            images=["falda-patchwork-1.jpeg", "falda-patchwork-2.jpeg"],
            desc="Combinación de paneles cálidos y encajes en naranja, amarillo y blanco, con costura vista.",
            price="25 €",
            ref="Ref. 06",
            header_right="Prendas · Ref. 06",
            footer_left="Prendas de vestir",
            num="07",
            footer_right="Confección propia",
        ),
        dict(
            kicker="Falda",
            title="Falda Encaje Menta",
            tags=["Talla M", "Excelente · Confección propia"],
            images=["falda-encaje-menta.jpeg"],
            desc="Diseño romántico en capas, bordados dorados y cintas en tono menta sobre encaje beige.",
            price="25 €",
            ref="Ref. 07",
            header_right="Prendas · Ref. 07",
            footer_left="Prendas de vestir",
            num="08",
            footer_right="Confección propia",
        ),
        dict(
            kicker="Zapatos",
            title="Zapatos Tacón Azules",
            tags=["Talla 37", "Buen estado"],
            images=["zapatos-tacon-1.jpeg", "zapatos-tacon-2.jpeg"],
            desc="Ante azul eléctrico con tira de ajuste al tobillo y tacón fino.",
            price="25 €",
            ref="Ref. 08",
            header_right="Calzado · Ref. 08",
            footer_left="Calzado",
            num="09",
            footer_right="Piel, charol y ante",
        ),
        dict(
            kicker="Botines",
            title="Botines Oxford Piel",
            tags=["Talla 37", "Muy buen estado"],
            images=["botines-oxford-1.jpeg", "botines-oxford-2.jpeg"],
            desc="Piel vacuna en tono camel, brogue, cordones y cremallera interior.",
            price="30 €",
            ref="Ref. 09",
            header_right="Calzado · Ref. 09",
            footer_left="Calzado",
            num="10",
            footer_right="Piel, charol y ante",
        ),
        dict(
            kicker="Zapatos",
            title="Zapatos Charol Café",
            tags=["Talla 37", "Nuevo · Sin estrenar", "Zinda"],
            images=["zapatos-charol-1.jpeg", "zapatos-charol-2.jpeg"],
            desc="Marca Zinda, charol de piel con detalle de flecos en la punta.",
            price="45 €",
            ref="Ref. 10",
            header_right="Calzado · Ref. 10",
            footer_left="Calzado",
            num="11",
            footer_right="Piel, charol y ante",
        ),
    ]

    cover(c, brand)
    for p in products:
        p = dict(p)
        p["tags"] = [t.replace("Confección propia", brand.handmade) for t in p["tags"]]
        p["footer_right"] = p["footer_right"].replace("Confección propia", brand.handmade)
        product_page(c, brand, **p)
    lots_page(c, brand)
    c.save()
    print(f"PDF escrito: {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--wallapop", action="store_true", help="Versión particular, sin marca Yana")
    args = parser.parse_args()
    main(WALLAPOP if args.wallapop else YANA)
