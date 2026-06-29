# -*- coding: utf-8 -*-
"""
Generador de presentación ejecutiva — Howy
Tema: Herramientas e IAs para creación, generación y edición de video (2026)
Diseño corporativo limpio. Salida: PowerPoint (.pptx) 16:9.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ----------------------------------------------------------------------------
# SISTEMA DE DISEÑO — MARCA HOWY
# ----------------------------------------------------------------------------
NAVY      = RGBColor(0x0E, 0x21, 0x3A)   # azul marino profundo (primario oscuro)
BLUE      = RGBColor(0x2D, 0x6C, 0xDF)   # azul Howy (primario)
CYAN      = RGBColor(0x18, 0xC2, 0xD6)   # cian (acento)
AMBER     = RGBColor(0xF5, 0xA6, 0x23)   # ámbar (resaltes / alertas)
INK       = RGBColor(0x1A, 0x24, 0x32)   # texto principal
GRAY      = RGBColor(0x5B, 0x66, 0x74)   # texto secundario
LIGHT     = RGBColor(0xF4, 0xF7, 0xFB)   # fondo claro de tarjetas
LINE      = RGBColor(0xD9, 0xE0, 0xE9)   # líneas / divisores
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
GREEN     = RGBColor(0x27, 0xAE, 0x60)   # positivo

FONT_H = "Calibri"      # encabezados
FONT_B = "Calibri"      # cuerpo

EMU_W, EMU_H = Inches(13.333), Inches(7.5)

prs = Presentation()
prs.slide_width = EMU_W
prs.slide_height = EMU_H
BLANK = prs.slide_layouts[6]


# ----------------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------------
def slide():
    return prs.slides.add_slide(BLANK)


def rect(s, x, y, w, h, color, line_color=None, line_w=None):
    sp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    sp.fill.solid()
    sp.fill.fore_color.rgb = color
    if line_color is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line_color
        sp.line.width = line_w or Pt(0.75)
    sp.shadow.inherit = False
    return sp


def rounded(s, x, y, w, h, color, line_color=None, line_w=None):
    sp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    try:
        sp.adjustments[0] = 0.06
    except Exception:
        pass
    sp.fill.solid()
    sp.fill.fore_color.rgb = color
    if line_color is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line_color
        sp.line.width = line_w or Pt(1)
    sp.shadow.inherit = False
    return sp


def txt(s, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
        space_after=4, line_spacing=1.0, wrap=True):
    """runs: lista de párrafos; cada párrafo es lista de (texto, size, color, bold, italic)."""
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space_after)
        p.space_before = Pt(0)
        p.line_spacing = line_spacing
        for (t, sz, col, bold, ital) in para:
            r = p.add_run()
            r.text = t
            r.font.size = Pt(sz)
            r.font.color.rgb = col
            r.font.bold = bold
            r.font.italic = ital
            r.font.name = FONT_H if bold else FONT_B
    return tb


def P(text, size, color, bold=False, ital=False):
    return [(text, size, color, bold, ital)]


def footer(s, page):
    txt(s, Inches(0.55), Inches(7.04), Inches(6), Inches(0.32),
        [[("Howy", 9, BLUE, True, False),
          ("  ·  Herramientas de IA para video — 2026", 9, GRAY, False, False)]],
        anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(11.8), Inches(7.04), Inches(1.0), Inches(0.32),
        [P(f"{page:02d}", 9, GRAY, False)], align=PP_ALIGN.RIGHT,
        anchor=MSO_ANCHOR.MIDDLE)


def header(s, kicker, title, page):
    """Encabezado estándar de slide de contenido."""
    rect(s, 0, 0, EMU_W, Inches(1.18), WHITE)
    rect(s, Inches(0.55), Inches(0.42), Inches(0.09), Inches(0.5), BLUE)
    txt(s, Inches(0.78), Inches(0.30), Inches(11.5), Inches(0.28),
        [P(kicker.upper(), 11, BLUE, True)])
    txt(s, Inches(0.78), Inches(0.54), Inches(11.9), Inches(0.55),
        [P(title, 26, NAVY, True)])
    rect(s, Inches(0.55), Inches(1.18), Inches(12.23), Pt(1.2), LINE)
    footer(s, page)


def chip(s, x, y, w, label, color):
    c = rounded(s, x, y, w, Inches(0.34), color)
    txt(s, x, y, w, Inches(0.34), [P(label, 10.5, WHITE, True)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return c


# ----------------------------------------------------------------------------
# 1. PORTADA
# ----------------------------------------------------------------------------
s = slide()
rect(s, 0, 0, EMU_W, EMU_H, NAVY)
# banda de acento diagonal-ish (barras)
rect(s, 0, Inches(6.7), EMU_W, Inches(0.12), BLUE)
rect(s, 0, Inches(6.82), EMU_W, Inches(0.06), CYAN)
# logo simple Howy
rounded(s, Inches(0.85), Inches(0.8), Inches(0.62), Inches(0.62), BLUE)
txt(s, Inches(0.85), Inches(0.8), Inches(0.62), Inches(0.62),
    [P("H", 30, WHITE, True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(1.62), Inches(0.8), Inches(5), Inches(0.62),
    [P("Howy", 26, WHITE, True)], anchor=MSO_ANCHOR.MIDDLE)

txt(s, Inches(0.85), Inches(2.55), Inches(11.6), Inches(0.4),
    [P("PRESENTACIÓN EJECUTIVA", 14, CYAN, True)])
txt(s, Inches(0.85), Inches(3.0), Inches(11.7), Inches(1.8),
    [P("Aplicaciones e IAs para crear,", 44, WHITE, True),
     P("generar y editar video", 44, WHITE, True)], line_spacing=1.02)
txt(s, Inches(0.85), Inches(5.05), Inches(11.0), Inches(0.7),
    [P("Soluciones fáciles de usar, gratuitas o de bajo costo, con conexión a IA",
       17, RGBColor(0xC6, 0xD3, 0xE6), False)])
txt(s, Inches(0.85), Inches(6.95), Inches(8), Inches(0.4),
    [[("Investigación y análisis de mercado", 11, RGBColor(0x9F, 0xB2, 0xCD), False, False)]])
txt(s, Inches(9.5), Inches(6.95), Inches(2.95), Inches(0.4),
    [P("Junio 2026", 11, RGBColor(0x9F, 0xB2, 0xCD), False)], align=PP_ALIGN.RIGHT)


# ----------------------------------------------------------------------------
# 2. RESUMEN EJECUTIVO
# ----------------------------------------------------------------------------
s = slide()
header(s, "Resumen ejecutivo", "Lo esencial en un vistazo", 2)
intro = ("El mercado de video con IA en 2026 está maduro: existen herramientas potentes, "
         "fáciles de usar y con planes gratuitos o económicos. Evaluamos más de 15 soluciones "
         "en cinco categorías para identificar las de mejor relación valor-costo y mayor "
         "capacidad de conexión con IA.")
txt(s, Inches(0.78), Inches(1.45), Inches(11.8), Inches(0.9),
    [P(intro, 14.5, GRAY, False)], line_spacing=1.15)

cards = [
    ("5", "categorías", "Generación, edición, avatares,\ntodo-en-uno y automatización."),
    ("15+", "herramientas", "Analizadas por facilidad,\ncosto y conexión con IA."),
    ("$0", "para empezar", "Todas tienen plan gratis\no de prueba sin tarjeta."),
    ("API", "conectable", "Integrables con ChatGPT\ny flujos automatizados."),
]
cw, gap = Inches(2.85), Inches(0.18)
x0 = Inches(0.78)
y0 = Inches(2.7)
for i, (big, small, desc) in enumerate(cards):
    x = x0 + i * (cw + gap)
    rounded(s, x, y0, cw, Inches(2.1), LIGHT)
    rect(s, x, y0, cw, Inches(0.09), BLUE)
    txt(s, x + Inches(0.22), y0 + Inches(0.28), cw - Inches(0.4), Inches(0.7),
        [[(big, 38, BLUE, True, False), ("  " + small, 14, NAVY, True, False)]],
        anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x + Inches(0.22), y0 + Inches(1.05), cw - Inches(0.44), Inches(1.0),
        [P(l, 12, GRAY, False) for l in desc.split("\n")], line_spacing=1.1)

# barra de conclusión
rounded(s, Inches(0.78), Inches(5.25), Inches(11.78), Inches(1.35), NAVY)
txt(s, Inches(1.1), Inches(5.45), Inches(11.2), Inches(0.95),
    [[("Recomendación clave:  ", 14.5, CYAN, True, False),
      ("para empezar sin costo combine ", 14.5, WHITE, False, False),
      ("CapCut", 14.5, WHITE, True, False),
      (" (edición) + ", 14.5, WHITE, False, False),
      ("Kling 3.0", 14.5, WHITE, True, False),
      (" (generación barata) + ", 14.5, WHITE, False, False),
      ("OpusClip", 14.5, WHITE, True, False),
      (" (clips). Para empresa, sume ", 14.5, WHITE, False, False),
      ("HeyGen/Synthesia", 14.5, WHITE, True, False),
      (" e integre todo vía API con ChatGPT.", 14.5, WHITE, False, False)]],
    anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.18)


# ----------------------------------------------------------------------------
# 3. METODOLOGÍA / CRITERIOS
# ----------------------------------------------------------------------------
s = slide()
header(s, "Metodología", "Criterios de evaluación", 3)
crit = [
    ("Facilidad de uso", "¿Cualquier persona logra un resultado pulido en minutos, sin curva técnica?", CYAN),
    ("Costo", "Disponibilidad de plan gratuito y precio de los planes de pago accesibles.", BLUE),
    ("Conexión con IA", "Integración con ChatGPT, API o flujos automatizados de generación.", AMBER),
    ("Calidad y alcance", "Resolución, idiomas, duración y consistencia de los resultados.", GREEN),
]
y = Inches(1.55)
for i, (t, d, c) in enumerate(crit):
    yy = y + i * Inches(1.32)
    rounded(s, Inches(0.78), yy, Inches(11.78), Inches(1.15), LIGHT)
    rect(s, Inches(0.78), yy, Inches(0.12), Inches(1.15), c)
    rounded(s, Inches(1.15), yy + Inches(0.27), Inches(0.62), Inches(0.62), c)
    txt(s, Inches(1.15), yy + Inches(0.27), Inches(0.62), Inches(0.62),
        [P(str(i + 1), 24, WHITE, True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(2.05), yy + Inches(0.18), Inches(10.2), Inches(0.45),
        [P(t, 17, NAVY, True)])
    txt(s, Inches(2.05), yy + Inches(0.6), Inches(10.2), Inches(0.45),
        [P(d, 12.5, GRAY, False)])


# ----------------------------------------------------------------------------
# 4. PANORAMA — 5 CATEGORÍAS
# ----------------------------------------------------------------------------
s = slide()
header(s, "Panorama", "El ecosistema en 5 categorías", 4)
cats = [
    ("01", "Generación con IA", "Texto/imagen → video", "Veo · Kling · Runway · Pika · Luma", BLUE),
    ("02", "Edición con IA", "Cortar, subtítulos, limpiar", "CapCut · Descript · DaVinci", CYAN),
    ("03", "Avatares con IA", "Presentador virtual que habla", "HeyGen · Synthesia", AMBER),
    ("04", "Todo-en-uno", "Guion → video automático", "Pictory · InVideo · VEED · Canva", GREEN),
    ("05", "Automatización", "API y flujos con ChatGPT", "OpusClip · Shotstack · Fliki", NAVY),
]
cw = Inches(2.3)
gap = Inches(0.12)
x0 = Inches(0.78)
y0 = Inches(1.7)
for i, (n, t, sub, tools, c) in enumerate(cats):
    x = x0 + i * (cw + gap)
    rounded(s, x, y0, cw, Inches(4.6), LIGHT)
    rect(s, x, y0, cw, Inches(0.7), c)
    txt(s, x, y0 + Inches(0.05), cw, Inches(0.6),
        [P(n, 30, WHITE, True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x + Inches(0.18), y0 + Inches(0.95), cw - Inches(0.36), Inches(0.85),
        [P(t, 16, NAVY, True)], align=PP_ALIGN.CENTER, line_spacing=1.0)
    txt(s, x + Inches(0.18), y0 + Inches(1.85), cw - Inches(0.36), Inches(0.7),
        [P(sub, 12, GRAY, True)], align=PP_ALIGN.CENTER, line_spacing=1.05)
    rect(s, x + Inches(0.4), y0 + Inches(2.7), cw - Inches(0.8), Pt(1), LINE)
    txt(s, x + Inches(0.18), y0 + Inches(2.95), cw - Inches(0.36), Inches(1.5),
        [P(tools, 12, c, True)], align=PP_ALIGN.CENTER, line_spacing=1.25)


# ----------------------------------------------------------------------------
# Helper: slide de categoría con tabla de tarjetas de herramientas
# ----------------------------------------------------------------------------
def tool_cards_slide(kicker, title, page, accent, tools, note=None):
    s = slide()
    header(s, kicker, title, page)
    n = len(tools)
    top = Inches(1.5)
    bottom = Inches(6.55) if note else Inches(6.8)
    avail = bottom - top
    ch = Emu(int(avail / n))
    inner_pad = Inches(0.14)
    for i, (name, badges, desc) in enumerate(tools):
        y = top + Emu(int(ch * i)) + (inner_pad if i else Emu(0))
        hh = ch - inner_pad
        rounded(s, Inches(0.78), y, Inches(11.78), hh, LIGHT)
        rect(s, Inches(0.78), y, Inches(0.12), hh, accent)
        # nombre
        txt(s, Inches(1.15), y, Inches(3.05), hh,
            [P(name, 17, NAVY, True)], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.0)
        # badges
        bx = Inches(4.25)
        by = y + Emu(int(hh / 2)) - Inches(0.17)
        for (blabel, bcolor) in badges:
            w = Inches(0.16 + 0.092 * len(blabel))
            chip(s, bx, by, w, blabel, bcolor)
            bx = bx + w + Inches(0.12)
        # descripción
        txt(s, Inches(7.4), y, Inches(5.0), hh,
            [P(desc, 12, GRAY, False)], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.08)
    if note:
        rounded(s, Inches(0.78), Inches(6.62), Inches(11.78), Inches(0.42), NAVY)
        txt(s, Inches(1.05), Inches(6.62), Inches(11.3), Inches(0.42),
            [[("» ", 11.5, CYAN, True, False), (note, 11.5, WHITE, False, False)]],
            anchor=MSO_ANCHOR.MIDDLE)
    return s


FREE = ("Gratis", GREEN)
CHEAP = ("Bajo costo", BLUE)
API = ("API/IA", AMBER)
EASY = ("Fácil", CYAN)
PRO = ("Profesional", GRAY)

# ----------------------------------------------------------------------------
# 5. GENERACIÓN CON IA
# ----------------------------------------------------------------------------
tool_cards_slide(
    "Categoría 01 · Generación", "Crear video desde texto o imagen", 5, BLUE,
    [
        ("Kling 3.0", [FREE, CHEAP, API],
         "Mejor relación calidad-precio (~$0.10/seg, ~$3 por video). 4K, 60fps, clips de 15s y lip-sync multilingüe. Plan gratis con generaciones diarias limitadas."),
        ("Google Veo 3.1", [FREE, API],
         "La calidad más alta: 4K real con audio nativo. Cuota gratuita vía Google AI Studio; plan AI Pro $19.99/mes. Ideal para conceptos de marketing realistas."),
        ("Runway Gen-4.5", [FREE, API, PRO],
         "El favorito profesional: control de cámara, motion brush y consistencia de personajes. 125 créditos gratis; plan Standard desde $12-15/mes."),
        ("Pika & Luma Dream Machine", [CHEAP, EASY],
         "Alternativas creativas y muy accesibles, con planes de pago desde ~$10/mes. Buenas para experimentar con efectos y estilos."),
    ],
    note="Nota: OpenAI descontinúa la app web de Sora 2 (abr-2026) y su API (sep-2026); evaluar con cautela para proyectos nuevos."
)

# ----------------------------------------------------------------------------
# 6. EDICIÓN CON IA
# ----------------------------------------------------------------------------
tool_cards_slide(
    "Categoría 02 · Edición", "Editar y pulir con ayuda de IA", 6, CYAN,
    [
        ("CapCut", [FREE, EASY, CHEAP],
         "El editor más fácil y popular. Versión gratis muy generosa: subtítulos automáticos, quitar fondo sin croma y efectos en tendencia. Pro $7.99/mes."),
        ("Descript", [CHEAP, API],
         "Editas el video editando su transcripción. Asistente de IA 'Underlord' y limpieza de audio 'Studio Sound'. Ideal para podcast y videos hablados. $24/mes."),
        ("DaVinci Resolve", [FREE, PRO],
         "Edición profesional gratuita: 4K y funciones de IA (Magic Mask, reducción de ruido, super scaling, detección de escenas) incluidas en la versión gratis."),
        ("Adobe Premiere (Firefly)", [PRO, API],
         "Estándar de la industria con IA generativa Firefly integrada. Para producción profesional con presupuesto y flujos avanzados."),
    ],
)

# ----------------------------------------------------------------------------
# 7. AVATARES CON IA
# ----------------------------------------------------------------------------
tool_cards_slide(
    "Categoría 03 · Avatares", "Presentadores virtuales con IA", 7, AMBER,
    [
        ("HeyGen", [FREE, CHEAP, API],
         "Avatares muy expresivos (micro-gestos naturales), 100+ avatares y 175+ idiomas con traducción y lip-sync. Plan gratis: 3 videos/mes. Creator $29/mes (~$24 anual)."),
        ("Synthesia", [FREE, CHEAP, API],
         "240+ avatares y 160+ idiomas, con gran consistencia en videos largos. Plan gratuito disponible; precio más predecible. Starter $29/mes (~$22 anual)."),
        ("¿Cuál elegir?", [EASY],
         "HeyGen destaca en realismo y multilingüe para ventas/redes; Synthesia es más predecible y robusto para capacitación y comunicación interna a escala."),
    ],
    note="Caso de uso típico: capacitación, onboarding, comunicados internos y videos de ventas localizados a varios idiomas sin grabar cámara."
)

# ----------------------------------------------------------------------------
# 8. TODO-EN-UNO
# ----------------------------------------------------------------------------
tool_cards_slide(
    "Categoría 04 · Todo-en-uno", "De guion a video, sin complicaciones", 8, GREEN,
    [
        ("Pictory", [FREE, EASY, API],
         "Pega un guion o un blog y genera el video: elige visuales, agrega transiciones y voz en off. Plan gratis: 10 videos/mes (hasta 2 min)."),
        ("InVideo", [FREE, EASY, API],
         "El mejor para marketing en redes: video 1080p desde un prompt + datos del producto. Free: 2 min/exportaciones con marca de agua; pago desde ~$28/mes."),
        ("VEED", [FREE, EASY, CHEAP],
         "Editor rápido en línea con subtítulos automáticos y efectos de IA. Free con marca de agua; plan Creator $12/mes (quita marca, 1080p)."),
        ("Canva", [FREE, EASY],
         "Plantillas y generador de video con IA, integrado al diseño. Plan gratuito útil para piezas sencillas y sociales; ideal para equipos no técnicos."),
    ],
)

# ----------------------------------------------------------------------------
# 9. AUTOMATIZACIÓN / CONEXIÓN CON IA
# ----------------------------------------------------------------------------
tool_cards_slide(
    "Categoría 05 · Automatización", "Conexión con IA y flujos automáticos", 9, NAVY,
    [
        ("OpusClip", [FREE, API],
         "Convierte videos largos en clips virales con subtítulos y 'Virality Score'. Free: 60 créditos/mes (con marca de agua). Pro $29/mes; API en plan Business."),
        ("Shotstack", [API, PRO],
         "API de renderizado en la nube: ChatGPT genera el guion → Shotstack corta, transiciona y exporta. Desde $0.20 por minuto renderizado."),
        ("Fliki (videoGPT)", [FREE, API, EASY],
         "Integra ChatGPT directamente: un Custom GPT en el GPT Store permite generar video sin copiar y pegar. Plan gratuito disponible."),
        ("Manus", [API],
         "Agente de IA que orquesta varios modelos: del guion a los recursos y al ensamblaje final, gestionando flujos de varios pasos."),
    ],
    note="Para conectar con IA: las APIs de Veo y modelos frontera rondan $0.15–$0.40 por segundo de video generado."
)

# ----------------------------------------------------------------------------
# 10. TABLA COMPARATIVA
# ----------------------------------------------------------------------------
s = slide()
header(s, "Comparativa", "Resumen costo y facilidad", 10)
rows = [
    ("Herramienta", "Categoría", "Plan gratis", "Pago desde", "Facilidad", "IA / API", True),
    ("CapCut", "Edición", "Sí (generoso)", "$7.99/mes", "Muy alta", "Sí", False),
    ("Kling 3.0", "Generación", "Sí (limitado)", "~$3/video", "Alta", "Sí", False),
    ("Google Veo 3.1", "Generación", "Cuota AI Studio", "$19.99/mes", "Media", "Sí (API)", False),
    ("Runway Gen-4.5", "Generación", "125 créditos", "$12-15/mes", "Media", "Sí (API)", False),
    ("DaVinci Resolve", "Edición", "Sí (completo)", "Pago único", "Media", "Local", False),
    ("HeyGen", "Avatares", "3 videos/mes", "$24/mes", "Alta", "Sí (API)", False),
    ("Synthesia", "Avatares", "Sí", "$22/mes", "Alta", "Sí (API)", False),
    ("Pictory", "Todo-en-uno", "10 videos/mes", "Económico", "Muy alta", "Sí", False),
    ("OpusClip", "Automatización", "60 créditos/mes", "$29/mes", "Alta", "Sí (API)", False),
]
tx, ty = Inches(0.78), Inches(1.45)
tw = Inches(11.78)
colw = [Inches(2.55), Inches(2.05), Inches(2.1), Inches(1.85), Inches(1.65), Inches(1.58)]
rh = Inches(0.515)
hdr_h = Inches(0.52)
# encabezado
rounded(s, tx, ty, tw, hdr_h, NAVY)
cx = tx
hdr = rows[0]
for j in range(6):
    al = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
    txt(s, cx + Inches(0.12), ty, colw[j] - Inches(0.2), hdr_h,
        [P(hdr[j], 11.5, WHITE, True)], align=al, anchor=MSO_ANCHOR.MIDDLE)
    cx += colw[j]
# filas
for i, row in enumerate(rows[1:]):
    yy = ty + hdr_h + Emu(int(rh * i))
    bg = WHITE if i % 2 == 0 else LIGHT
    rect(s, tx, yy, tw, rh, bg)
    cx = tx
    for j in range(6):
        al = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
        bold = (j == 0)
        col = NAVY if j == 0 else GRAY
        sz = 11.5 if j == 0 else 11
        txt(s, cx + Inches(0.12), yy, colw[j] - Inches(0.2), rh,
            [P(row[j], sz, col, bold)], align=al, anchor=MSO_ANCHOR.MIDDLE)
        cx += colw[j]
rect(s, tx, ty + hdr_h, tw, Emu(int(rh * len(rows[1:]))), WHITE,
     line_color=LINE, line_w=Pt(1)).fill.background()


# ----------------------------------------------------------------------------
# 11. RECOMENDACIONES POR PERFIL
# ----------------------------------------------------------------------------
s = slide()
header(s, "Recomendaciones", "El stack ideal según tu perfil", 11)
profiles = [
    ("Creador / Redes sociales", "Presupuesto $0", BLUE,
     ["CapCut — edición gratis", "Kling 3.0 — generación barata", "OpusClip — clips virales"]),
    ("PyME / Marketing", "Bajo costo", CYAN,
     ["InVideo o Pictory — guion→video", "HeyGen/Synthesia — avatares", "Runway — piezas de calidad"]),
    ("Producción profesional", "Sin suscripción", GREEN,
     ["DaVinci Resolve — gratis y pro", "Google Veo 3.1 — máxima calidad", "Descript — flujo por texto"]),
    ("Escala / Automatización", "Conexión IA", AMBER,
     ["Shotstack — API de render", "Fliki videoGPT — desde ChatGPT", "Manus — agente orquestador"]),
]
cw = Inches(5.78)
chh = Inches(2.5)
gx, gy = Inches(0.78), Inches(1.55)
for i, (title, tag, c, items) in enumerate(profiles):
    x = gx + (i % 2) * (cw + Inches(0.22))
    y = gy + (i // 2) * (chh + Inches(0.2))
    rounded(s, x, y, cw, chh, LIGHT)
    rect(s, x, y, cw, Inches(0.7), c)
    txt(s, x + Inches(0.28), y, cw - Inches(2.0), Inches(0.7),
        [P(title, 16, WHITE, True)], anchor=MSO_ANCHOR.MIDDLE)
    chip(s, x + cw - Inches(1.85), y + Inches(0.19), Inches(1.6), tag, NAVY)
    for k, it in enumerate(items):
        iy = y + Inches(0.92) + k * Inches(0.49)
        rounded(s, x + Inches(0.3), iy + Inches(0.07), Inches(0.16), Inches(0.16), c)
        txt(s, x + Inches(0.62), iy, cw - Inches(0.9), Inches(0.45),
            [P(it, 13, INK, False)], anchor=MSO_ANCHOR.MIDDLE)


# ----------------------------------------------------------------------------
# 12. CONCLUSIONES Y PRÓXIMOS PASOS
# ----------------------------------------------------------------------------
s = slide()
header(s, "Conclusiones", "Hallazgos y próximos pasos", 12)
txt(s, Inches(0.78), Inches(1.45), Inches(5.7), Inches(0.4),
    [P("HALLAZGOS CLAVE", 12.5, BLUE, True)])
findings = [
    "Ya no hace falta presupuesto para empezar: todas las categorías tienen opción gratuita.",
    "La 'conexión con IA' es real: ChatGPT + API permiten automatizar la producción.",
    "Lo más fácil hoy: CapCut, Pictory y Canva para resultados pulidos en minutos.",
    "Mejor valor en generación: Kling 3.0; mejor calidad: Veo 3.1.",
]
for i, f in enumerate(findings):
    iy = Inches(1.95) + i * Inches(0.92)
    rounded(s, Inches(0.78), iy + Inches(0.05), Inches(0.3), Inches(0.3), BLUE)
    txt(s, Inches(0.78), iy + Inches(0.05), Inches(0.3), Inches(0.3),
        [P("✓", 13, WHITE, True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(1.25), iy, Inches(5.25), Inches(0.85),
        [P(f, 13, INK, False)], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.08)

# panel próximos pasos
rounded(s, Inches(6.85), Inches(1.45), Inches(5.7), Inches(5.05), NAVY)
txt(s, Inches(7.2), Inches(1.7), Inches(5.0), Inches(0.4),
    [P("PRÓXIMOS PASOS", 12.5, CYAN, True)])
steps = [
    ("1", "Pilotar sin costo", "Probar CapCut + Kling + OpusClip en una campaña real esta semana."),
    ("2", "Definir el stack", "Elegir 2-3 herramientas según el perfil y caso de uso prioritario."),
    ("3", "Automatizar", "Conectar ChatGPT con una API (Shotstack/Fliki) para escalar producción."),
    ("4", "Medir y ajustar", "Comparar tiempo de producción y costo por video antes/después."),
]
for i, (n, t, d) in enumerate(steps):
    iy = Inches(2.25) + i * Inches(1.02)
    rounded(s, Inches(7.2), iy, Inches(0.5), Inches(0.5), CYAN)
    txt(s, Inches(7.2), iy, Inches(0.5), Inches(0.5),
        [P(n, 18, NAVY, True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(7.9), iy - Inches(0.02), Inches(4.4), Inches(0.4),
        [P(t, 14.5, WHITE, True)])
    txt(s, Inches(7.9), iy + Inches(0.35), Inches(4.45), Inches(0.6),
        [P(d, 11.5, RGBColor(0xC6, 0xD3, 0xE6), False)], line_spacing=1.05)


# ----------------------------------------------------------------------------
# 13. CIERRE
# ----------------------------------------------------------------------------
s = slide()
rect(s, 0, 0, EMU_W, EMU_H, NAVY)
rect(s, 0, Inches(0.0), EMU_W, Inches(0.12), BLUE)
rect(s, 0, Inches(0.12), EMU_W, Inches(0.06), CYAN)
rounded(s, Inches(5.85), Inches(2.35), Inches(0.72), Inches(0.72), BLUE)
txt(s, Inches(5.85), Inches(2.35), Inches(0.72), Inches(0.72),
    [P("H", 34, WHITE, True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(0), Inches(3.35), EMU_W, Inches(0.7),
    [P("Gracias", 40, WHITE, True)], align=PP_ALIGN.CENTER)
txt(s, Inches(0), Inches(4.25), EMU_W, Inches(0.5),
    [P("¿Listos para producir video con IA, fácil y a bajo costo?", 16,
       RGBColor(0xC6, 0xD3, 0xE6), False)], align=PP_ALIGN.CENTER)
txt(s, Inches(0), Inches(6.7), EMU_W, Inches(0.4),
    [[("Howy", 12, CYAN, True, False),
      ("   ·   Presentación ejecutiva   ·   Junio 2026", 12,
       RGBColor(0x9F, 0xB2, 0xCD), False, False)]], align=PP_ALIGN.CENTER)


# ----------------------------------------------------------------------------
out = "/home/user/Work/presentaciones/Howy_Herramientas_IA_Video_2026.pptx"
prs.save(out)
print("OK ->", out, "| slides:", len(prs.slides._sldIdLst))
