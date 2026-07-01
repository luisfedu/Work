# -*- coding: utf-8 -*-
"""
Presentación ejecutiva — Howy
Maquinaria del proceso de aguacate: cosecha, recepción, lavado, calibrado/selección,
empaque, paletizado y cadena de frío. Diseño corporativo Howy. Salida: PPTX 16:9.
Fuentes: sitios de fabricantes, datasheets y documentos oficiales (2026).
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

NAVY  = RGBColor(0x0E, 0x21, 0x3A)
BLUE  = RGBColor(0x2D, 0x6C, 0xDF)
CYAN  = RGBColor(0x18, 0xC2, 0xD6)
AMBER = RGBColor(0xF5, 0xA6, 0x23)
GREEN = RGBColor(0x2E, 0xA8, 0x4F)
INK   = RGBColor(0x1A, 0x24, 0x32)
GRAY  = RGBColor(0x5B, 0x66, 0x74)
LIGHT = RGBColor(0xF4, 0xF7, 0xFB)
LINE  = RGBColor(0xD9, 0xE0, 0xE9)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FB = "Calibri"

EMU_W, EMU_H = Inches(13.333), Inches(7.5)
prs = Presentation()
prs.slide_width = EMU_W
prs.slide_height = EMU_H
BLANK = prs.slide_layouts[6]
_page = [0]


def slide():
    return prs.slides.add_slide(BLANK)


def rect(s, x, y, w, h, color, lc=None, lw=None):
    sp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    if lc is None: sp.line.fill.background()
    else: sp.line.color.rgb = lc; sp.line.width = lw or Pt(0.75)
    sp.shadow.inherit = False
    return sp


def rounded(s, x, y, w, h, color, lc=None, lw=None, rad=0.06):
    sp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    try: sp.adjustments[0] = rad
    except Exception: pass
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    if lc is None: sp.line.fill.background()
    else: sp.line.color.rgb = lc; sp.line.width = lw or Pt(1)
    sp.shadow.inherit = False
    return sp


def P(t, sz, col, bold=False, ital=False):
    return [(t, sz, col, bold, ital)]


def txt(s, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
        sa=3, ls=1.0, wrap=True):
    tb = s.shapes.add_textbox(x, y, w, h); tf = tb.text_frame
    tf.word_wrap = wrap; tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.space_after = Pt(sa); p.space_before = Pt(0); p.line_spacing = ls
        for (t, sz, col, bold, ital) in para:
            r = p.add_run(); r.text = t
            r.font.size = Pt(sz); r.font.color.rgb = col
            r.font.bold = bold; r.font.italic = ital; r.font.name = FB
    return tb


def footer(s):
    _page[0] += 1
    txt(s, Inches(0.55), Inches(7.06), Inches(9), Inches(0.3),
        [[("Howy", 9, BLUE, True, False),
          ("  ·  Maquinaria del proceso de aguacate — 2026", 9, GRAY, False, False)]],
        anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(11.9), Inches(7.06), Inches(0.9), Inches(0.3),
        [P(f"{_page[0]:02d}", 9, GRAY)], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def header(s, kicker, title, accent=BLUE):
    rect(s, Inches(0.55), Inches(0.4), Inches(0.09), Inches(0.5), accent)
    txt(s, Inches(0.78), Inches(0.28), Inches(11.6), Inches(0.28), [P(kicker.upper(), 11, accent, True)])
    txt(s, Inches(0.78), Inches(0.52), Inches(11.9), Inches(0.55), [P(title, 25, NAVY, True)])
    rect(s, Inches(0.55), Inches(1.16), Inches(12.23), Pt(1.2), LINE)
    footer(s)


def chip(s, x, y, label, color, h=Inches(0.3), fs=10):
    w = Inches(0.16 + 0.088 * len(label))
    sp = rounded(s, x, y, w, h, color)
    tf = sp.text_frame; tf.word_wrap = False
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = label
    r.font.size = Pt(fs); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FB
    return x + w + Inches(0.1)


_IMGDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "img")
_IMGMAP = [
    ("Tijeras de cosecha", "av_tijeras"), ("Pértiga telescópica", "av_pertiga"),
    ("Munckhof", "av_munckhof"), ("Revo Piuma", "av_revo"),
    ("Bins plásticos", "av_bins"), ("Telehandler", "av_telehandler"),
    ("ProFruit UNLOADER", "av_profruit"), ("Volteo suave", "av_volteo_suave"),
    ("Túnel de lavado", "av_lavado"), ("Secado (air knife)", "av_secado"),
    ("Copas basculantes", "av_copas"), ("Rodillos rotatorios", "av_rodillos"),
    ("Visión externa", "av_vision"), ("Calidad interna NIR", "av_nir"),
    ("Mesas de acumulación", "av_empaque"), ("Etiquetado PLU", "av_etiquetado"),
    ("Embalaje: malla", "av_embalaje"), ("Paletizado robótico", "av_paletizado"),
    ("Global Cooling", "av_preenfriado"), ("Otros preenfriadores", "av_preenf2"),
    ("Cámara de refrigeración", "av_frio"), ("Atmósfera controlada", "av_ca"),
    ("Generador de etileno", "av_etileno"), ("Cuartos de maduración", "av_madroom"),
]
def _img_for(name):
    for k, v in _IMGMAP:
        if k in name:
            p = os.path.join(_IMGDIR, v + ".png")
            return p if os.path.exists(p) else None
    return None


def machine_card(s, y, accent, name, country, funcion, specs, costo, proveedor, H=Inches(2.5)):
    X, W = Inches(0.78), Inches(11.78)
    LP = Inches(3.05)
    rounded(s, X, y, W, H, LIGHT)
    rounded(s, X, y, LP, H, accent, rad=0.05)
    rect(s, X + LP - Inches(0.14), y + Inches(0.02), Inches(0.14), H - Inches(0.04), accent)
    _p = _img_for(name)
    if _p:
        s.shapes.add_picture(_p, X + Inches(0.28), y + Inches(0.16), width=Inches(2.5), height=Inches(1.546))
    txt(s, X + Inches(0.18), y + H - Inches(0.42), LP - Inches(0.3), Inches(0.32),
        [[("● ", 9, WHITE, False, False), (country, 10, WHITE, False, False)]],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    rx = X + LP + Inches(0.22)
    rw = Inches(8.25)
    txt(s, rx, y + Inches(0.14), rw, Inches(0.5), [P(name, 14, NAVY, True)], ls=1.0)
    txt(s, rx, y + Inches(0.7), rw, Inches(0.5), [P(funcion, 11, INK, False)], ls=1.05)
    sy = y + Inches(1.24)
    for sp_txt in specs[:3]:
        rounded(s, rx, sy + Inches(0.05), Inches(0.13), Inches(0.13), accent)
        txt(s, rx + Inches(0.28), sy, rw - Inches(0.3), Inches(0.32),
            [P(sp_txt, 10.5, GRAY, False)], anchor=MSO_ANCHOR.MIDDLE, ls=1.0)
        sy += Inches(0.3)
    by = y + H - Inches(0.32)
    txt(s, rx, by, Inches(4.3), Inches(0.32),
        [[("Costo:  ", 10, accent, True, False), (costo, 10, INK, False, False)]],
        anchor=MSO_ANCHOR.MIDDLE, ls=1.0)
    txt(s, rx + Inches(4.35), by, Inches(3.9), Inches(0.32),
        [[("Dónde:  ", 10, accent, True, False), (proveedor, 10, INK, False, False)]],
        anchor=MSO_ANCHOR.MIDDLE, ls=1.0)


# ===========================================================================
# 1. PORTADA
# ===========================================================================
s = slide()
rect(s, 0, 0, EMU_W, EMU_H, NAVY)
rect(s, 0, Inches(6.7), EMU_W, Inches(0.12), GREEN)
rect(s, 0, Inches(6.82), EMU_W, Inches(0.06), CYAN)
rounded(s, Inches(0.85), Inches(0.8), Inches(0.62), Inches(0.62), BLUE)
txt(s, Inches(0.85), Inches(0.8), Inches(0.62), Inches(0.62), [P("H", 30, WHITE, True)],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(1.62), Inches(0.8), Inches(5), Inches(0.62), [P("Howy", 26, WHITE, True)],
    anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(0.85), Inches(2.45), Inches(11.6), Inches(0.4),
    [P("PRESENTACIÓN EJECUTIVA · INVESTIGACIÓN TÉCNICA", 13.5, CYAN, True)])
txt(s, Inches(0.85), Inches(2.95), Inches(11.7), Inches(1.9),
    [P("Maquinaria del proceso", 42, WHITE, True),
     P("del aguacate", 42, WHITE, True)], ls=1.02)
txt(s, Inches(0.85), Inches(5.05), Inches(11.4), Inches(0.9),
    [P("Cosecha · recepción · lavado · calibrado y selección · empaque · paletizado · cadena de frío",
       16, RGBColor(0xC6, 0xD3, 0xE6), False)], ls=1.15)
txt(s, Inches(0.85), Inches(6.95), Inches(9), Inches(0.4),
    [P("Partes mecánicas · funciones · costos · proveedores · datasheets · estructura de línea",
       10.5, RGBColor(0x9F, 0xB2, 0xCD), False)])
txt(s, Inches(11.0), Inches(6.95), Inches(1.45), Inches(0.4),
    [P("Julio 2026", 10.5, RGBColor(0x9F, 0xB2, 0xCD), False)], align=PP_ALIGN.RIGHT)


# ===========================================================================
# 2. RESUMEN / METODOLOGÍA
# ===========================================================================
s = slide()
header(s, "Resumen ejecutivo", "Alcance y método de la investigación")
txt(s, Inches(0.78), Inches(1.4), Inches(11.8), Inches(0.95),
    [P("Mapeamos toda la maquinaria que interviene desde que el aguacate se corta del árbol hasta que "
       "sale refrigerado hacia el cliente. La información proviene de sitios de fabricantes, catálogos, "
       "datasheets y documentos técnicos de todo el mundo (Europa, EE. UU., Australia, LATAM y China).",
       13.5, GRAY, False)], ls=1.15)
cards = [
    ("5", "etapas", "Campo, recepción, calibrado,\nempaque y cadena de frío.", GREEN),
    ("30+", "máquinas", "Descritas con partes,\nfunción, specs y costo.", BLUE),
    ("100%", "manual la cosecha", "El aguacate se magulla:\nno hay vibrador viable.", AMBER),
    ("NIR", "el corazón técnico", "Materia seca = madurez,\nmedida sin cortar la fruta.", CYAN),
]
cw, gap, x0, y0 = Inches(2.85), Inches(0.18), Inches(0.78), Inches(2.55)
for i, (big, small, desc, c) in enumerate(cards):
    x = x0 + i * (cw + gap)
    rounded(s, x, y0, cw, Inches(2.05), LIGHT)
    rect(s, x, y0, cw, Inches(0.09), c)
    txt(s, x + Inches(0.2), y0 + Inches(0.24), cw - Inches(0.36), Inches(0.7),
        [[(big, 34, c, True, False), ("  " + small, 12.5, NAVY, True, False)]], anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x + Inches(0.2), y0 + Inches(1.02), cw - Inches(0.4), Inches(0.95),
        [P(l, 11, GRAY, False) for l in desc.split("\n")], ls=1.08)
rounded(s, Inches(0.78), Inches(4.95), Inches(11.78), Inches(1.65), NAVY)
txt(s, Inches(1.1), Inches(5.12), Inches(11.2), Inches(0.35), [P("HILO CONDUCTOR", 11.5, CYAN, True)])
txt(s, Inches(1.1), Inches(5.45), Inches(11.2), Inches(1.05),
    [P("El aguacate (sobre todo Hass) es muy sensible al golpe y al daño de lenticelas. Por eso TODA la "
       "maquinaria está diseñada para un trato suave: volteo en seco, transportadores acolchados, ventosas "
       "y giro controlado. La tecnología de punta está en la selección óptica + NIR (materia seca), y la "
       "inversión es escalable: desde herramientas de decenas de dólares hasta líneas premium de millones.",
       12.5, WHITE, False)], ls=1.15, anchor=MSO_ANCHOR.MIDDLE)


# ===========================================================================
# 3. MAPA DE LA LÍNEA (flujo por fases)
# ===========================================================================
s = slide()
header(s, "Estructura de la línea", "Mapa del proceso, de principio a fin")
phases = [
    ("CAMPO", GREEN, ["1 · Cosecha manual", "2 · Acopio en bins", "3 · Transporte a planta"]),
    ("RECEPCIÓN", CYAN, ["4 · Volteo de bins", "5 · Preselección", "6 · Lavado y cepillado",
                          "7 · Encerado", "8 · Secado"]),
    ("CALIBRADO", BLUE, ["9 · Selección óptica", "10 · Peso + NIR (materia seca)", "11 · Distribución a salidas"]),
    ("EMPAQUE", AMBER, ["12 · Etiquetado PLU", "13 · Empaque en bandeja/caja", "14 · Embalaje", "15 · Paletizado"]),
    ("CADENA DE FRÍO", NAVY, ["16 · Preenfriado aire forzado", "17 · Frío / atmósfera controlada",
                              "18 · Maduración (etileno)", "19 · Despacho refrigerado"]),
]
y = Inches(1.45)
rh = Inches(1.06)
for ph, c, steps in phases:
    rounded(s, Inches(0.78), y, Inches(2.2), rh - Inches(0.12), c)
    txt(s, Inches(0.78), y, Inches(2.2), rh - Inches(0.12), [P(ph, 13, WHITE, True)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ls=0.95)
    cx = Inches(3.15)
    cyy = y + Inches(0.05)
    for stp in steps:
        w = Inches(0.16 + 0.088 * len(stp))
        if cx + w > Inches(12.55):
            cx = Inches(3.15); cyy += Inches(0.42)
        chip(s, cx, cyy, stp, c, h=Inches(0.34), fs=10)
        cx = cx + w + Inches(0.1)
    y += rh
txt(s, Inches(0.78), Inches(6.72), Inches(11.8), Inches(0.3),
    [P("Nota: el encerado es opcional según destino; la atmósfera controlada y la maduración se usan para exportación / retail.",
       9.5, GRAY, True)])


# ===========================================================================
# 4. COSECHA — HERRAMIENTAS MANUALES
# ===========================================================================
s = slide()
header(s, "Etapa 1 · Campo — cosecha", "Herramientas de cosecha manual", GREEN)
machine_card(s, Inches(1.4), GREEN,
    "Tijeras de cosecha (Manzana Nules M25-AM / Corona)", "España · EE. UU.",
    "Cortan el pedúnculo dejando ~3 mm de 'botón' sin dañar la piel del fruto.",
    ["Partes: hoja de corte cónica de acero, puntas y bordes redondeados, mango ergonómico",
     "Diseñadas específicamente para aguacate (evitan marcas y rayaduras)",
     "Datasheet: ajustables a distinto grosor de pedúnculo"],
    "USD 22.6 (Corona/Lobo); COP 293k–340k altura", "Manzana Nules, Lobo Products, Terravocado")
machine_card(s, Inches(4.05), GREEN,
    "Pértiga telescópica + cabezal con bolsa (TP300AL + M26 / Lobo)", "España · EE. UU.",
    "Cosecha en altura: sistema 'jalar y cortar' que deja caer el fruto en la bolsa.",
    ["Partes: pértiga de aluminio/fibra de vidrio 1.7–3.7 m, hoja endurecida, bolsa de poliéster",
     "Cabezal de doble ángulo; bolsa recolectora ~18 kg con anillos de descarga",
     "Fibra de vidrio no se dobla bajo carga (a diferencia del aluminio)"],
    "Pértiga USD 89.9; cabezal+bolsa USD 69.9", "Lobo Products (EE.UU.), Manzana Nules (ES)")


# ===========================================================================
# 5. COSECHA — PLATAFORMAS (HARVEST AIDS)
# ===========================================================================
s = slide()
header(s, "Etapa 1 · Campo — cosecha", "Plataformas de cosecha (harvest aids)", GREEN)
machine_card(s, Inches(1.4), GREEN,
    "Munckhof Pluk-O-Trak", "Países Bajos",
    "Plataforma autopropulsada: 4–6 recolectores + cintas depositan la fruta en cajas.",
    ["Partes: chasis autopropulsado, 2 plataformas elevables, 4–6 cintas transportadoras",
     "Datasheet (Senior): motor 9.7 kW, 1,140 kg, 4.7 m, árbol hasta 4 m",
     "Reduce costo de cosecha y daño hasta ~50%; gasolina/eléctrico/híbrido"],
    "Por cotización (usado: mercado NL)", "Munckhof (NL); dist. NP Seymour (UK)")
machine_card(s, Inches(4.05), GREEN,
    "Revo Piuma 4WD / Billo BIG 2000", "Italia",
    "Cosecha y poda en alta densidad; cintas laterales + central bajan la fruta al bin.",
    ["Partes: chasis 4WD autonivelante, plataforma 140×110 cm, compresor 50 L",
     "Altura máx. de plataforma 250 cm; dirección independiente 'auto-drive'",
     "IMPORTANTE: el aguacate NO se cosecha con vibrador — magullado 90–95% y daña el árbol"],
    "Por cotización", "Revo/Billo (IT); dist. Blueline, OESCO (EE.UU.)")


# ===========================================================================
# 6. TRANSPORTE EN CAMPO
# ===========================================================================
s = slide()
header(s, "Etapa 1 · Campo — logística", "Contenedores y manejo en campo", GREEN)
machine_card(s, Inches(1.4), GREEN,
    "Bins plásticos ventilados (MacroBin / IPL Schoeller)", "EE. UU. / global",
    "Recolectan, transportan y almacenan la fruta; paredes ventiladas para flujo de aire.",
    ["Partes: paredes ventiladas, base para montacargas, apilables e higiénicos",
     "Datasheet: 48×48×28 in; capacidad de carga ~667 L (MacroBin 24FV)",
     "Superan a la madera en carga, higiene y compatibilidad con frío"],
    "USD 189–349 por bin (Pallets & Bins)", "IPL Schoeller, TranPak, Buckhorn")
machine_card(s, Inches(4.05), GREEN,
    "Telehandler / montacargas todo terreno (Genie, JLG)", "EE. UU. / global",
    "Cargan y apilan los bins llenos al remolque o camión, en terreno de huerto.",
    ["Partes: pluma telescópica, horquillas, mástil, neumáticos off-road",
     "Datasheet: capacidad 2,270–5,440 kg; alcance ~18 ft (alto alcance hasta 56 ft)",
     "También tractores frutícolas estrechos con remolques portabines"],
    "Variable (compra/renta)", "Genie, JLG y distribuidores regionales")


# ===========================================================================
# 7. RECEPCIÓN Y VOLTEO DE BINS
# ===========================================================================
s = slide()
header(s, "Etapa 2 · Recepción", "Volteo de bins (seco vs. húmedo)", CYAN)
machine_card(s, Inches(1.4), CYAN,
    "Volteador ProFruit UNLOADER 800", "Polonia",
    "Levanta el bin y vierte la fruta gradualmente sobre la cinta clasificadora (1er paso).",
    ["Partes: accionamiento hidráulico, superficies inox grado alimenticio, control por palanca",
     "Datasheet: caja máx. 120×120×85 cm, capacidad de carga 800 kg",
     "También versión UNLOADER 500"],
    "Por cotización", "ProFruit (Polonia)")
machine_card(s, Inches(4.05), CYAN,
    "Volteo suave / seco (KW Soft Auto · Unitec UNI ROV · ICOEL)", "Australia · Italia",
    "Vaciado gradual y suave para fruta delicada; evita el impacto que causa magullado.",
    ["Partes: inox, destacador (de-stacker) y apilador de bins vacíos, estaciones buffer",
     "Volteo SECO preferido en aguacate (menos daño y sin exceso de humedad)",
     "Volteo húmedo (a canal de agua) es común en cítricos, menos en aguacate"],
    "Por cotización", "KW Automation (AU), Unitec/ICOEL (IT)")


# ===========================================================================
# 8. LAVADO, SECADO, ENCERADO
# ===========================================================================
s = slide()
header(s, "Etapa 2 · Recepción", "Lavado, cepillado, secado y encerado", CYAN)
machine_card(s, Inches(1.4), CYAN,
    "Túnel de lavado y cepillado", "Líneas MAF/GREEFA/TOMRA y chinas",
    "Aspersión a alta presión + túnel de cepillos que limpian y sanitizan la fruta.",
    ["Partes: tanque de burbujas + elevador de rodillos, cepillos de crin/nylon, boquillas, bomba",
     "Cepillos por color: verde (agita/sanitiza), rojo (quita agua), negro (pulido)",
     "Datasheet: 1–20 t/h; inox SS304 (contacto) / SS316; tanque 2.45 m³; agua 1.5 t/h"],
    "Parte del rango de línea (ver costos)", "MAF, GREEFA, TOMRA; chinos (Gelgoog)")
machine_card(s, Inches(4.05), CYAN,
    "Secado (air knife) + encerado", "Global",
    "Cuchilla de aire retira las gotas; el encerado (opcional) da brillo y vida útil.",
    ["Partes: soplador de alta velocidad / cuchillas de aire, ventiladores, aplicador de cera",
     "Encerado según mercado destino; seguido de túnel de secado con aire caliente",
     "Cepillos pulidores finales antes del calibrado"],
    "Incluido en la línea llave en mano", "Integradores de línea (ver proveedores)")


# ===========================================================================
# 9. CALIBRADO POR PESO — MECÁNICA
# ===========================================================================
s = slide()
header(s, "Etapa 3 · Calibrado y selección", "Calibrado por peso — mecánica", BLUE)
machine_card(s, Inches(1.4), BLUE,
    "Copas basculantes (tipping cups) + celda de carga", "Tecnología base",
    "Cada fruto viaja en una copa; se pesa en movimiento y la copa vuelca en la salida por calibre.",
    ["Partes: copas sobre cadena, celda de carga por posición, actuador de volcado, PLC",
     "Requiere singulación previa (una fruta por copa) para pesar con precisión",
     "Asigna cada aguacate a su salida por peso (calibres 48/60/70…)"],
    "Integrado en la calibradora", "Van Doren, MAF, Aweta, GREEFA")
machine_card(s, Inches(4.05), BLUE,
    "Rodillos rotatorios (roller cups) + singulador", "Tecnología base",
    "Giran la fruta 360° para que las cámaras capten toda la superficie; luego descargan.",
    ["Partes: rodillos de gran diámetro, singulador de entrada, transportador",
     "Permite inspección visual total (color, defectos) durante el giro",
     "Datasheet típico: ~2 t/carril/h y 95% de precisión (TOMRA hasta ~5 t/carril/h)"],
    "Integrado en la calibradora", "TOMRA/Compac, GREEFA, MAF")


# ===========================================================================
# 10. SELECCIÓN ÓPTICA + NIR
# ===========================================================================
s = slide()
header(s, "Etapa 3 · Calibrado y selección", "Selección óptica + calidad interna (NIR)", BLUE)
machine_card(s, Inches(1.4), BLUE,
    "Visión externa (cámaras + iluminación LED)", "TOMRA, GREEFA, MAF, GP Graders",
    "Evalúan color, tamaño, forma y defectos de piel (cortes, magulladuras, roña, insectos).",
    ["Partes: túnel multicámara RGB, LED difusa, procesador de imagen, software",
     "TOMRA Spectrim + LUCAi usa IA de aprendizaje profundo para clasificar defectos",
     "GREEFA iQS · MAF Globalscan (360°) · GP Graders gpVision (HD)"],
    "Módulo de línea (cotización)", "Fabricantes premium (ver tabla)")
machine_card(s, Inches(4.05), BLUE,
    "Calidad interna NIR — materia seca / madurez", "Infrarrojo cercano (no destructivo)",
    "Mide la materia seca (% → aceite = madurez) y detecta pardeamiento sin cortar la fruta.",
    ["Inline: TOMRA Inspectra² (materia seca/Brix), GREEFA iFA (imagen IR), Aweta Inscan (materia seca + aceite)",
     "Portátil de mano: Felix F-751 Avocado Quality Meter (materia seca 14–40%, ±1.15 DM)",
     "Materia seca mínima de cosecha (Hass) ~20–23% según norma del país"],
    "Portátil ≈ USD 5,400 (£4,263); inline: cotización", "Felix Instruments; fabricantes de línea")


# ===========================================================================
# 11. TABLA — MARCAS LÍDERES DE CALIBRADO
# ===========================================================================
s = slide()
header(s, "Etapa 3 · Calibrado y selección", "Marcas líderes de líneas de calibrado", BLUE)
rows = [
    ("Marca", "País", "Tecnología clave", "Capacidad / dato", True),
    ("Van Doren Sales", "EE. UU.", "Peso por copas + celdas de carga", "Alto volumen", False),
    ("GP Graders", "Australia", "AirJet + gpVision (visión + peso)", "hasta 32 frutos/s por carril", False),
    ("MAF Roda", "Francia", "Globalscan 360° + NIR/IDD (Insight)", "líneas multicarril", False),
    ("GREEFA", "P. Bajos", "GeoSort + iQS (ext.) + iFA (interno IR)", "robot empaque 100 pzas/min", False),
    ("TOMRA / Compac", "Noruega / NZ", "Spectrim + LUCAi (IA) + Inspectra² NIR", "~5 t/carril/h (premium)", False),
    ("Aweta", "P. Bajos", "Peso/volumen + visión + NIR", "KG3 ±2 g de exactitud", False),
    ("Unitec · Multiscan", "Italia · España", "Visión artificial (Avocado Vision)", "a medida", False),
    ("Reemoon · Gelgoog", "China", "Peso + visión (+Brix) — bajo costo", "1–20 t/h", False),
]
tx, ty, tw = Inches(0.78), Inches(1.42), Inches(11.78)
colw = [Inches(2.6), Inches(1.85), Inches(4.9), Inches(2.43)]
hh = Inches(0.5); rh2 = Inches(0.535)
rounded(s, tx, ty, tw, hh, NAVY)
cx = tx
for j in range(4):
    al = PP_ALIGN.LEFT if j != 1 else PP_ALIGN.CENTER
    txt(s, cx + Inches(0.14), ty, colw[j] - Inches(0.2), hh, [P(rows[0][j], 11.5, WHITE, True)],
        align=al, anchor=MSO_ANCHOR.MIDDLE)
    cx += colw[j]
for i, row in enumerate(rows[1:]):
    yy = ty + hh + Emu(int(rh2 * i))
    rect(s, tx, yy, tw, rh2, WHITE if i % 2 == 0 else LIGHT)
    cx = tx
    for j in range(4):
        al = PP_ALIGN.LEFT if j != 1 else PP_ALIGN.CENTER
        bold = (j == 0)
        col = NAVY if j == 0 else GRAY
        txt(s, cx + Inches(0.14), yy, colw[j] - Inches(0.2), rh2,
            [P(row[j], 11 if j != 2 else 10.5, col, bold)], align=al, anchor=MSO_ANCHOR.MIDDLE)
        cx += colw[j]
txt(s, tx, Inches(6.75), tw, Inches(0.3),
    [P("Ningún fabricante premium publica precios de lista: las líneas se cotizan por proyecto (nº de carriles, módulos NIR, capacidad).",
       9.5, GRAY, True)])


# ===========================================================================
# 12. EMPAQUE Y ETIQUETADO
# ===========================================================================
s = slide()
header(s, "Etapa 4 · Empaque", "Empaque, llenado y etiquetado", AMBER)
machine_card(s, Inches(1.4), AMBER,
    "Mesas de acumulación y llenado de cajas (tray fillers)", "MAF · GREEFA · Unitec · Berjeda",
    "Reúnen la fruta ya calibrada y la depositan en bandeja/caja por peso o por conteo.",
    ["Partes: bandas de acumulación, celdas de carga, cámara de conteo, cilindros neumáticos, robot pick&place",
     "Unitec 'UNIQ' y GREEFA SmartPackr empacan en bandejas con robot (hasta 100 pzas/min)",
     "Van Doren COR: cambio de formato en < 60 s"],
    "Por cotización", "MAF, GREEFA, Unitec; Berjeda (ES), ASLAN (MX)")
machine_card(s, Inches(4.05), AMBER,
    "Etiquetado PLU (Sinclair CPL)", "Reino Unido",
    "Aplica una etiqueta PLU a cada aguacate dispuesto en bandeja, en un solo paso.",
    ["Partes: hasta 16 cabezales aplicadores, cepillos de fijación, banda motorizada, HMI",
     "Datasheet: hasta 2,640 bandejas/h; etiqueta 18–26 mm; reconocimiento de patrón A/B",
     "Sistemas multi-carril hasta 720 frutas/min"],
    "Por cotización", "Sinclair International (datasheet PDF)")


# ===========================================================================
# 13. EMBALAJE Y PALETIZADO
# ===========================================================================
s = slide()
header(s, "Etapa 4 · Empaque", "Embalaje y paletizado", AMBER)
machine_card(s, Inches(1.4), AMBER,
    "Embalaje: malla/clip · flow pack · case packer", "Volm · ULMA · Van Doren",
    "Empaca en malla (2–4 uds.), envoltura flow pack o arma y llena la caja de cartón.",
    ["Partes: cabezal clipador de doble grapa, mordazas selladoras, ventosas, magazine de cajas",
     "Malla: Volm/NNZ · Flow pack HFFS: ULMA · Case packer robótico: Van Doren COR, FANUC/ABB",
     "Robot Aporo (Robotics Plus): 100–120 frutas/min con ventosas (trato suave)"],
    "Clipadoras: gama económica", "Volm, NNZ, ULMA, Robotics Plus")
machine_card(s, Inches(4.05), AMBER,
    "Paletizado robótico + envoltura de tarima", "ABB · FANUC · KUKA · Robopac",
    "Apila las cajas en la tarima por patrón y la envuelve con film estirable para transporte.",
    ["Partes: robot 4–6 ejes, garra de vacío, mesa giratoria, carro de film pre-estirado, PLC",
     "Datasheet: ABB IRB 460/660 ~2,000 ciclos/h; Robopac Masterplat turntable 2,000 kg",
     "Opción china KR-120: 6 ejes, 120 kg, ciclo 8 s, 17–25 kW, aire 7 bar"],
    "Paletizador chino KR-120: USD 23,000–24,000/set", "ABB/FANUC/KUKA; Robopac, Signode")


# ===========================================================================
# 14. PREENFRIAMIENTO
# ===========================================================================
s = slide()
header(s, "Etapa 5 · Cadena de frío", "Preenfriamiento por aire forzado", NAVY)
machine_card(s, Inches(1.4), NAVY,
    "Global Cooling Jet-Ready Precooler", "EE. UU.",
    "Baja la temperatura de la pulpa rápidamente tras cosecha para frenar la maduración.",
    ["Partes: 2 ventiladores de 10 HP, bastidor de acero galvanizado, plénum, cortinas de sellado",
     "Datasheet: > 4,000 CFM por pallet, operando con 8 pallets",
     "Aire refrigerado succionado horizontalmente a través de las cajas"],
    "Por cotización", "Global Cooling Inc. (EE.UU.)")
machine_card(s, Inches(4.05), NAVY,
    "Otros preenfriadores (TRJ · MACS · chinos)", "EE. UU. · China",
    "Unidades de aire forzado portátiles o automáticas integradas a la cámara.",
    ["TRJ 'SuperFlow'; MACS Cool (automático por lotes de 6 pallets)",
     "Referencia de capacidad: enfriar 40 t de aguacate en 24 h con 160 kW instalados",
     "Precoolers chinos (Coldmax, Hejia): opción de bajo costo"],
    "Chinos: gama baja; marca: cotización", "TRJ, MACS Cool, Coldmax, InspiraFarms")


# ===========================================================================
# 15. FRÍO Y ATMÓSFERA CONTROLADA
# ===========================================================================
s = slide()
header(s, "Etapa 5 · Cadena de frío", "Refrigeración y atmósfera controlada", NAVY)
machine_card(s, Inches(1.4), NAVY,
    "Cámara de refrigeración (cold room)", "Global",
    "Almacena el aguacate a ~4–7 °C para conservar calidad hasta el despacho.",
    ["Partes: unidad condensadora (compresor), evaporadores, paneles aislantes de poliuretano",
     "Sistemas DX (directa) para capacidades chicas/medias; chiller para plantas grandes",
     "Control de temperatura y humedad relativa"],
    "Por m³, baja al subir el volumen", "Frigomekanik, InspiraFarms, chinos")
machine_card(s, Inches(4.05), NAVY,
    "Atmósfera controlada — generador N₂ PSA (Absoger F75)", "Francia · Italia",
    "Genera nitrógeno para desplazar el O₂ y bajar la cámara/contenedor a atmósfera controlada.",
    ["Partes: torres con tamiz molecular de carbono, compresor, scrubber de CO₂, controlador",
     "Datasheet (Absoger PSA F75): 209 m³/h a 2% O₂, 8 bar, compresores 55 kW",
     "Trata 100–1,200 t de fruta/día; usado en contenedores CA para exportación"],
    "Por cotización", "Absoger (FR), Isolcell (IT)")


# ===========================================================================
# 16. MADURACIÓN CON ETILENO
# ===========================================================================
s = slide()
header(s, "Etapa 5 · Cadena de frío", "Maduración con etileno ('ripe & ready')", NAVY)
machine_card(s, Inches(1.4), NAVY,
    "Generador de etileno Catalytic Easy-Ripe", "EE. UU.",
    "Genera etileno controlado a partir de concentrado líquido para una maduración uniforme.",
    ["Partes: cámara catalítica calefactada, depósito de 2 L, controlador de tasa ajustable",
     "Datasheet: 160 W; 0.5–2 L etileno/24 h; cuarto de 57 a 285 m³; 31×24×25 cm",
     "Parámetros aguacate: 100 ppm etileno, 15–20 °C, 90–95% HR, controlar CO₂"],
    "Por cotización (QA Supplies, HundredX)", "Catalytic Generators (EE.UU.)")
machine_card(s, Inches(4.05), NAVY,
    "Cuartos de maduración llave en mano (Interko OPTIMO)", "Países Bajos · UK · EE.UU.",
    "Cuarto completo que controla aire, temperatura, humedad, O₂, CO₂ y etileno.",
    ["Partes: ventiladores reversibles, evaporadores, control integrado, inyección de etileno",
     "Interko OPTIMO: 8–24 pallets; también Softripe (JD Cooling), DASERCO, Thermal Tech",
     "Instrumentación de control: Felix AccuRipe / F-950 (CO₂/O₂/etileno)"],
    "Por cotización (proyecto)", "Interko (NL), JD Cooling (UK), DASERCO (EE.UU.)")


# ===========================================================================
# 17. COSTOS Y ECONOMÍA
# ===========================================================================
s = slide()
header(s, "Economía", "Costos: qué cuesta cada bloque", BLUE)
costs = [
    ("Herramientas de cosecha manual", "USD 22 – 90", GREEN, "Tijeras, pértigas, bolsas (Lobo Products)"),
    ("Bins plásticos ventilados", "USD 189 – 349 c/u", GREEN, "MacroBin (Pallets & Bins)"),
    ("Medidor NIR de mano (materia seca)", "≈ USD 5,400 (£4,263)", CYAN, "Felix F-751 (distribuidores UK)"),
    ("Paletizador robótico (China, KR-120)", "USD 23,000 – 24,000 / set", AMBER, "Único precio público concreto (FOB China)"),
    ("Línea china completa (lavado→calibrado)", "USD 7,000 – 50,000", BLUE, "12-grados ~USD 15,000/set; módulo simple desde USD 1,400"),
    ("Línea integrada media / alta (multicarril)", "USD 80,000 – 400,000", BLUE, "Sorting/grading integrado (sin obra ni frío)"),
    ("Línea premium turnkey + NIR interno", "Cientos de miles a millones", NAVY, "TOMRA / MAF / GREEFA — solo por cotización"),
]
y = Inches(1.45)
for i, (label, price, c, note) in enumerate(costs):
    yy = y + i * Inches(0.72)
    rounded(s, Inches(0.78), yy, Inches(11.78), Inches(0.62), LIGHT)
    rect(s, Inches(0.78), yy, Inches(0.12), Inches(0.62), c)
    txt(s, Inches(1.05), yy, Inches(5.1), Inches(0.62), [P(label, 12.5, NAVY, True)],
        anchor=MSO_ANCHOR.MIDDLE, ls=1.0)
    txt(s, Inches(6.2), yy, Inches(3.15), Inches(0.62), [P(price, 12.5, c, True)],
        anchor=MSO_ANCHOR.MIDDLE, ls=1.0)
    txt(s, Inches(9.4), yy, Inches(3.05), Inches(0.62), [P(note, 9.8, GRAY, False)],
        anchor=MSO_ANCHOR.MIDDLE, ls=1.0)
txt(s, Inches(0.78), Inches(6.68), Inches(11.8), Inches(0.34),
    [P("La cadena de frío (preenfriado, cámaras, CA y maduración) se cotiza aparte por proyecto y suele sumar tanto o más que la línea de calibrado.",
       9.5, GRAY, True)])


# ===========================================================================
# 18. PROVEEDORES POR REGIÓN
# ===========================================================================
s = slide()
header(s, "Dónde se obtiene", "Proveedores por bloque y región", BLUE)
prov = [
    ("Cosecha (herramientas y plataformas)", GREEN,
     "Manzana Nules (ES) · Lobo Products (EE.UU.) · Munckhof (NL) · Revo, Billo (IT) · Terravocado (CO)"),
    ("Recepción, lavado y calibrado — alta tecnología", BLUE,
     "MAF Roda (FR) · GREEFA, Aweta (NL) · Unitec (IT) · Multiscan (ES) · TOMRA (NO/NZ) · Van Doren (EE.UU.) · GP Graders (AU)"),
    ("Línea completa de bajo costo", CYAN,
     "Reemoon · Gelgoog · fruitprocess (China) — líneas lavado+secado+encerado+calibrado 1–20 t/h"),
    ("Empaque, etiquetado y paletizado", AMBER,
     "Sinclair (UK) · Robotics Plus (NZ) · Volm, NNZ (EE.UU.) · ULMA (ES) · ABB/FANUC/KUKA · Robopac, Signode"),
    ("Cadena de frío, atmósfera controlada y maduración", NAVY,
     "Global Cooling, TRJ, Catalytic (EE.UU.) · Interko, Van Amerongen (NL) · Softripe/JD Cooling (UK) · Absoger (FR) · Isolcell (IT) · InspiraFarms (UK/Kenia)"),
    ("Representantes / integración en LATAM", GRAY,
     "Berjeda (ES) y ASLAN Industrial (MX) instalan en México, Perú, Chile y Colombia · usados en Duijndam Machines (NL), Machinio"),
]
y = Inches(1.5)
for i, (t, c, d) in enumerate(prov):
    yy = y + i * Inches(0.86)
    rounded(s, Inches(0.78), yy, Inches(11.78), Inches(0.76), LIGHT)
    rect(s, Inches(0.78), yy, Inches(0.12), Inches(0.76), c)
    txt(s, Inches(1.05), yy + Inches(0.08), Inches(11.3), Inches(0.32), [P(t, 12.5, NAVY, True)])
    txt(s, Inches(1.05), yy + Inches(0.4), Inches(11.35), Inches(0.34), [P(d, 10.8, GRAY, False)], ls=1.0)


# ===========================================================================
# 19. DATASHEETS Y FUENTES
# ===========================================================================
s = slide()
header(s, "Referencias", "Datasheets y fuentes oficiales")
txt(s, Inches(0.78), Inches(1.4), Inches(5.9), Inches(0.3), [P("DATASHEETS / CATÁLOGOS (PDF)", 12, BLUE, True)])
ds = [
    "Sinclair CPL — etiquetadora de patrón (PDF)",
    "Munckhof Pluk-O-Trak — brochure (PDF)",
    "Revo Piuma 4WD — catálogo AgriExpo (PDF)",
    "Catalytic Easy-Ripe — datasheet generador etileno",
    "Absoger PSA F75 — generador N₂ (postharvest.biz)",
    "Felix F-751 — Avocado Quality Meter (NIR)",
]
for i, d in enumerate(ds):
    yy = Inches(1.8) + i * Inches(0.52)
    rounded(s, Inches(0.78), yy + Inches(0.04), Inches(0.15), Inches(0.15), BLUE)
    txt(s, Inches(1.05), yy, Inches(5.5), Inches(0.42), [P(d, 11.5, INK, False)], anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(6.9), Inches(1.4), Inches(5.7), Inches(0.3), [P("SITIOS DE FABRICANTES", 12, BLUE, True)])
srcs = [
    "tomra.com/food/categories/fruit/avocados",
    "greefa.com · maf-roda.com · aweta.com",
    "gpgraders.com · unisorting.com · multiscan.eu",
    "vandorensales.com · sinclair-intl.com",
    "roboticsplus.co.nz · volmcompanies.com",
    "catalyticgenerators.com · interko.com",
    "felixinstruments.com · inspirafarms.com",
    "manzana-nules.com · loboproductsinc.com · munckhof.org",
]
for i, d in enumerate(srcs):
    yy = Inches(1.8) + i * Inches(0.52)
    rounded(s, Inches(6.9) + Inches(0.0), yy + Inches(0.04), Inches(0.15), Inches(0.15), CYAN)
    txt(s, Inches(7.17), yy, Inches(5.4), Inches(0.42), [P(d, 11, INK, False)], anchor=MSO_ANCHOR.MIDDLE)
rounded(s, Inches(0.78), Inches(6.5), Inches(11.78), Inches(0.5), LIGHT)
txt(s, Inches(1.05), Inches(6.5), Inches(11.3), Inches(0.5),
    [[("Nota: ", 10.5, BLUE, True, False),
      ("los precios y specs de equipos de marca casi nunca son públicos; donde no hay dato verificable se indicó 'por cotización'. Verificar con el fabricante.",
       10.5, GRAY, False, False)]], anchor=MSO_ANCHOR.MIDDLE)


# ===========================================================================
# 20. CONCLUSIONES
# ===========================================================================
s = slide()
header(s, "Conclusiones", "Hallazgos clave")
finds = [
    ("El fruto manda", "El aguacate es delicado: toda la maquinaria prioriza el trato suave (volteo seco, cintas acolchadas, ventosas, giro controlado)."),
    ("Cosecha manual", "No existe cosecha mecánica viable: el vibrador causa 90–95% de magullado y daña el árbol. Se usa tijera + pértiga + bolsa y plataformas de apoyo."),
    ("El corazón es la visión + NIR", "La tecnología de punta está en la selección óptica (IA) y el NIR de materia seca, que mide la madurez sin cortar el fruto."),
    ("Inversión escalable", "Desde herramientas de decenas de dólares y líneas chinas (USD 1.4k–8k) hasta líneas premium de cientos de miles a millones."),
    ("Geografía del mercado", "Europa, EE.UU. y Australia lideran la alta tecnología; China ofrece bajo costo; LATAM compra vía representantes e integra localmente."),
]
y = Inches(1.5)
for i, (t, d) in enumerate(finds):
    yy = y + i * Inches(1.02)
    rounded(s, Inches(0.78), yy, Inches(0.5), Inches(0.5), BLUE)
    txt(s, Inches(0.78), yy, Inches(0.5), Inches(0.5), [P(str(i + 1), 18, WHITE, True)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(1.45), yy - Inches(0.02), Inches(11.1), Inches(0.4), [P(t, 15, NAVY, True)])
    txt(s, Inches(1.45), yy + Inches(0.36), Inches(11.1), Inches(0.6), [P(d, 12, GRAY, False)], ls=1.08)


# ===========================================================================
# 21. CIERRE
# ===========================================================================
s = slide()
rect(s, 0, 0, EMU_W, EMU_H, NAVY)
rect(s, 0, 0, EMU_W, Inches(0.12), GREEN)
rect(s, 0, Inches(0.12), EMU_W, Inches(0.06), CYAN)
rounded(s, Inches(5.85), Inches(2.35), Inches(0.72), Inches(0.72), BLUE)
txt(s, Inches(5.85), Inches(2.35), Inches(0.72), Inches(0.72), [P("H", 34, WHITE, True)],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, 0, Inches(3.35), EMU_W, Inches(0.7), [P("Gracias", 40, WHITE, True)], align=PP_ALIGN.CENTER)
txt(s, 0, Inches(4.25), EMU_W, Inches(0.6),
    [P("Del árbol al contenedor: toda la maquinaria del aguacate, mapeada.",
       16, RGBColor(0xC6, 0xD3, 0xE6), False)], align=PP_ALIGN.CENTER)
txt(s, 0, Inches(6.7), EMU_W, Inches(0.4),
    [[("Howy", 12, CYAN, True, False),
      ("   ·   Investigación técnica   ·   Julio 2026", 12, RGBColor(0x9F, 0xB2, 0xCD), False, False)]],
    align=PP_ALIGN.CENTER)


out = "/home/user/Work/presentaciones/Howy_Maquinaria_Aguacate_2026.pptx"
prs.save(out)
print("OK ->", out, "| slides:", len(prs.slides._sldIdLst))
