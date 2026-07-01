# -*- coding: utf-8 -*-
"""
Presentación ejecutiva — Howy
Maquinaria del proceso de NOPAL y TUNA, con enfoque en RÉPLICA MEXICANA
(componentes y proveedores nacionales vs. importar). Diseño Howy. PPTX 16:9.
Fuentes: fabricantes mexicanos, portales (QuiMinet, MercadoLibre), datasheets, FAO/INIFAP.
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
MXRED = RGBColor(0xC1, 0x3A, 0x3A)
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


def slide(): return prs.slides.add_slide(BLANK)


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


def Pr(t, sz, col, bold=False, ital=False): return [(t, sz, col, bold, ital)]


def txt(s, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, sa=3, ls=1.0, wrap=True):
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
          ("  ·  Maquinaria del nopal — réplica mexicana — 2026", 9, GRAY, False, False)]],
        anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(11.9), Inches(7.06), Inches(0.9), Inches(0.3),
        [Pr(f"{_page[0]:02d}", 9, GRAY)], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def header(s, kicker, title, accent=BLUE):
    rect(s, Inches(0.55), Inches(0.4), Inches(0.09), Inches(0.5), accent)
    txt(s, Inches(0.78), Inches(0.28), Inches(11.6), Inches(0.28), [Pr(kicker.upper(), 11, accent, True)])
    txt(s, Inches(0.78), Inches(0.52), Inches(11.9), Inches(0.55), [Pr(title, 25, NAVY, True)])
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
    ("Corte manual", "no_corte"), ("EPP y acarreo", "no_epp"),
    ("Nopalli", "no_desespina"), ("Línea DESINOX", "no_desinox"),
    ("cepillos/rodillos en seco", "no_tuna_brush"), ("Benchmark a NO importar", "no_agrilux"),
    ("Lavadora por inmersión", "no_lav_inmersion"), ("Lavado por burbujas", "no_lav_burbujas"),
    ("Picadora de nopal INALSA", "no_picadora"), ("Cortadora en cubos", "no_cortadora_cubos"),
    ("Escaldadora", "no_escaldado"), ("Bandas y mesas", "no_bandas"),
    ("Deshidratador de charolas", "no_deshid_charolas"), ("Deshidratador solar", "no_deshid_solar"),
    ("Molino de martillos", "no_molino"), ("Tamizado", "no_tamizado"),
    ("Despulpadora", "no_despulpadora"), ("valor agregado", "no_valor"),
    ("Dosificadora de polvo", "no_dosificadora"), ("Empaque de nopal fresco", "no_map"),
]
def _img_for(name):
    for k, v in _IMGMAP:
        if k in name:
            p = os.path.join(_IMGDIR, v + ".png")
            return p if os.path.exists(p) else None
    return None


def machine_card(s, y, accent, name, country, funcion, specs, costo, mx, H=Inches(2.5)):
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
    rx = X + LP + Inches(0.22); rw = Inches(8.25)
    txt(s, rx, y + Inches(0.14), rw, Inches(0.5), [Pr(name, 14, NAVY, True)], ls=1.0)
    txt(s, rx, y + Inches(0.7), rw, Inches(0.5), [Pr(funcion, 11, INK, False)], ls=1.05)
    sy = y + Inches(1.24)
    for sp_txt in specs[:3]:
        rounded(s, rx, sy + Inches(0.05), Inches(0.13), Inches(0.13), accent)
        txt(s, rx + Inches(0.28), sy, rw - Inches(0.3), Inches(0.32), [Pr(sp_txt, 10.5, GRAY, False)],
            anchor=MSO_ANCHOR.MIDDLE, ls=1.0)
        sy += Inches(0.3)
    by = y + H - Inches(0.32)
    txt(s, rx, by, Inches(4.3), Inches(0.32), [[("Costo:  ", 10, accent, True, False), (costo, 10, INK, False, False)]],
        anchor=MSO_ANCHOR.MIDDLE, ls=1.0)
    txt(s, rx + Inches(4.35), by, Inches(3.9), Inches(0.32),
        [[("México:  ", 10, GREEN, True, False), (mx, 10, INK, False, False)]], anchor=MSO_ANCHOR.MIDDLE, ls=1.0)


# ===========================================================================
# 1. PORTADA
# ===========================================================================
s = slide()
rect(s, 0, 0, EMU_W, EMU_H, NAVY)
rect(s, 0, Inches(6.7), EMU_W, Inches(0.12), GREEN)
rect(s, 0, Inches(6.82), EMU_W, Inches(0.06), MXRED)
rounded(s, Inches(0.85), Inches(0.8), Inches(0.62), Inches(0.62), BLUE)
txt(s, Inches(0.85), Inches(0.8), Inches(0.62), Inches(0.62), [Pr("H", 30, WHITE, True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(1.62), Inches(0.8), Inches(5), Inches(0.62), [Pr("Howy", 26, WHITE, True)], anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(0.85), Inches(2.4), Inches(11.6), Inches(0.4), [Pr("PRESENTACIÓN EJECUTIVA · INVESTIGACIÓN TÉCNICA", 13.5, CYAN, True)])
txt(s, Inches(0.85), Inches(2.9), Inches(11.7), Inches(1.9),
    [Pr("Maquinaria del proceso", 42, WHITE, True), Pr("del nopal y la tuna", 42, WHITE, True)], ls=1.02)
txt(s, Inches(0.85), Inches(5.0), Inches(11.5), Inches(0.9),
    [[("Enfoque: ", 17, GREEN, True, False),
      ("componentes para una réplica mexicana (fabricación nacional) en lugar de importar",
       17, RGBColor(0xC6, 0xD3, 0xE6), False, False)]], ls=1.15)
txt(s, Inches(0.85), Inches(6.95), Inches(9), Inches(0.4),
    [Pr("Cosecha · desespinado · lavado · corte · deshidratado · molienda · empaque · componentes MX", 10.5, RGBColor(0x9F, 0xB2, 0xCD), False)])
txt(s, Inches(11.0), Inches(6.95), Inches(1.45), Inches(0.4), [Pr("Julio 2026", 10.5, RGBColor(0x9F, 0xB2, 0xCD), False)], align=PP_ALIGN.RIGHT)


# ===========================================================================
# 2. RESUMEN / ENFOQUE
# ===========================================================================
s = slide()
header(s, "Resumen ejecutivo", "México produce el nopal; puede producir la máquina", GREEN)
txt(s, Inches(0.78), Inches(1.4), Inches(11.8), Inches(0.95),
    [Pr("México es el primer productor mundial de nopal y tuna, pero la maquinaria industrial más completa "
        "suele importarse. La buena noticia: casi toda la línea es replicable en México con talleres de acero "
        "inoxidable y componentes de catálogo (motores, bandas, cepillos, cuchillas) de venta nacional.",
        13.5, GRAY, False)], ls=1.15)
cards = [
    ("#1", "productor mundial", "~845 mil t de nopal y\n~409 mil t de tuna (2024).", GREEN),
    ("80-90%", "componentes de catálogo", "Estructura inox + piezas\nestándar nacionales.", BLUE),
    ("20-25", "nopales/min", "Una desespinadora vs. 5-6\na mano: cuello de botella.", CYAN),
    ("MX", "ya lo fabrica", "Nopalea, DESINOX, INALSA,\nVEYCO, Equitek, Tecnodac.", AMBER),
]
cw, gap, x0, y0 = Inches(2.85), Inches(0.18), Inches(0.78), Inches(2.55)
for i, (big, small, desc, c) in enumerate(cards):
    x = x0 + i * (cw + gap)
    rounded(s, x, y0, cw, Inches(2.05), LIGHT)
    rect(s, x, y0, cw, Inches(0.09), c)
    txt(s, x + Inches(0.2), y0 + Inches(0.24), cw - Inches(0.36), Inches(0.7),
        [[(big, 30, c, True, False), ("  " + small, 11.5, NAVY, True, False)]], anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x + Inches(0.2), y0 + Inches(1.02), cw - Inches(0.4), Inches(0.95),
        [Pr(l, 11, GRAY, False) for l in desc.split("\n")], ls=1.08)
rounded(s, Inches(0.78), Inches(4.95), Inches(11.78), Inches(1.65), NAVY)
txt(s, Inches(1.1), Inches(5.12), Inches(11.2), Inches(0.35), [Pr("TESIS DE ESTA PRESENTACIÓN", 11.5, CYAN, True)])
txt(s, Inches(1.1), Inches(5.45), Inches(11.2), Inches(1.05),
    [Pr("La maquinaria de nopal no es tecnología cerrada: es una estructura de acero inoxidable 304 + "
        "componentes electromecánicos estándar (motores WEG, rodamientos SKF, cepillos a medida, variadores "
        "Delta). Fabricar en México da refacciones inmediatas, adaptación a la variedad local y menor costo "
        "total. Solo el corte de precisión y el control fino (PLC/servo/vacío) ameritan compra especializada.",
        12, WHITE, False)], ls=1.13, anchor=MSO_ANCHOR.MIDDLE)


# ===========================================================================
# 3. MAPA DE LA LÍNEA
# ===========================================================================
s = slide()
header(s, "Estructura de la línea", "Mapa del proceso (nopal-verdura)", GREEN)
phases = [
    ("COSECHA", GREEN, ["1 · Corte manual", "2 · Acarreo en cajas"]),
    ("LIMPIEZA", CYAN, ["3 · Recepción y selección", "4 · Lavado / desinfección", "5 · Desespinado", "6 · Desorillado"]),
    ("TRANSFORMA", BLUE, ["7 · Corte (cubos/tiras)", "8 · Escaldado (quita baba)", "9 · Enfriado"]),
    ("SECO / CONSERVA", AMBER, ["10 · Deshidratado", "11 · Molienda + tamizado", "12 · Despulpado / jugo"]),
    ("EMPAQUE", NAVY, ["13 · Envasado (fresco/salmuera/polvo)", "14 · Etiquetado", "15 · Almacén"]),
]
y = Inches(1.45); rh = Inches(1.06)
for ph, c, steps in phases:
    rounded(s, Inches(0.78), y, Inches(2.2), rh - Inches(0.12), c)
    txt(s, Inches(0.78), y, Inches(2.2), rh - Inches(0.12), [Pr(ph, 12.5, WHITE, True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, ls=0.95)
    cx = Inches(3.15); cyy = y + Inches(0.05)
    for stp in steps:
        w = Inches(0.16 + 0.088 * len(stp))
        if cx + w > Inches(12.55):
            cx = Inches(3.15); cyy += Inches(0.42)
        chip(s, cx, cyy, stp, c, h=Inches(0.34), fs=10)
        cx = cx + w + Inches(0.1)
    y += rh
txt(s, Inches(0.78), Inches(6.72), Inches(11.8), Inches(0.3),
    [Pr("Ruta de la TUNA (fruto): recepción → lavado → desespinado (cepillos en seco) → calibrado → empaque; o jugo (despulpado → pasteurizado).", 9.5, GRAY, True)])


# ===========================================================================
# 4. COSECHA
# ===========================================================================
s = slide()
header(s, "Etapa 1 · Cosecha", "Herramientas de cosecha manual", GREEN)
machine_card(s, Inches(1.4), GREEN,
    "Corte manual (cuchillo curvo, navaja, tijeras)", "Nacional",
    "Cortar el cladodio tierno (15-25 cm) sin dañar la penca madre; cortar la tuna (no jalar).",
    ["Partes: hoja de acero inoxidable o al carbono, mango de madera/plástico, resortes",
     "Se recomienda cortar dejando la base para no desgarrar",
     "Costo muy bajo (ferreterías, agroservicios, Mercado Libre)"],
    "Bajo (ferreterías)", "Muy fácil (cuchillería nacional)")
machine_card(s, Inches(4.05), GREEN,
    "EPP y acarreo (guantes anti-espina, pinzas, cajas)", "Nacional",
    "Proteger manos de espinas y gloquidios (ahuates) y transportar el producto cosechado.",
    ["Partes: guante de piel/carnaza o kevlar, pinzas de acero/plástico, cajas HDPE",
     "El guante se ensambla en México; solo la fibra kevlar suele importarse",
     "Cajas y pinzas: proveedores agrícolas nacionales"],
    "Bajo", "Fácil (piel/plástico nacional)")


# ===========================================================================
# 5. DESESPINADO DE NOPAL
# ===========================================================================
s = slide()
header(s, "Etapa 2 · Limpieza", "Desespinado de nopal-verdura", CYAN)
machine_card(s, Inches(1.4), CYAN,
    "Desespinadora 'Nopalli' (Nopalea)", "México · Nuevo León",
    "Retira espinas de caras y bordes en un solo paso, sin lastimar el nopalito (eficiencia 80-95%).",
    ["Partes: motor 1 HP 110 V, rodillos de tracción, porta-cuchillas ajustable (tensión/ángulo/profundidad)",
     "Estructura inox 304 + plástico grado alimenticio; ~200 kg/h; hasta 60 pencas/min",
     "El fabricante declara 'refacciones convencionales, fáciles de conseguir'"],
    "~$15,000-100,000 MXN", "Fabricación 100% nacional")
machine_card(s, Inches(4.05), CYAN,
    "Línea DESINOX (4 equipos) + patente MX WO2005011941", "México · Jalisco",
    "Lavadora + desespinadora + desorilladora + rayadora en inox 304; la patente MX es plano de referencia.",
    ["Partes (patente): rodillos auto-ajustables por resorte, cuchillas de doble filo intercambiables, paro de emergencia",
     "Capacidad de la patente: 10-600 kg/h; módulos apilables para ambas caras",
     "Referente nacional de 'línea completa' de nopal-verdura"],
    "Por cotización", "Referente de réplica nacional")


# ===========================================================================
# 6. DESESPINADO DE TUNA
# ===========================================================================
s = slide()
header(s, "Etapa 2 · Limpieza", "Desespinado de tuna (fruto)", CYAN)
machine_card(s, Inches(1.4), CYAN,
    "Desespinado por cepillos/rodillos en seco (prototipo IPN-UPIITA)", "México · Edo. de México",
    "El fruto rueda entre cepillos/rodillos que arrancan gloquidios; el secado facilita el desprendimiento.",
    ["Etapas: dosificación → rodillos de desespinado → secado → recolector de espinas → clasificador por tamaño",
     "Componentes: cilindro/tambor inox, cerdas de nylon, motorreductor, banda + rodillo inclinado",
     "Arquitectura de referencia desarrollada por el IPN (mecatrónica)"],
    "Prototipo académico", "Fabricable (inox + cerdas + motor)")
machine_card(s, Inches(4.05), CYAN,
    "Benchmark a NO importar: Agrilux (España) / Somca (Chile)", "Internacional",
    "Líneas comerciales de desespinado en seco por rodillos; referencia de costo que justifica la réplica.",
    ["Agrilux: 300 / 600 / 1,000 / 2,000 kg/h; acero de alta resistencia (opción inox)",
     "Precio Agrilux 300 kg/h: desde €12,270 (~US$13,000) → costo de importar a evitar",
     "También Henan Saloni (China) fabrica desespinadora de cactus/nopal"],
    "desde €12,270 (importado)", "Reemplazable por diseño nacional")


# ===========================================================================
# 7. LAVADO
# ===========================================================================
s = slide()
header(s, "Etapa 2 · Limpieza", "Lavado y desinfección", CYAN)
machine_card(s, Inches(1.4), CYAN,
    "Lavadora por inmersión Tecnodac TSH", "México",
    "Lavado y desinfección por inmersión con turbulencia (agua clorada ~100-200 ppm).",
    ["Partes: tina y canastilla inox 304, motobomba inox, boquilla inyectora, volteo neumático, timer",
     "Datasheet: 25-150 kg por carga; ciclo 1-8 min; 220 V; requiere aire 6-7 kg/cm²",
     "Todos los componentes son de mercado nacional"],
    "Por cotización", "Fabricable (taller inox)")
machine_card(s, Inches(4.05), CYAN,
    "Lavado por burbujas y aspersión (Solifood, Citrus)", "México",
    "Burbujas + aspersores de alta presión para producto delicado (nopal cortado); recircula el agua.",
    ["Partes: tina inox 304/316 soldadura sanitaria, bomba inox, aspersores, variador de frecuencia",
     "Componentes nacionales: bomba centrífuga inox, boquillas Spraying Systems, VFD Delta",
     "Tecnologías: inmersión (robustos), aspersión (delicados), burbujeo (suciedad incrustada)"],
    "Por cotización", "Fabricación nacional")


# ===========================================================================
# 8. CORTE
# ===========================================================================
s = slide()
header(s, "Etapa 3 · Transformación", "Corte y picado", BLUE)
machine_card(s, Inches(1.4), BLUE,
    "Picadora de nopal INALSA PN-27 / PN-54", "México · Nuevo León",
    "Picado de nopal en volumen (alto tonelaje / industrial-forraje).",
    ["Potencia: motor eléctrico 7.5 HP, o gasolina 13 HP, o toma de fuerza (TDF) de tractor",
     "Datasheet: PN-27 = 7 t/h (75×80×60 cm); PN-54 = 14 t/h (1.5×1.44×1.3 m)",
     "Construcción metálica robusta de fabricación nacional"],
    "Por cotización", "Fabricación 100% nacional")
machine_card(s, Inches(4.05), BLUE,
    "Cortadora en cubos/juliana (benchmark Nilma) — réplica CNC", "Italia (referencia)",
    "Corte continuo y uniforme en cubos, tiras o juliana para nopal fresco de mesa.",
    ["Partes a replicar: discos y rejillas de corte inox intercambiables, cámara inox, motorreductor, tolva",
     "Es el ÚNICO punto que exige maquinado de precisión (discos/rejillas)",
     "Existen talleres CNC en México (p. ej. Adek, Monterrey) para fabricar las cuchillas"],
    "Referencia (a replicar)", "Media-alta (CNC nacional)")


# ===========================================================================
# 9. ESCALDADO + BANDAS
# ===========================================================================
s = slide()
header(s, "Etapa 3 · Transformación", "Escaldado (quita baba) y transporte", BLUE)
machine_card(s, Inches(1.4), BLUE,
    "Escaldadora (blanching) y enfriador", "Nacional (a medida)",
    "Agua hirviendo 3-5 min inactiva enzimas, fija el color y reduce el mucílago (baba); luego choque en frío.",
    ["Partes: tina inox 304 + resistencias eléctricas o quemador de gas + transportador de malla/tornillo + control de temperatura",
     "Enfriador: tina/túnel de agua fría (hielo o chiller) con recirculación",
     "100% fabricable por cualquier taller de acero inoxidable mexicano"],
    "A medida (taller inox)", "Fabricación nacional")
machine_card(s, Inches(4.05), BLUE,
    "Bandas y mesas de selección inox (MATEX, Ferromat, Tecnibandas, ASLAN)", "México",
    "Transportar el producto entre etapas y seleccionar/descartar en mesa.",
    ["Partes: banda modular de plástico o malla inox, motorreductor (~0.75 kW), estructura AISI-304",
     "Bandas modulares Intralox/Ammeraal disponibles vía distribuidores mexicanos (RYASA, SIMSA)",
     "Rubro muy maduro localmente: fabricación fácil"],
    "Por metro (cotización)", "Muy fácil (nacional)")


# ===========================================================================
# 10. DESHIDRATADO
# ===========================================================================
s = slide()
header(s, "Etapa 4 · Seco / conserva", "Deshidratado", AMBER)
machine_card(s, Inches(1.4), AMBER,
    "Deshidratador de charolas (MT Maquinaria, VINCON)", "México · Puebla",
    "Secar tiras/rebanadas por aire caliente forzado a 55-65 °C hasta ~5-10% de humedad (base para harina).",
    ["Partes: gabinete + charolas inox, quemador de gas L.P. de hierro colado o resistencias 1.5-2 kW, ventilador, termostato",
     "Datasheet: VINCON 35-350 kg/h de entrada; gabinetes de 16-20 charolas ~20 kg/lote",
     "Interior inox sin tornillos/remaches (higiene)"],
    "Gabinete $4-12k; industrial ~$100k MXN", "Fabricación nacional")
machine_card(s, Inches(4.05), AMBER,
    "Deshidratador solar (≤60 °C) y de túnel", "México (UNAM / IPN)",
    "Secado de bajo costo operativo (solar) o continuo por carros (túnel) para volumen.",
    ["Solar: colector, cámara con charolas, chimenea o ventilador fotovoltaico (máx. 60 °C para no dañar el producto)",
     "Túnel: carros de charolas + banco de resistencias/quemador + múltiples ventiladores",
     "Fabricable con materiales locales; el control PLC/HMI es lo de mayor costo"],
    "Solar: bajo costo", "Fabricación nacional")


# ===========================================================================
# 11. MOLIENDA
# ===========================================================================
s = slide()
header(s, "Etapa 4 · Seco / conserva", "Molienda y tamizado (harina de nopal)", AMBER)
machine_card(s, Inches(1.4), AMBER,
    "Molino de martillos VEYCO (serie MMV / MM)", "México",
    "Moler nopal seco a harina/polvo por impacto y corte, con criba que define la finura.",
    ["Partes: rotor con 16-120 martillos (inox o acero al carbón), cribas 0.8-12 mm, cámara, tolva, motor 3-30 HP",
     "Datasheet: MMV06 = 50-300 kg/h (3-5 HP) … MMV40 = 4,000-5,000 kg/h (30-40 HP)",
     "Harina de nopal se vende a ~$70-85 MXN/kg (valor agregado)"],
    "Por cotización (según HP)", "Fabricación 100% nacional")
machine_card(s, Inches(4.05), AMBER,
    "Tamizado / cernido (TPI México, Russell Finex)", "México",
    "Clasificar la harina por tamaño y retirar la fibra gruesa tras la molienda.",
    ["Partes: criba circular vibratoria, mallas de acero inox intercambiables, motovibrador, resortes",
     "Cernidores de sobremesa desde ~$2,000-8,000 MXN; industriales por cotización",
     "El motovibrador de calidad puede importarse; el resto es nacional"],
    "$2-8k (sobremesa)", "Fácil (nacional)")


# ===========================================================================
# 12. DESPULPADO / JUGO
# ===========================================================================
s = slide()
header(s, "Etapa 4 · Seco / conserva", "Despulpado, jugo y valor agregado", AMBER)
machine_card(s, Inches(1.4), AMBER,
    "Despulpadora / extractor (Micron, Equinox, FoxSteel)", "México · CDMX / Edo. Méx.",
    "Separar pulpa/jugo de la cáscara y la semilla (tuna) o triturar nopal a pulpa.",
    ["Partes: tolva inox, tambor/criba perforada, paletas o tornillo sinfín/cepillos, motorreductor, chasis inox T-304",
     "Datasheet: 30-400 kg/h (líneas industriales hasta 2,000 kg/h)",
     "Componentes de fabricación nacional"],
    "Amplio (cotización)", "Fabricación nacional")
machine_card(s, Inches(4.05), AMBER,
    "Productos de valor agregado (tuna)", "Proceso",
    "Jugo/néctar, puré/concentrado (67-68 °Brix), mermelada, colorante (betalaínas) y aceite de semilla.",
    ["Equipos: despulpadora, refinador, marmita con camisa de vapor, pasteurizador, prensa de aceite",
     "Benchmark de líneas: IBC (China, 1-300 t/día), Enoitalia (Italia, ~1,500 kg/h), Romiter",
     "Marmitas y tanques inox: fabricación nacional; pasteurizador de placas: compra especializada"],
    "Modular (por etapa)", "Parcial (marmitas nacional)")


# ===========================================================================
# 13. EMPAQUE
# ===========================================================================
s = slide()
header(s, "Etapa 5 · Empaque", "Envasado, sellado y etiquetado", NAVY)
machine_card(s, Inches(1.4), NAVY,
    "Dosificadora de polvo (auger) Equitek + selladora al vacío", "México · Nuevo León",
    "Dosificar la harina de nopal (10 g-5 kg) y sellar bolsas al vacío para alargar la vida útil.",
    ["Partes: tolva inox + agitador, tornillo dosificador (auger), servo/celda de carga, PLC/HMI, barra selladora, bomba de vacío",
     "Datasheet Equitek DSL: 10 g-5 kg, 1-50 pzas/min, 220 V, aire 90 psi",
     "Estructura y tolva nacionales; servo/celda/bomba de vacío suelen importarse"],
    "Selladora $1.5-30k MXN", "Parcial (control importado)")
machine_card(s, Inches(4.05), NAVY,
    "Empaque de nopal fresco (MAP) y en salmuera", "México",
    "Fresco cortado con atmósfera modificada, o nopalitos en salmuera en frasco/bolsa pasteurizados.",
    ["MAP: film barrera + atmósfera O₂ 2-5% / CO₂ 3-10% a 5 °C (inhibe oscurecimiento)",
     "Salmuera: marmita, llenadora, tapadora/engargoladora, autoclave o baño 15 min",
     "Marmitas y mesas inox nacionales; el film/equipo MAP suele importarse"],
    "Modular (cotización)", "Fabricable (film importado)")


# ===========================================================================
# 14. FOCO — COMPONENTES PARA RÉPLICA MEXICANA
# ===========================================================================
s = slide()
header(s, "Foco · Réplica mexicana", "Componentes y dónde comprarlos en México", GREEN)
rows = [
    ("Componente", "Proveedor / distribuidor en México", "Marcas", True),
    ("Motores y motorreductores", "RORISA, Siemens Motores MX, SEW-Eurodrive MX, Energía Controlada", "WEG, Siemens, Baldor", False),
    ("Acero inoxidable 304/316", "Aceros y Metales Cuautitlán, Integrinox (Mty), Metales de México", "lámina / tubo / PTR", False),
    ("Bandas modulares y transportadoras", "RYASA, SIMSA, Bandas Matuz, MATEX, Ferromat", "Intralox, Ammeraal", False),
    ("Rodamientos, chumaceras, cadenas", "RYASA, NSK Rodamientos Mexicana, Grupo SURA", "SKF, NSK", False),
    ("Cepillos y rodillos a medida", "Cepillos Regios, Cepillo Técnico, Cepillos BHM (Apodaca)", "nylon / crin / alambre", False),
    ("Variadores (VFD) y PLC", "IAS Automation (Delta), Industrias GSL, SiemSupply", "Delta, Siemens, Allen-Bradley", False),
    ("Boquillas, bombas inox, resistencias", "Spraying Systems MX, Barmesa, MISUMI MX", "aspersión / centrífugas", False),
    ("Cuchillas y discos de corte inox", "Adek (Monterrey), Cuchillas México", "inox 420 / 440", False),
]
tx, ty, tw = Inches(0.78), Inches(1.4), Inches(11.78)
colw = [Inches(3.4), Inches(5.85), Inches(2.53)]
hh = Inches(0.46); rh2 = Inches(0.5)
rounded(s, tx, ty, tw, hh, NAVY)
cx = tx
for j in range(3):
    txt(s, cx + Inches(0.14), ty, colw[j] - Inches(0.2), hh, [Pr(rows[0][j], 11.5, WHITE, True)], anchor=MSO_ANCHOR.MIDDLE)
    cx += colw[j]
for i, row in enumerate(rows[1:]):
    yy = ty + hh + Emu(int(rh2 * i))
    rect(s, tx, yy, tw, rh2, WHITE if i % 2 == 0 else LIGHT)
    cx = tx
    for j in range(3):
        bold = (j == 0); col = NAVY if j == 0 else GRAY
        txt(s, cx + Inches(0.14), yy, colw[j] - Inches(0.2), rh2, [Pr(row[j], 11 if j == 0 else 10.5, col, bold)],
            anchor=MSO_ANCHOR.MIDDLE)
        cx += colw[j]
txt(s, tx, Inches(6.55), tw, Inches(0.32),
    [[("Talleres inox para ensamble a medida:  ", 10.5, GREEN, True, False),
      ("Servinox y DESINOX (Jalisco) · INALSA e Inox Proyecta (N.L.) · Dinorte (Coahuila) · Mekanex · VEYCO · Equitek.",
       10.5, GRAY, False, False)]])


# ===========================================================================
# 15. FOCO — FABRICAR VS COMPRAR
# ===========================================================================
s = slide()
header(s, "Foco · Réplica mexicana", "¿Qué fabricar en México y qué comprar?", GREEN)
rounded(s, Inches(0.78), Inches(1.45), Inches(5.85), Inches(5.1), LIGHT)
rect(s, Inches(0.78), Inches(1.45), Inches(5.85), Inches(0.6), GREEN)
txt(s, Inches(1.0), Inches(1.45), Inches(5.5), Inches(0.6), [Pr("FABRICAR / CONSEGUIR FÁCIL EN MÉXICO", 12.5, WHITE, True)], anchor=MSO_ANCHOR.MIDDLE)
fab = ["Estructura y cámaras en acero inox 304", "Charolas, martillos, cribas, tolvas, tornillos auger",
       "Rodillos, cuchillas y porta-cuchillas", "Resistencias eléctricas y quemadores de gas L.P.",
       "Ventiladores/turbinas y ductos", "Motores y motorreductores (WEG, Siemens)",
       "Tinas, marmitas y mesas de selección", "Bandas transportadoras y estructuras",
       "Tableros eléctricos básicos y timers"]
for i, t in enumerate(fab):
    yy = Inches(2.25) + i * Inches(0.46)
    rounded(s, Inches(1.02), yy + Inches(0.04), Inches(0.14), Inches(0.14), GREEN)
    txt(s, Inches(1.3), yy, Inches(5.2), Inches(0.4), [Pr(t, 11, INK, False)], anchor=MSO_ANCHOR.MIDDLE)
rounded(s, Inches(6.72), Inches(1.45), Inches(5.85), Inches(5.1), LIGHT)
rect(s, Inches(6.72), Inches(1.45), Inches(5.85), Inches(0.6), AMBER)
txt(s, Inches(6.94), Inches(1.45), Inches(5.5), Inches(0.6), [Pr("COMPRAR A MARCA / IMPORTAR (CONTROL FINO)", 12.5, WHITE, True)], anchor=MSO_ANCHOR.MIDDLE)
imp = ["PLC + HMI de gama y controladores PID de precisión", "Variadores de frecuencia (VFD) de marca",
       "Servomotores con encoder", "Celdas de carga para dosificación por peso",
       "Bombas de vacío para empacadora", "Motovibradores de calidad (tamizadora)",
       "Discos/rejillas de corte de precisión (CNC)", "Film y equipo de atmósfera modificada (MAP)"]
for i, t in enumerate(imp):
    yy = Inches(2.25) + i * Inches(0.46)
    rounded(s, Inches(6.96), yy + Inches(0.04), Inches(0.14), Inches(0.14), AMBER)
    txt(s, Inches(7.24), yy, Inches(5.2), Inches(0.4), [Pr(t, 11, INK, False)], anchor=MSO_ANCHOR.MIDDLE)


# ===========================================================================
# 16. NACIONAL VS IMPORTADO
# ===========================================================================
s = slide()
header(s, "Foco · Réplica mexicana", "Fabricar en México vs. importar", GREEN)
comp = [
    ("Criterio", "Fabricar en México", "Importar", True),
    ("Costo inicial", "Menor: material + mano de obra + componentes de catálogo", "Mayor: precio + flete + aduana + margen", False),
    ("Refacciones", "Estándar (WEG, SKF, Delta) en stock; días", "Piezas propietarias; semanas/meses", False),
    ("Mantenimiento", "Cualquier taller local lo atiende", "Técnico especializado / del fabricante", False),
    ("Tiempo de entrega", "Semanas (taller local)", "Meses (fabricación + envío + aduana)", False),
    ("Adaptación al nopal", "Total (ajuste de rodillos/cepillos/cuchillas)", "Diseño genérico, difícil de modificar", False),
    ("Servicio / idioma", "Español, mismo huso, garantía local", "Barrera de idioma y distancia", False),
]
tx, ty, tw = Inches(0.78), Inches(1.5), Inches(11.78)
colw = [Inches(2.75), Inches(4.9), Inches(4.13)]
hh = Inches(0.52); rh2 = Inches(0.66)
rounded(s, tx, ty, tw, hh, NAVY)
cx = tx
heads = [("Criterio", GRAY), ("Fabricar en México", GREEN), ("Importar", AMBER)]
for j in range(3):
    txt(s, cx + Inches(0.14), ty, colw[j] - Inches(0.2), hh, [Pr(comp[0][j], 12, WHITE, True)], anchor=MSO_ANCHOR.MIDDLE)
    cx += colw[j]
for i, row in enumerate(comp[1:]):
    yy = ty + hh + Emu(int(rh2 * i))
    rect(s, tx, yy, tw, rh2, WHITE if i % 2 == 0 else LIGHT)
    # marca la columna "México" con fondo verde muy suave
    cx = tx
    for j in range(3):
        bold = (j == 0)
        col = NAVY if j == 0 else (GREEN if j == 1 else GRAY)
        txt(s, cx + Inches(0.14), yy, colw[j] - Inches(0.24), rh2, [Pr(row[j], 11 if j == 0 else 10.5, col, bold)],
            anchor=MSO_ANCHOR.MIDDLE, ls=1.02)
        cx += colw[j]


# ===========================================================================
# 17. COSTOS
# ===========================================================================
s = slide()
header(s, "Economía", "Costos de referencia (MXN)", BLUE)
costs = [
    ("Herramientas de cosecha manual", "Bajo", GREEN, "Ferreterías / Mercado Libre"),
    ("Desespinadora de nopal (nacional)", "$15,000 - 100,000", CYAN, "Ref. $120k por 500 kg/h (Michoacán)"),
    ("Deshidratador de charolas", "$4,000 - 12,000 (semi)", AMBER, "Industrial ~$100,000"),
    ("Selladora al vacío", "$1,500 - 30,000", NAVY, "Doméstica a comercial de cámara"),
    ("Molino de martillos / despulpadora", "Por cotización", AMBER, "Según HP y capacidad (VEYCO)"),
    ("Nave / planta (obra, por m²)", "$12,000 - 25,000 / m²", BLUE, "Proceso seco vs. húmedo (Grupo CCEIC)"),
    ("Benchmark IMPORTADO a evitar", "desde €12,270 (~US$13k)", GRAY, "Agrilux 300 kg/h; líneas grandes por cotización"),
]
y = Inches(1.45)
for i, (label, price, c, note) in enumerate(costs):
    yy = y + i * Inches(0.72)
    rounded(s, Inches(0.78), yy, Inches(11.78), Inches(0.62), LIGHT)
    rect(s, Inches(0.78), yy, Inches(0.12), Inches(0.62), c)
    txt(s, Inches(1.05), yy, Inches(5.0), Inches(0.62), [Pr(label, 12.5, NAVY, True)], anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(6.1), yy, Inches(3.25), Inches(0.62), [Pr(price, 12.5, c, True)], anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(9.4), yy, Inches(3.05), Inches(0.62), [Pr(note, 9.8, GRAY, False)], anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(0.78), Inches(6.68), Inches(11.8), Inches(0.34),
    [Pr("Los fabricantes rara vez publican precio de lista; los rangos vienen de portales (QuiMinet/MercadoLibre) y deben confirmarse por cotización.", 9.5, GRAY, True)])


# ===========================================================================
# 18. NORMAS Y APOYOS
# ===========================================================================
s = slide()
header(s, "Marco normativo", "Normas y aliados para fabricar en México", BLUE)
items = [
    ("NOM-251-SSA1-2009", GREEN, "Prácticas de higiene para el proceso de alimentos (obligatoria): superficies de contacto en acero grado alimenticio, diseño que permita limpieza (sin tornillos/remaches expuestos), mantenimiento del equipo."),
    ("Buenas Prácticas de Manufactura (BPM)", BLUE, "Programas voluntarios de SENASICA (órgano de SADER) para establecimientos que procesan alimentos; útiles para certificación y exportación."),
    ("Materiales grado alimenticio", CYAN, "Acero inoxidable 304 (contacto) y 316 (medios ácidos/salinos: jugo, salmuera); grasa grado alimenticio en rodamientos."),
    ("Aliados de I+D (academia)", AMBER, "IPN-UPIITA (desespinadora de tuna), UNAM (deshidratado solar) y UACh (jugo estabilizado) desarrollan tecnología nacional; posibles socios para diseño de la réplica."),
]
y = Inches(1.55)
for i, (t, c, d) in enumerate(items):
    yy = y + i * Inches(1.28)
    rounded(s, Inches(0.78), yy, Inches(11.78), Inches(1.12), LIGHT)
    rect(s, Inches(0.78), yy, Inches(0.12), Inches(1.12), c)
    txt(s, Inches(1.1), yy + Inches(0.16), Inches(11.2), Inches(0.4), [Pr(t, 15, NAVY, True)])
    txt(s, Inches(1.1), yy + Inches(0.56), Inches(11.2), Inches(0.5), [Pr(d, 11.5, GRAY, False)], ls=1.08)


# ===========================================================================
# 19. RUTA DE ADOPCIÓN
# ===========================================================================
s = slide()
header(s, "Plan", "Ruta recomendada para la réplica", BLUE)
txt(s, Inches(0.78), Inches(1.4), Inches(11.8), Inches(0.5),
    [Pr("De lo simple a lo industrial: primero el núcleo de bajo costo, después la transformación según el producto elegido.", 13, GRAY, False)])
phases = [
    ("FASE 1", "Diseño + BOM", GREEN, ["Definir producto: fresco, salmuera, harina o jugo", "Lista de materiales (BOM) con proveedores MX", "Elegir taller inox local"]),
    ("FASE 2", "Núcleo de limpieza", CYAN, ["Desespinadora + lavadora nacional", "Mesa de selección y banda", "Cumplir higiene NOM-251"]),
    ("FASE 3", "Transformación", BLUE, ["Corte + escaldado (fresco/salmuera)", "o Deshidratado + molino (harina)", "o Despulpadora (jugo)"]),
    ("FASE 4", "Empaque + escala", AMBER, ["Dosificado / sellado / etiquetado", "Control fino (PLC, celda, vacío)", "Certificar BPM y escalar"]),
]
cw, gap, x0, y0 = Inches(2.85), Inches(0.18), Inches(0.78), Inches(2.15)
for i, (ph, title, c, its) in enumerate(phases):
    x = x0 + i * (cw + gap)
    rounded(s, x, y0, cw, Inches(4.15), LIGHT)
    rect(s, x, y0, cw, Inches(0.95), c)
    txt(s, x + Inches(0.22), y0 + Inches(0.12), cw - Inches(0.4), Inches(0.35), [Pr(ph, 11.5, WHITE, True)])
    txt(s, x + Inches(0.22), y0 + Inches(0.45), cw - Inches(0.4), Inches(0.45), [Pr(title, 16, WHITE, True)])
    for k, it in enumerate(its):
        iy = y0 + Inches(1.2) + k * Inches(0.9)
        rounded(s, x + Inches(0.22), iy + Inches(0.04), Inches(0.34), Inches(0.34), c)
        txt(s, x + Inches(0.22), iy + Inches(0.04), Inches(0.34), Inches(0.34), [Pr(str(k + 1), 13, WHITE, True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        txt(s, x + Inches(0.66), iy, cw - Inches(0.85), Inches(0.82), [Pr(it, 11, INK, False)], anchor=MSO_ANCHOR.MIDDLE, ls=1.05)
for i in range(3):
    ax = x0 + (i + 1) * cw + i * gap + Inches(0.01)
    txt(s, ax, y0 + Inches(1.7), gap, Inches(0.5), [Pr("›", 22, GRAY, True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# ===========================================================================
# 20. FUENTES
# ===========================================================================
s = slide()
header(s, "Referencias", "Fabricantes y fuentes consultadas")
txt(s, Inches(0.78), Inches(1.4), Inches(5.9), Inches(0.3), [Pr("FABRICANTES MEXICANOS", 12, GREEN, True)])
mx = ["Nopalea / Nopalli (N.L.) — desespinadora", "DESINOX (Jalisco) — línea de 4 equipos",
      "INALSA (N.L.) — picadora PN-27/54", "VEYCO — molinos de martillos",
      "MT Maquinaria (Puebla) — deshidratador", "Tecnodac / Solifood / Citrus — lavado",
      "Equitek (N.L.) — envasadoras", "Servinox / Dinorte / Mekanex — talleres inox"]
for i, d in enumerate(mx):
    yy = Inches(1.8) + i * Inches(0.48)
    rounded(s, Inches(0.78), yy + Inches(0.04), Inches(0.14), Inches(0.14), GREEN)
    txt(s, Inches(1.02), yy, Inches(5.6), Inches(0.4), [Pr(d, 11, INK, False)], anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(6.9), Inches(1.4), Inches(5.7), Inches(0.3), [Pr("REFERENCIAS TÉCNICAS Y PORTALES", 12, BLUE, True)])
rf = ["Patente MX WO2005011941A1 (desespinadora)", "IPN-UPIITA / UNAM Ecotec (deshidratado, tuna)",
      "FAO — Utilización agroindustrial del nopal", "INIFAP — manual de nopal verdura",
      "NOM-251-SSA1-2009 (DOF) — higiene", "QuiMinet / Cosmos / Mercado Libre (precios)",
      "Benchmark: Agrilux (ES), IBC/Romiter (China), Enoitalia (IT)", "SIAP — producción nacional de nopal y tuna"]
for i, d in enumerate(rf):
    yy = Inches(1.8) + i * Inches(0.48)
    rounded(s, Inches(6.9), yy + Inches(0.04), Inches(0.14), Inches(0.14), BLUE)
    txt(s, Inches(7.14), yy, Inches(5.45), Inches(0.4), [Pr(d, 11, INK, False)], anchor=MSO_ANCHOR.MIDDLE)
rounded(s, Inches(0.78), Inches(6.5), Inches(11.78), Inches(0.5), LIGHT)
txt(s, Inches(1.05), Inches(6.5), Inches(11.3), Inches(0.5),
    [[("Nota: ", 10.5, BLUE, True, False),
      ("los precios de portales varían por capacidad y plaza; confirmar por cotización directa con cada fabricante.", 10.5, GRAY, False, False)]],
    anchor=MSO_ANCHOR.MIDDLE)


# ===========================================================================
# 21. CONCLUSIONES
# ===========================================================================
s = slide()
header(s, "Conclusiones", "Hallazgos clave", GREEN)
finds = [
    ("Oportunidad de sustitución", "México es el productor #1 pero importa la maquinaria más completa: hay espacio para fabricar nacional."),
    ("La réplica es viable", "El 80-90% de cada máquina son componentes de catálogo + estructura de acero inox de taller local."),
    ("Ya hay industria nacional", "Nopalea, DESINOX, INALSA, VEYCO, Tecnodac y Equitek prueban que se puede fabricar en México."),
    ("Solo importar lo fino", "Corte de precisión (CNC) y control (PLC/servo/celdas/vacío) ameritan compra especializada."),
    ("Ventaja competitiva", "Refacciones inmediatas, adaptación a la variedad local del nopal y menor costo total de propiedad."),
]
y = Inches(1.55)
for i, (t, d) in enumerate(finds):
    yy = y + i * Inches(1.02)
    rounded(s, Inches(0.78), yy, Inches(0.5), Inches(0.5), GREEN)
    txt(s, Inches(0.78), yy, Inches(0.5), Inches(0.5), [Pr(str(i + 1), 18, WHITE, True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, Inches(1.45), yy - Inches(0.02), Inches(11.1), Inches(0.4), [Pr(t, 15, NAVY, True)])
    txt(s, Inches(1.45), yy + Inches(0.36), Inches(11.1), Inches(0.6), [Pr(d, 12, GRAY, False)], ls=1.08)


# ===========================================================================
# 22. CIERRE
# ===========================================================================
s = slide()
rect(s, 0, 0, EMU_W, EMU_H, NAVY)
rect(s, 0, 0, EMU_W, Inches(0.12), GREEN)
rect(s, 0, Inches(0.12), EMU_W, Inches(0.06), MXRED)
rounded(s, Inches(5.85), Inches(2.35), Inches(0.72), Inches(0.72), BLUE)
txt(s, Inches(5.85), Inches(2.35), Inches(0.72), Inches(0.72), [Pr("H", 34, WHITE, True)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, 0, Inches(3.35), EMU_W, Inches(0.7), [Pr("Hecho en México", 38, WHITE, True)], align=PP_ALIGN.CENTER)
txt(s, 0, Inches(4.25), EMU_W, Inches(0.6),
    [Pr("Del cladodio al empaque: maquinaria de nopal replicable con talento y componentes nacionales.", 15, RGBColor(0xC6, 0xD3, 0xE6), False)], align=PP_ALIGN.CENTER)
txt(s, 0, Inches(6.7), EMU_W, Inches(0.4),
    [[("Howy", 12, CYAN, True, False), ("   ·   Investigación técnica   ·   Julio 2026", 12, RGBColor(0x9F, 0xB2, 0xCD), False, False)]], align=PP_ALIGN.CENTER)


out = "/home/user/Work/presentaciones/Howy_Maquinaria_Nopal_2026.pptx"
prs.save(out)
print("OK ->", out, "| slides:", len(prs.slides._sldIdLst))
