# -*- coding: utf-8 -*-
"""
Guía detallada para el equipo — Howy
Ficha por herramienta + recomendaciones + camino de uso, con enlaces a tutoriales.
Salida: PowerPoint (.pptx) 16:9.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

NAVY  = RGBColor(0x0E, 0x21, 0x3A)
BLUE  = RGBColor(0x2D, 0x6C, 0xDF)
CYAN  = RGBColor(0x18, 0xC2, 0xD6)
AMBER = RGBColor(0xF5, 0xA6, 0x23)
INK   = RGBColor(0x1A, 0x24, 0x32)
GRAY  = RGBColor(0x5B, 0x66, 0x74)
LIGHT = RGBColor(0xF4, 0xF7, 0xFB)
LINE  = RGBColor(0xD9, 0xE0, 0xE9)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREEN = RGBColor(0x27, 0xAE, 0x60)
RED   = RGBColor(0xE0, 0x42, 0x42)

FB = "Calibri"
EMU_W, EMU_H = Inches(13.333), Inches(7.5)

prs = Presentation()
prs.slide_width = EMU_W
prs.slide_height = EMU_H
BLANK = prs.slide_layouts[6]


def slide():
    return prs.slides.add_slide(BLANK)


def rect(s, x, y, w, h, color, line_color=None, line_w=None):
    sp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    if line_color is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line_color; sp.line.width = line_w or Pt(0.75)
    sp.shadow.inherit = False
    return sp


def rounded(s, x, y, w, h, color, line_color=None, line_w=None, rad=0.06):
    sp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    try: sp.adjustments[0] = rad
    except Exception: pass
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    if line_color is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line_color; sp.line.width = line_w or Pt(1)
    sp.shadow.inherit = False
    return sp


def P(t, sz, col, bold=False, ital=False):
    return [(t, sz, col, bold, ital)]


def txt(s, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
        space_after=4, line_spacing=1.0, wrap=True):
    tb = s.shapes.add_textbox(x, y, w, h); tf = tb.text_frame
    tf.word_wrap = wrap; tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.space_after = Pt(space_after); p.space_before = Pt(0)
        p.line_spacing = line_spacing
        for (t, sz, col, bold, ital) in para:
            r = p.add_run(); r.text = t
            r.font.size = Pt(sz); r.font.color.rgb = col
            r.font.bold = bold; r.font.italic = ital; r.font.name = FB
    return tb


def footer(s, page):
    txt(s, Inches(0.55), Inches(7.04), Inches(8), Inches(0.32),
        [[("Howy", 9, BLUE, True, False),
          ("  ·  Guía de herramientas de IA para video — 2026", 9, GRAY, False, False)]],
        anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(11.8), Inches(7.04), Inches(1.0), Inches(0.32),
        [P(f"{page:02d}", 9, GRAY)], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def header(s, kicker, title, page, accent=BLUE):
    rect(s, Inches(0.55), Inches(0.42), Inches(0.09), Inches(0.5), accent)
    txt(s, Inches(0.78), Inches(0.30), Inches(11.5), Inches(0.28),
        [P(kicker.upper(), 11, accent, True)])
    txt(s, Inches(0.78), Inches(0.54), Inches(11.9), Inches(0.55),
        [P(title, 26, NAVY, True)])
    rect(s, Inches(0.55), Inches(1.18), Inches(12.23), Pt(1.2), LINE)
    footer(s, page)


def chip(s, x, y, label, color, h=Inches(0.32)):
    w = Inches(0.2 + 0.094 * len(label))
    sp = rounded(s, x, y, w, h, color)
    tf = sp.text_frame; tf.word_wrap = False
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = label
    r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FB
    return x + w + Inches(0.12)


def link_button(s, x, y, w, h, label, url, color):
    sp = rounded(s, x, y, w, h, color)
    sp.click_action.hyperlink.address = url
    tf = sp.text_frame; tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.1); tf.margin_right = Inches(0.1)
    tf.margin_top = 0; tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = label
    r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FB
    r.hyperlink.address = url
    return sp


# ===========================================================================
# PORTADA
# ===========================================================================
s = slide()
rect(s, 0, 0, EMU_W, EMU_H, NAVY)
rect(s, 0, Inches(6.7), EMU_W, Inches(0.12), BLUE)
rect(s, 0, Inches(6.82), EMU_W, Inches(0.06), CYAN)
rounded(s, Inches(0.85), Inches(0.8), Inches(0.62), Inches(0.62), BLUE)
txt(s, Inches(0.85), Inches(0.8), Inches(0.62), Inches(0.62), [P("H", 30, WHITE, True)],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(1.62), Inches(0.8), Inches(5), Inches(0.62), [P("Howy", 26, WHITE, True)],
    anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(0.85), Inches(2.5), Inches(11.6), Inches(0.4),
    [P("GUÍA PARA EL EQUIPO", 14, CYAN, True)])
txt(s, Inches(0.85), Inches(2.95), Inches(11.7), Inches(1.8),
    [P("Herramientas de IA para video:", 40, WHITE, True),
     P("fichas, recomendaciones y cómo usarlas", 40, WHITE, True)], line_spacing=1.02)
txt(s, Inches(0.85), Inches(5.15), Inches(11.0), Inches(0.7),
    [P("Qué es cada app · funciones gratis a explotar · cuáles convienen · tutoriales en video",
       16, RGBColor(0xC6, 0xD3, 0xE6), False)])
txt(s, Inches(0.85), Inches(6.95), Inches(8), Inches(0.4),
    [P("Material de capacitación interna", 11, RGBColor(0x9F, 0xB2, 0xCD), False)])
txt(s, Inches(9.5), Inches(6.95), Inches(2.95), Inches(0.4),
    [P("Junio 2026", 11, RGBColor(0x9F, 0xB2, 0xCD), False)], align=PP_ALIGN.RIGHT)


# ===========================================================================
# CÓMO LEER ESTA GUÍA (leyenda)
# ===========================================================================
s = slide()
header(s, "Introducción", "Cómo leer esta guía", 2)
txt(s, Inches(0.78), Inches(1.45), Inches(11.8), Inches(0.7),
    [P("Cada herramienta tiene una ficha con lo que es, las funciones gratuitas que conviene "
       "aprovechar, para qué caso sirve mejor y un botón con un tutorial en video (clic para abrir).",
       14, GRAY, False)], line_spacing=1.15)
txt(s, Inches(0.78), Inches(2.45), Inches(11.8), Inches(0.3),
    [P("ETIQUETAS QUE VERÁS", 12, BLUE, True)])
legend = [
    ("Gratis", GREEN, "Tiene plan gratuito útil."),
    ("Bajo costo", BLUE, "Planes de pago accesibles."),
    ("Fácil", CYAN, "Curva de aprendizaje mínima."),
    ("API/IA", AMBER, "Se conecta con IA / se automatiza."),
    ("Profesional", GRAY, "Potencia de nivel pro."),
]
y = Inches(2.85)
for i, (lab, col, desc) in enumerate(legend):
    yy = y + i * Inches(0.72)
    chip(s, Inches(0.9), yy, lab, col, h=Inches(0.38))
    txt(s, Inches(2.9), yy, Inches(9.6), Inches(0.4),
        [P(desc, 13.5, INK, False)], anchor=MSO_ANCHOR.MIDDLE)
rounded(s, Inches(0.78), Inches(6.5), Inches(11.78), Inches(0.5), LIGHT)
txt(s, Inches(1.05), Inches(6.5), Inches(11.3), Inches(0.5),
    [[("Tip: ", 12, BLUE, True, False),
      ("los precios y límites de los planes gratis cambian seguido; confirma en la web oficial antes de contratar.",
       12, GRAY, False, False)]], anchor=MSO_ANCHOR.MIDDLE)


# ===========================================================================
# FICHAS DE HERRAMIENTAS
# ===========================================================================
G = ("Gratis", GREEN); C = ("Bajo costo", BLUE); F = ("Fácil", CYAN)
A = ("API/IA", AMBER); PRO = ("Profesional", GRAY)

tools = [
    dict(cat="Edición · Categoría 02", name="CapCut", accent=CYAN, badges=[G, F, C],
         que="Editor de video gratuito (móvil y PC) líder para redes sociales. Interfaz simple "
             "que permite lograr un video pulido en minutos, sin saber de líneas de tiempo.",
         gratis=["Subtítulos automáticos editables", "Quitar fondo sin croma (IA)",
                 "Plantillas y efectos en tendencia", "Texto, música y transiciones",
                 "Exportar en 1080p sin marca de agua"],
         ideal="Contenido para TikTok / Reels / Shorts y edición rápida del día a día.",
         vt="Tutorial CapCut desde cero (principiantes)",
         vu="https://www.youtube.com/watch?v=e7zs-Tap9XY"),
    dict(cat="Todo-en-uno · Categoría 04", name="Canva", accent=GREEN, badges=[G, F],
         que="Plataforma de diseño todo-en-uno con editor de video y generador con IA. Ideal para "
             "equipos no técnicos que ya usan Canva para diseño de marca.",
         gratis=["Plantillas de video listas", "Generador 'Texto a video' con IA",
                 "Grabadora de pantalla y cámara", "Banco de elementos y música",
                 "Subtítulos automáticos"],
         ideal="Piezas sociales, presentaciones animadas y videos de marca sin curva técnica.",
         vt="Videos en minutos con IA en Canva (2026)",
         vu="https://www.youtube.com/watch?v=3kDT54Kz9Dc"),
    dict(cat="Generación · Categoría 01", name="Kling 3.0", accent=BLUE, badges=[G, C, A],
         que="Generador de video con IA (texto o imagen a video) con la mejor relación "
             "calidad-precio: 4K, 60 fps, clips de 15 s y lip-sync multilingüe.",
         gratis=["Créditos diarios gratuitos", "Texto a video e imagen a video",
                 "Lip-sync en varios idiomas", "Extender / continuar clips",
                 "Galería de estilos y plantillas"],
         ideal="B-roll, escenas con movimiento y clips cortos de alto impacto a bajo costo.",
         vt="Cómo usar Kling AI — videos con IA gratis",
         vu="https://www.youtube.com/watch?v=m6zEjDALPqE"),
    dict(cat="Generación · Categoría 01", name="Google Veo 3.1", accent=BLUE, badges=[G, A, PRO],
         que="Modelo de Google con la calidad más alta: 4K real con audio nativo. Accesible "
             "desde Gemini, Google AI Studio y la app Flow.",
         gratis=["Cuota gratuita en Gemini / AI Studio", "Audio nativo dentro del video",
                 "Prompts en lenguaje natural", "Integración con Flow para escenas largas",
                 "Texto a video e imagen a video"],
         ideal="Conceptos de marketing realistas y piezas de la más alta calidad.",
         vt="Tutorial Google Veo 3.1 en Flow",
         vu="https://www.youtube.com/watch?v=k0r4vqjXwyU"),
    dict(cat="Generación · Categoría 01", name="Runway Gen-4.5", accent=BLUE, badges=[G, C, PRO],
         que="Suite creativa profesional con control fino: movimientos de cámara, 'motion brush' "
             "y consistencia de personajes/marca entre tomas.",
         gratis=["125 créditos al registrarse", "Texto e imagen a video",
                 "Motion brush (animar zonas)", "Herramientas de edición con IA",
                 "Quitar fondo y más"],
         ideal="Equipos que necesitan control creativo y consistencia de marca.",
         vt="Runway para principiantes (tutorial completo)",
         vu="https://www.youtube.com/watch?v=FKvAPQjdp2g"),
    dict(cat="Edición · Categoría 02", name="Descript", accent=CYAN, badges=[C, A],
         que="Editor que funciona editando la transcripción: borras texto y se borra el video. "
             "El flujo más rápido para contenido hablado.",
         gratis=["Transcripción automática", "Edición por texto",
                 "Eliminar muletillas ('eh', 'um')", "Studio Sound (limpieza de audio)",
                 "Grabación de pantalla"],
         ideal="Podcasts, entrevistas y videos tipo 'talking head'.",
         vt="Edita tu primer video con Descript (español)",
         vu="https://www.youtube.com/watch?v=pTHZ8hRUwzY"),
    dict(cat="Edición · Categoría 02", name="DaVinci Resolve", accent=CYAN, badges=[G, PRO],
         que="Edición profesional de escritorio totalmente gratuita. Estándar de cine para "
             "edición, color, efectos y audio en un solo programa.",
         gratis=["Edición 4K completa", "Magic Mask (selección con IA)",
                 "Reducción de ruido y super scaling", "Detección de escenas",
                 "Corrección de color profesional"],
         ideal="Producción profesional sin pagar suscripción.",
         vt="DaVinci Resolve 19 — tutorial completo (español)",
         vu="https://www.youtube.com/watch?v=PtAxuOAQNcI"),
    dict(cat="Avatares · Categoría 03", name="HeyGen", accent=AMBER, badges=[G, C, A],
         que="Avatares de IA muy expresivos que hablan en 175+ idiomas. Permite crear tu clon "
             "digital y traducir videos con lip-sync.",
         gratis=["3 videos al mes", "Avatares de stock",
                 "Texto a voz (TTS)", "Traducción de video (demo)",
                 "Plantillas listas"],
         ideal="Ventas, capacitación y comunicados multilingües sin grabar a cámara.",
         vt="Tutorial HeyGen 2026 — videos con avatares de IA",
         vu="https://www.youtube.com/watch?v=SiwJ4GJe4xY"),
    dict(cat="Avatares · Categoría 03", name="Synthesia", accent=AMBER, badges=[G, C, A],
         que="Plataforma de avatares con IA (240+ avatares, 160+ idiomas) con gran consistencia, "
             "pensada para video corporativo y formación.",
         gratis=["Plan gratuito con minutos de prueba", "Avatares y plantillas",
                 "Texto a video", "Narración multilingüe",
                 "Editor por escenas"],
         ideal="Capacitación, onboarding y comunicación interna a escala.",
         vt="Synthesia AI — guía completa (español)",
         vu="https://www.youtube.com/watch?v=r2FqQzGNUWg"),
    dict(cat="Todo-en-uno · Categoría 04", name="Pictory", accent=GREEN, badges=[G, F, A],
         que="Convierte un guion o un blog en video automáticamente: selecciona visuales, agrega "
             "transiciones y voz en off con IA.",
         gratis=["10 videos al mes (hasta 2 min)", "Guion a video",
                 "Blog / artículo a video", "Voz en off con IA",
                 "Subtítulos automáticos"],
         ideal="Convertir texto y artículos en videos de forma rápida.",
         vt="Cómo usar Pictory AI — tutorial en español",
         vu="https://www.youtube.com/watch?v=QQylZbgwyMk"),
    dict(cat="Todo-en-uno · Categoría 04", name="InVideo", accent=GREEN, badges=[G, F, A],
         que="Generador de video para marketing: crea videos 1080p desde un solo prompt, con "
             "guion, visuales, voz y edición automáticos.",
         gratis=["Minutos de generación semanales", "Prompt a video",
                 "Miles de plantillas", "Voz con IA",
                 "Banco de stock (con marca de agua)"],
         ideal="Videos de producto y marketing para redes sociales.",
         vt="Tutorial InVideo AI 2026 (español)",
         vu="https://www.youtube.com/watch?v=NwCf1MU1Wqs"),
    dict(cat="Todo-en-uno · Categoría 04", name="VEED", accent=GREEN, badges=[G, F, C],
         que="Editor de video online rápido con subtítulos automáticos y herramientas de IA. "
             "Funciona en el navegador, sin instalar nada.",
         gratis=["Subtítulos automáticos", "Recortar y redimensionar",
                 "Quitar fondo y ruido", "Grabadora de pantalla",
                 "Plantillas (export con marca de agua)"],
         ideal="Edición rápida en el navegador para redes y podcasts.",
         vt="Cómo usar VEED.io — tutorial en español (2025)",
         vu="https://www.youtube.com/watch?v=MFllzKvqnCY"),
    dict(cat="Automatización · Categoría 05", name="OpusClip", accent=NAVY, badges=[G, A],
         que="Convierte videos largos en clips cortos virales de forma automática, con subtítulos "
             "y un 'Virality Score' que prioriza los mejores momentos.",
         gratis=["60 créditos al mes", "Clips automáticos desde video largo",
                 "Subtítulos animados con IA", "Reencuadre vertical automático",
                 "(export con marca de agua)"],
         ideal="Reciclar webinars y podcasts en Reels / Shorts / TikToks.",
         vt="Cómo usar Opus Clip — tutorial en español (2026)",
         vu="https://www.youtube.com/watch?v=21QDrK4fYzk"),
]

page = 3
for t in tools:
    s = slide()
    acc = t["accent"]
    header(s, t["cat"], t["name"], page, accent=acc)
    # badges
    bx = Inches(0.78)
    for (lab, col) in t["badges"]:
        bx = chip(s, bx, Inches(1.32), lab, col)
    # --- columna izquierda: QUÉ ES ---
    rounded(s, Inches(0.78), Inches(1.85), Inches(5.55), Inches(3.15), LIGHT)
    rect(s, Inches(0.78), Inches(1.85), Inches(0.12), Inches(3.15), acc)
    txt(s, Inches(1.1), Inches(2.05), Inches(5.0), Inches(0.3),
        [P("QUÉ ES", 12, acc, True)])
    txt(s, Inches(1.1), Inches(2.45), Inches(5.05), Inches(2.45),
        [P(t["que"], 13.5, INK, False)], line_spacing=1.18)
    # --- columna derecha: FUNCIONES GRATIS ---
    rounded(s, Inches(6.6), Inches(1.85), Inches(5.95), Inches(3.15), WHITE,
            line_color=LINE, line_w=Pt(1.2))
    txt(s, Inches(6.9), Inches(2.05), Inches(5.4), Inches(0.3),
        [P("FUNCIONES GRATIS A EXPLOTAR", 12, GREEN, True)])
    for k, g in enumerate(t["gratis"]):
        gy = Inches(2.5) + k * Inches(0.47)
        rounded(s, Inches(6.95), gy + Inches(0.05), Inches(0.16), Inches(0.16), GREEN)
        txt(s, Inches(7.27), gy, Inches(5.05), Inches(0.42),
            [P(g, 12.5, INK, False)], anchor=MSO_ANCHOR.MIDDLE)
    # --- franja IDEAL PARA ---
    rounded(s, Inches(0.78), Inches(5.18), Inches(11.78), Inches(0.62), NAVY)
    txt(s, Inches(1.05), Inches(5.18), Inches(11.3), Inches(0.62),
        [[("Ideal para:  ", 13, CYAN, True, False), (t["ideal"], 13, WHITE, False, False)]],
        anchor=MSO_ANCHOR.MIDDLE)
    # --- botón de video ---
    link_button(s, Inches(0.78), Inches(5.98), Inches(11.78), Inches(0.62),
                "▶  Ver tutorial en YouTube:  " + t["vt"], t["vu"], acc)
    page += 1


# ===========================================================================
# CUÁLES CONVIENEN MÁS
# ===========================================================================
s = slide()
header(s, "Recomendación", "¿Cuáles convienen más?", page, accent=BLUE); page += 1
picks = [
    ("Más fácil para empezar", CYAN, "CapCut · Canva · Pictory",
     "Resultados pulidos en minutos, sin conocimientos técnicos."),
    ("Mejor 100% gratis", GREEN, "DaVinci Resolve · CapCut · Kling",
     "Máxima potencia sin pagar: edición pro y generación con IA."),
    ("Mejor generación con IA", BLUE, "Kling (precio) · Veo (calidad) · Runway (control)",
     "Crear video desde texto/imagen según prioridad."),
    ("Mejor para empresa / equipo", AMBER, "HeyGen · Synthesia · InVideo",
     "Avatares para capacitación y ventas; marketing a escala."),
    ("Mejor automatización", NAVY, "OpusClip · Fliki · Shotstack",
     "Clips automáticos y flujos conectados con ChatGPT / API."),
]
y = Inches(1.5)
for i, (t, c, tools_s, d) in enumerate(picks):
    yy = y + i * Inches(0.78)
    rounded(s, Inches(0.78), yy, Inches(11.78), Inches(0.66), LIGHT)
    rect(s, Inches(0.78), yy, Inches(0.12), Inches(0.66), c)
    txt(s, Inches(1.1), yy, Inches(3.6), Inches(0.66),
        [P(t, 13.5, NAVY, True)], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.0)
    txt(s, Inches(4.7), yy, Inches(4.2), Inches(0.66),
        [P(tools_s, 12.5, c, True)], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.0)
    txt(s, Inches(8.95), yy, Inches(3.45), Inches(0.66),
        [P(d, 11, GRAY, False)], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.0)
# Top 3 para Howy
rounded(s, Inches(0.78), Inches(5.6), Inches(11.78), Inches(1.05), NAVY)
txt(s, Inches(1.1), Inches(5.75), Inches(11.2), Inches(0.35),
    [P("TOP 3 PARA EMPEZAR EN HOWY", 12.5, CYAN, True)])
txt(s, Inches(1.1), Inches(6.1), Inches(11.3), Inches(0.5),
    [[("CapCut", 14, WHITE, True, False), (" (edición gratis)  +  ", 14, WHITE, False, False),
      ("Canva/Pictory", 14, WHITE, True, False), (" (guion→video)  +  ", 14, WHITE, False, False),
      ("HeyGen", 14, WHITE, True, False), (" (avatares).  Suma ", 14, WHITE, False, False),
      ("OpusClip", 14, WHITE, True, False), (" para reciclar en clips.", 14, WHITE, False, False)]],
    anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.1)


# ===========================================================================
# CAMINO DE USO RECOMENDADO (roadmap)
# ===========================================================================
s = slide()
header(s, "Plan de adopción", "Camino de uso recomendado", page, accent=BLUE); page += 1
txt(s, Inches(0.78), Inches(1.4), Inches(11.8), Inches(0.5),
    [P("Un plan progresivo de ~4–6 semanas para que el equipo adopte el video con IA sin fricción.",
       13.5, GRAY, False)])
phases = [
    ("FASE 1", "Semana 1", CYAN, "Explorar gratis",
     ["Crear cuenta en CapCut y Canva", "Editar 1 video social real",
      "Probar subtítulos automáticos"]),
    ("FASE 2", "Semana 2-3", BLUE, "Generar con IA",
     ["Probar Kling (clips/B-roll)", "Probar Veo desde Gemini",
      "Comparar calidad vs. tiempo"]),
    ("FASE 3", "Semana 3-4", AMBER, "Avatares",
     ["Crear 1 video con HeyGen", "Guion de ventas o capacitación",
      "Traducir a otro idioma"]),
    ("FASE 4", "Mes 2", GREEN, "Escalar / automatizar",
     ["Reciclar con OpusClip", "Conectar ChatGPT + API",
      "Medir costo por video"]),
]
cw = Inches(2.85); gap = Inches(0.18); x0 = Inches(0.78); y0 = Inches(2.2)
for i, (ph, wk, c, title, items) in enumerate(phases):
    x = x0 + i * (cw + gap)
    rounded(s, x, y0, cw, Inches(4.1), LIGHT)
    rect(s, x, y0, cw, Inches(0.95), c)
    txt(s, x + Inches(0.22), y0 + Inches(0.12), cw - Inches(0.4), Inches(0.35),
        [P(ph + "  ·  " + wk, 11.5, WHITE, True)])
    txt(s, x + Inches(0.22), y0 + Inches(0.45), cw - Inches(0.4), Inches(0.45),
        [P(title, 16, WHITE, True)])
    for k, it in enumerate(items):
        iy = y0 + Inches(1.2) + k * Inches(0.78)
        rounded(s, x + Inches(0.22), iy + Inches(0.04), Inches(0.34), Inches(0.34), c)
        txt(s, x + Inches(0.22), iy + Inches(0.04), Inches(0.34), Inches(0.34),
            [P(str(k + 1), 13, WHITE, True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        txt(s, x + Inches(0.66), iy, cw - Inches(0.85), Inches(0.7),
            [P(it, 11.5, INK, False)], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.05)
# flechas entre fases
for i in range(3):
    ax = x0 + (i + 1) * cw + i * gap + Inches(0.01)
    txt(s, ax, y0 + Inches(1.6), gap, Inches(0.5), [P("›", 22, GRAY, True)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# ===========================================================================
# CIERRE
# ===========================================================================
s = slide()
rect(s, 0, 0, EMU_W, EMU_H, NAVY)
rect(s, 0, 0, EMU_W, Inches(0.12), BLUE)
rect(s, 0, Inches(0.12), EMU_W, Inches(0.06), CYAN)
rounded(s, Inches(5.85), Inches(2.3), Inches(0.72), Inches(0.72), BLUE)
txt(s, Inches(5.85), Inches(2.3), Inches(0.72), Inches(0.72), [P("H", 34, WHITE, True)],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, 0, Inches(3.3), EMU_W, Inches(0.7), [P("Manos a la obra", 38, WHITE, True)],
    align=PP_ALIGN.CENTER)
txt(s, 0, Inches(4.2), EMU_W, Inches(0.5),
    [P("Elijan 2-3 herramientas de la Fase 1 y hagan su primer video esta semana.",
       16, RGBColor(0xC6, 0xD3, 0xE6), False)], align=PP_ALIGN.CENTER)
txt(s, 0, Inches(6.7), EMU_W, Inches(0.4),
    [[("Howy", 12, CYAN, True, False),
      ("   ·   Guía de herramientas de IA para video   ·   Junio 2026", 12,
       RGBColor(0x9F, 0xB2, 0xCD), False, False)]], align=PP_ALIGN.CENTER)


out = "/home/user/Work/presentaciones/Howy_Guia_Detallada_IA_Video_2026.pptx"
prs.save(out)
print("OK ->", out, "| slides:", len(prs.slides._sldIdLst))
