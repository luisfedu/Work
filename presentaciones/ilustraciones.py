# -*- coding: utf-8 -*-
"""
Ilustraciones esquemáticas (SVG -> PNG) estilo Howy para la maquinaria de
aguacate y nopal. Ejecutar para generar assets/img/*.png
"""
import os, io, math
import cairosvg

NAVY="#0E213A"; BLUE="#2D6CDF"; CYAN="#18C2D6"; AMBER="#F5A623"
GREEN="#2EA84F"; GRAY="#5B6674"; LIGHT="#F4F7FB"; LINE="#C7D0DB"
WHITE="#FFFFFF"; INK="#1A2432"; STEEL="#B9C4D2"; STEELD="#8C99A9"
BROWN="#5A3B22"; RED="#C1443A"
W,H=760,470

def svg(body,bg=LIGHT):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect x="0" y="0" width="{W}" height="{H}" rx="18" fill="{bg}"/>{body}</svg>')
def title(t,color=NAVY):
    return (f'<text x="{W/2}" y="44" font-family="Arial" font-size="30" font-weight="700" '
            f'fill="{color}" text-anchor="middle">{t}</text>')
def label(x,y,t,color=GRAY,anchor="middle",size=19):
    return (f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" font-weight="600" '
            f'fill="{color}" text-anchor="{anchor}">{t}</text>')
def leader(x1,y1,x2,y2,color=STEELD):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2"/>'
            f'<circle cx="{x2}" cy="{y2}" r="4" fill="{color}"/>')
def arrow(x1,y1,x2,y2,color=BLUE,w=6):
    ang=math.atan2(y2-y1,x2-x1); a=11
    x3=x2-a*math.cos(ang-0.5); y3=y2-a*math.sin(ang-0.5)
    x4=x2-a*math.cos(ang+0.5); y4=y2-a*math.sin(ang+0.5)
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<polygon points="{x2},{y2} {x3},{y3} {x4},{y4}" fill="{color}"/>')
def rr(x,y,w,h,fill,rx=8,stroke="none",sw=0):
    st=f'stroke="{stroke}" stroke-width="{sw}"' if stroke!="none" else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {st}/>'
def ci(cx,cy,r,fill,stroke="none",sw=0):
    st=f'stroke="{stroke}" stroke-width="{sw}"' if stroke!="none" else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" {st}/>'
def poly(pts,fill,stroke="none",sw=0):
    st=f'stroke="{stroke}" stroke-width="{sw}"' if stroke!="none" else ""
    p=" ".join(f"{a},{b}" for a,b in pts)
    return f'<polygon points="{p}" fill="{fill}" {st}/>'
def line(x1,y1,x2,y2,color=STEELD,w=3,cap="butt"):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}" stroke-linecap="{cap}"/>'

def motor(x,y,color=STEELD):
    s=rr(x,y,70,52,color,rx=8)
    for i in range(5):
        s+=line(x+8+i*13,y+4,x+8+i*13,y+48,NAVY,2)
    s+=rr(x+70,y+16,14,20,STEEL,rx=3)
    return s
def fan(cx,cy,r,color=BLUE):
    s=ci(cx,cy,r,WHITE,stroke=color,sw=5)
    for k in range(5):
        a=k*72*math.pi/180
        s+=line(cx,cy,cx+(r-6)*math.cos(a),cy+(r-6)*math.sin(a),color,6,"round")
    return s+ci(cx,cy,6,color)
def brush_roller(cx,cy,r,color=AMBER):
    s=""
    for k in range(24):
        a=k*15*math.pi/180
        s+=line(cx+r*math.cos(a),cy+r*math.sin(a),cx+(r+13)*math.cos(a),cy+(r+13)*math.sin(a),color,3)
    return s+ci(cx,cy,r,STEEL,stroke=STEELD,sw=3)+ci(cx,cy,5,STEELD)
def roller(cx,cy,r,color=STEEL):
    return ci(cx,cy,r,color,stroke=STEELD,sw=3)+ci(cx,cy,4,STEELD)
def belt(x,y,w,rollers=5,color=NAVY):
    s=rr(x,y,w,26,color,rx=13); step=w/(rollers-1)
    for i in range(rollers):
        s+=ci(x+i*step,y+13,9,STEEL,stroke=NAVY,sw=2)
    return s
def avocado(cx,cy,s=1.0,color=GREEN,stem=True):
    st=rr(cx-3*s,cy-40*s,6*s,12*s,BROWN,rx=3) if stem else ""
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{22*s}" ry="{30*s}" fill="{color}"/>'+st
def nopal(cx,cy,s=1.0):
    s2=f'<ellipse cx="{cx}" cy="{cy}" rx="{34*s}" ry="{46*s}" fill="{GREEN}"/>'
    for (dx,dy) in [(-14,-18),(12,-22),(-16,6),(14,4),(0,20),(-2,-2)]:
        s2+=ci(cx+dx*s,cy+dy*s,3.2*s,"#1C6B33")
    return s2
def pear(cx,cy,s=1.0,color=RED):
    s2=f'<ellipse cx="{cx}" cy="{cy}" rx="{22*s}" ry="{30*s}" fill="{color}"/>'
    for (dx,dy) in [(-8,-12),(6,-16),(-10,4),(8,2),(0,14)]:
        s2+=line(cx+dx*s,cy+dy*s,cx+dx*s+5,cy+dy*s-5,"#F2E7A6",2)
    return s2
def hopper(x,y,w,h,color=STEEL):
    return poly([(x,y),(x+w,y),(x+w-w*0.28,y+h),(x+w*0.28,y+h)],color,STEELD,3)
def tank(x,y,w,h,color=STEEL,water=CYAN):
    s=rr(x,y,w,h,color,rx=12,stroke=STEELD,sw=3)
    s+=rr(x+8,y+h*0.45,w-16,h*0.5,water,rx=8)
    return s+rr(x+8,y+h*0.45,w-16,10,WHITE,rx=5)
def spray(x,y,color=CYAN):
    s=rr(x-6,y-14,12,14,STEELD,rx=3)
    for dx in (-10,0,10):
        s+=line(x,y,x+dx,y+26,color,3,"round")+ci(x+dx,y+30,3,color)
    return s
def camera(cx,cy,color=NAVY):
    return rr(cx-26,cy-20,52,34,color,rx=6)+ci(cx,cy-3,11,CYAN,stroke=WHITE,sw=3)+rr(cx-34,cy+16,68,8,AMBER,rx=4)
def cabinet(x,y,w,h,color=STEEL,trays=5):
    s=rr(x,y,w,h,color,rx=10,stroke=STEELD,sw=3)
    for i in range(trays):
        s+=rr(x+10,y+18+i*(h-30)/trays,w-20,10,LIGHT,rx=3,stroke=STEELD,sw=1)
    return s
def robot_arm(bx,by,color=AMBER):
    s=rr(bx-22,by,44,22,NAVY,rx=6)
    s+=line(bx,by,bx-6,by-70,color,14,"round")+line(bx-6,by-70,bx+70,by-96,color,14,"round")
    s+=ci(bx,by,9,NAVY)+ci(bx-6,by-70,9,NAVY)+rr(bx+64,by-104,26,20,STEELD,rx=4)
    return s
def box(x,y,w,h,color=AMBER):
    return rr(x,y,w,h,color,rx=5,stroke="#B9791A",sw=2)+line(x+w/2,y,x+w/2,y+h,"#B9791A",2)
def blade(x,y,color=STEELD):
    return poly([(x,y),(x+26,y-8),(x+26,y+8)],color,NAVY,2)
def sun(cx,cy,r=26,color=AMBER):
    s=ci(cx,cy,r,color)
    for k in range(8):
        a=k*45*math.pi/180
        s+=line(cx+(r+4)*math.cos(a),cy+(r+4)*math.sin(a),cx+(r+16)*math.cos(a),cy+(r+16)*math.sin(a),color,4,"round")
    return s
def flame(cx,cy,color=AMBER):
    return f'<path d="M{cx} {cy} q-18 -20 0 -46 q6 16 12 6 q10 20 -12 40 z" fill="{color}"/>'
def snow(cx,cy,r=16,color=CYAN):
    s=""
    for k in range(6):
        a=k*60*math.pi/180
        s+=line(cx,cy,cx+r*math.cos(a),cy+r*math.sin(a),color,3,"round")
    return s
def person(cx,cy,color=NAVY):
    return ci(cx,cy-30,12,color)+rr(cx-11,cy-16,22,34,color,rx=8)
def wheel(cx,cy,r=22):
    return ci(cx,cy,r,NAVY)+ci(cx,cy,r*0.45,STEEL)
def bin_crate(x,y,w,h,color=STEEL):
    s=rr(x,y,w,h,color,rx=6,stroke=STEELD,sw=3)
    for i in range(1,5):
        s+=line(x+i*w/5,y+6,x+i*w/5,y+h-6,STEELD,3)
    s+=rr(x+8,y+h,14,10,STEELD,rx=2)+rr(x+w-22,y+h,14,10,STEELD,rx=2)
    return s
def gcyl(x,y,w,h,color=BLUE,txt="N₂"):
    s=rr(x,y,w,h,color,rx=12)+rr(x+w*0.3,y-12,w*0.4,14,STEELD,rx=4)
    return s+label(x+w/2,y+h/2+7,txt,WHITE,size=22)

# ---------------------------------------------------------------------------
# ESCENAS
# ---------------------------------------------------------------------------
S={}

# ---- AGUACATE ----
def _b(*p): return "".join(p)

S["av_tijeras"]=svg(title("Tijeras de cosecha")+_b(
    # tijera
    line(300,250,420,180,STEELD,10,"round"),line(300,250,420,320,STEELD,10,"round"),
    line(300,250,235,285,NAVY,12,"round"),line(300,250,235,215,NAVY,12,"round"),
    ci(300,250,8,AMBER),
    avocado(520,250,1.1),
    label(430,150,"Corte limpio del pedúnculo")+leader(430,160,420,182),
    label(235,330,"Mangos",anchor="middle")))

S["av_pertiga"]=svg(title("Pértiga telescópica + bolsa")+_b(
    f'<ellipse cx="560" cy="150" rx="150" ry="80" fill="{GREEN}" opacity="0.9"/>',
    avocado(560,170,0.8),
    line(140,420,470,180,STEELD,12,"round"),
    rr(455,150,26,40,NAVY,rx=5),
    poly([(445,190),(495,190),(505,250),(435,250)],AMBER,"#B9791A",2),
    label(150,300,"Pértiga 1.7–3.7 m",anchor="start")+leader(255,300,300,300),
    label(470,290,"Cabezal + bolsa")+leader(470,275,470,252)))

S["av_bins"]=svg(title("Bins plásticos ventilados")+_b(
    bin_crate(230,180,300,180),
    avocado(290,170,0.7),avocado(360,165,0.7),avocado(430,170,0.7),avocado(470,172,0.7),
    label(600,270,"Paredes")+label(600,296,"ventiladas")+leader(560,285,505,285),
    label(380,420,"Base para montacargas")))

S["av_telehandler"]=svg(title("Telehandler (manejo de bins)")+_b(
    rr(150,250,190,90,AMBER,rx=12),wheel(200,360),wheel(300,360),
    rr(230,200,70,55,NAVY,rx=8),
    line(300,270,540,210,STEELD,16,"round"),
    line(540,210,540,300,NAVY,8),line(540,300,590,300,NAVY,8),
    bin_crate(540,240,90,60),
    label(200,180,"Pluma telescópica")+leader(300,190,420,240)))

S["av_profruit"]=svg(title("Volteador de bins (en seco)")+_b(
    belt(360,300,340,5),
    f'<g transform="rotate(-32 300 250)">'+bin_crate(230,190,150,110)+'</g>',
    avocado(360,250,0.6),avocado(400,258,0.6),avocado(450,252,0.6),
    line(230,340,230,250,STEELD,10),
    label(250,150,"Bin inclinado")+leader(300,160,290,205),
    label(560,360,"Cinta clasificadora")))

S["av_volteo_suave"]=svg(title("Volteo suave / destacker")+_b(
    bin_crate(150,300,120,80),bin_crate(150,235,120,60),
    f'<g transform="rotate(-20 400 250)">'+bin_crate(340,220,120,90)+'</g>',
    belt(470,330,220,4),avocado(520,290,0.6),avocado(560,296,0.6),
    label(210,420,"Bins vacíos")+label(560,420,"Vaciado gradual")))

S["av_lavado"]=svg(title("Lavado y cepillado")+_b(
    belt(120,320,520,6),
    brush_roller(210,270,32),brush_roller(300,270,32),brush_roller(390,270,32),brush_roller(480,270,32),
    spray(300,170),spray(390,170),
    avocado(150,270,0.7),avocado(560,270,0.7),
    label(300,440,"Cepillos de nylon")+leader(300,420,300,308),
    label(590,160,"Aspersión")+leader(560,168,395,168)))

S["av_secado"]=svg(title("Secado (air knife) + encerado")+_b(
    belt(120,320,520,6),avocado(200,270,0.7),avocado(420,270,0.7),
    rr(180,150,70,20,STEELD,rx=6),
    line(190,172,175,230,CYAN,4,"round"),line(215,172,215,235,CYAN,4,"round"),line(240,172,255,230,CYAN,4,"round"),
    spray(430,160,AMBER),
    fan(560,190,30,BLUE),
    label(215,120,"Cuchilla de aire")+leader(215,130,215,150),
    label(430,120,"Encerado")+leader(430,130,430,150)))

S["av_copas"]=svg(title("Calibrado por peso (copa + celda)")+_b(
    belt(90,160,580,6),
    _b(*[_b(f'<path d="M{cx-30} 220 q30 42 60 0 z" fill="{STEEL}" stroke="{STEELD}" stroke-width="3"/>',avocado(cx,212,0.62)) for cx in (200,340,480)]),
    rr(300,300,80,42,NAVY,rx=6),label(340,327,"celda",WHITE,size=18),
    arrow(340,258,340,298,BLUE,5),
    label(200,150,"Copa basculante")+label(340,382,"Celda de carga (pesa cada fruto)")))

S["av_rodillos"]=svg(title("Rodillos giratorios + inspección")+_b(
    rr(120,300,520,20,NAVY,rx=10),
    roller(220,275,26),roller(300,275,26),roller(380,275,26),roller(460,275,26),
    avocado(340,255,0.7),
    f'<path d="M312 250 a30 14 0 0 1 56 0" fill="none" stroke="{BLUE}" stroke-width="4"/>',
    arrow(366,246,372,252,BLUE,4),
    camera(340,150),
    label(560,150,"Cámara + LED")+leader(520,158,372,158),
    label(240,430,"Giro 360° del fruto")+leader(300,412,330,270)))

S["av_vision"]=svg(title("Selección óptica (visión + IA)")+_b(
    belt(120,320,520,6),
    avocado(210,270,0.7,GREEN),avocado(320,270,0.7,"#4FB06A"),avocado(430,270,0.7,GREEN),avocado(520,270,0.7,"#2C8A46"),
    camera(340,160),
    line(316,192,250,250,CYAN,2),line(364,192,430,250,CYAN,2),
    label(560,150,"Color, tamaño, defectos")+leader(430,175,368,178)))

S["av_nir"]=svg(title("Calidad interna NIR (materia seca)")+_b(
    avocado(300,250,1.5),
    arrow(120,250,270,250,AMBER,6),arrow(330,250,470,250,AMBER,6),
    f'<path d="M500 300 q15 -50 30 0 q15 50 30 0 q15 -50 30 0" fill="none" stroke="{BLUE}" stroke-width="4"/>',
    label(150,220,"NIR",AMBER,anchor="start",size=22),
    label(300,400,"Mide % de materia seca = madurez")))

S["av_empaque"]=svg(title("Empaque en bandeja")+_b(
    rr(180,220,400,180,STEEL,rx=12,stroke=STEELD,sw=3),
    _b(*[_b(*[avocado(230+c*90,270+r*70,0.6) for c in range(4)]) for r in range(2)]),
    label(380,430,"Bandeja / caja por peso o conteo")))

S["av_etiquetado"]=svg(title("Etiquetado PLU")+_b(
    belt(120,330,520,6),avocado(250,280,0.85),avocado(470,280,0.85),
    ci(360,180,42,WHITE,stroke=STEELD,sw=4),ci(360,180,10,STEELD),
    rr(345,225,30,30,AMBER,rx=4),
    arrow(360,258,360,285,AMBER,5),
    rr(468,268,26,16,WHITE,stroke=BLUE,sw=2),label(481,281,"PLU",BLUE,size=11),
    label(430,150,"Rollo de etiquetas")+leader(402,165,378,178)))

S["av_embalaje"]=svg(title("Encajonado / malla")+_b(
    box(160,250,180,120),
    _b(*[avocado(200+c*45,290+r*40,0.5) for r in range(2) for c in range(3)]),
    arrow(370,300,440,300,BLUE,6),
    box(470,250,150,120,STEEL),
    label(250,410,"Case packer")+label(545,410,"Caja lista")))

S["av_paletizado"]=svg(title("Paletizado robótico")+_b(
    robot_arm(230,340),
    box(500,360,130,50),box(500,305,130,50),box(520,255,90,45),
    rr(490,410,150,14,NAVY,rx=4),
    label(320,220,"Brazo 6 ejes")+leader(300,235,285,270),label(560,445,"Tarima")))

S["av_preenfriado"]=svg(title("Preenfriamiento por aire forzado")+_b(
    box(220,220,150,180,STEEL),box(400,220,150,180,STEEL),
    fan(150,310,34,BLUE),fan(620,310,34,BLUE),
    arrow(184,310,215,310,CYAN,5),arrow(586,310,556,310,CYAN,5),
    snow(385,150,18),
    label(385,430,"Aire frío a través de los pallets")))

S["av_frio"]=svg(title("Cámara de refrigeración")+_b(
    rr(200,150,360,250,STEEL,rx=14,stroke=STEELD,sw=4),
    rr(330,250,100,150,NAVY,rx=6),
    snow(280,210,20),snow(480,210,20),
    rr(560,200,44,120,WHITE,stroke=BLUE,sw=4),ci(582,320,20,BLUE),rr(578,220,8,100,BLUE,rx=4),
    label(600,180,"~4–7 °C",anchor="middle")))

S["av_ca"]=svg(title("Atmósfera controlada (N₂ PSA)")+_b(
    gcyl(180,190,90,190,BLUE,"N₂"),gcyl(300,190,90,190,STEELD,"CO₂"),
    arrow(400,240,500,240,GREEN,6),
    box(520,190,160,190,STEEL),
    label(600,240,"O₂ ↓",GREEN,size=22),
    label(225,410,"Genera N₂")+label(560,410,"Contenedor CA")))

S["av_etileno"]=svg(title("Generador de etileno")+_b(
    rr(230,220,150,140,STEEL,rx=12,stroke=STEELD,sw=3),
    ci(305,290,34,AMBER),label(305,298,"C₂H₄",WHITE,size=20),
    _b(*[ci(430+i*22,250+((i%2)*20),6,GREEN) for i in range(5)]),
    label(305,400,"0.5–2 L etileno / 24 h")))

S["av_madroom"]=svg(title("Cuarto de maduración")+_b(
    rr(180,150,400,250,STEEL,rx=14,stroke=STEELD,sw=4),
    box(230,300,90,60),box(340,300,90,60),box(450,300,90,60),
    fan(250,210,30,BLUE),
    ci(470,200,30,AMBER),label(470,208,"C₂H₄",WHITE,size=15),
    label(380,430,"15–20 °C · 90–95% HR")))

S["av_munckhof"]=svg(title("Plataforma de cosecha")+_b(
    f'<ellipse cx="600" cy="150" rx="140" ry="75" fill="{GREEN}" opacity="0.9"/>',avocado(600,160,0.6),
    rr(150,300,240,70,AMBER,rx=12),wheel(200,375),wheel(340,375),
    rr(180,180,120,120,NAVY,rx=8),person(240,250,WHITE),
    line(300,250,470,210,STEEL,10,"round"),
    label(255,150,"Plataformas + cintas")+leader(285,160,300,240)))

S["av_revo"]=svg(title("Plataforma autopropulsada 4WD")+_b(
    rr(180,270,380,80,AMBER,rx=12),wheel(230,355),wheel(360,355),wheel(500,355),
    rr(320,170,120,100,NAVY,rx=8),person(380,230,WHITE),
    belt(150,250,120,3),belt(470,250,120,3),
    bin_crate(340,300,80,45),
    label(370,150,"Cintas laterales + central")+leader(370,160,380,190)))

S["av_preenf2"]=svg(title("Preenfriadores (unidades)")+_b(
    box(250,230,120,150,STEEL),box(400,230,120,150,STEEL),
    fan(180,305,30,BLUE),fan(590,305,30,BLUE),fan(385,140,30,BLUE),
    arrow(212,305,246,305,CYAN,5),arrow(558,305,524,305,CYAN,5),
    snow(120,150,16),
    label(385,420,"Aire forzado (TRJ · MACS · chinos)")))

# ---- NOPAL ----
S["no_corte"]=svg(title("Corte manual del nopal")+_b(
    nopal(300,250,1.5),
    f'<path d="M470 180 q-40 40 -120 90" fill="none" stroke="{STEELD}" stroke-width="12" stroke-linecap="round"/>',
    line(470,180,510,150,NAVY,12,"round"),
    label(430,140,"Cuchillo curvo")+leader(430,150,455,168)))

S["no_epp"]=svg(title("EPP y acarreo")+_b(
    # guante
    _b(*[rr(190+i*18,150,14,60,CYAN,rx=6) for i in range(4)]),rr(180,205,90,70,CYAN,rx=12),
    # pinzas
    line(360,180,420,300,STEELD,8,"round"),line(400,180,340,300,STEELD,8,"round"),
    bin_crate(500,250,140,110),
    label(225,300,"Guante anti-espina")+label(380,330,"Pinzas")+label(570,390,"Cajas")))

S["no_desespina"]=svg(title("Desespinadora de nopal")+_b(
    rr(120,290,520,20,NAVY,rx=10),
    roller(240,268,26),roller(340,268,26),roller(440,268,26),
    blade(277,268),blade(377,268),
    nopal(165,258,0.8),nopal(560,262,0.8),
    motor(120,205),
    label(360,205,"Cuchillas rasuran la espina")+leader(360,218,377,262),
    label(240,435,"Rodillos de tracción")+leader(240,418,240,294)))

S["no_desinox"]=svg(title("Línea DESINOX (4 equipos)")+_b(
    *[_b(rr(120+i*150,250,110,110,STEEL,rx=10,stroke=STEELD,sw=3),
         label(175+i*150,315,n,NAVY,size=17)) for i,n in enumerate(["Lava","Desesp","Desor","Raya"])],
    *[arrow(230+i*150,305,270+i*150,305,BLUE,5) for i in range(3)],
    label(380,410,"Línea completa en acero inoxidable 304")))

S["no_tuna_brush"]=svg(title("Desespinado de tuna (cepillos)")+_b(
    ci(360,250,110,STEEL,stroke=STEELD,sw=4),
    *[line(360+95*math.cos(k*20*math.pi/180),250+95*math.sin(k*20*math.pi/180),
           360+120*math.cos(k*20*math.pi/180),250+120*math.sin(k*20*math.pi/180),AMBER,3) for k in range(18)],
    ci(360,250,12,NAVY),pear(360,250,1.0),
    label(560,200,"Tambor con cepillos")+leader(500,210,455,230),
    label(360,410,"El fruto rueda y suelta gloquidios")))

S["no_agrilux"]=svg(title("Benchmark: desespinado en seco")+_b(
    rr(180,200,320,150,STEEL,rx=12,stroke=STEELD,sw=3),
    *[brush_roller(240+i*90,270,26) for i in range(3)],
    pear(150,270,0.8),pear(530,270,0.8),
    rr(300,150,80,20,STEELD,rx=6),line(340,170,340,200,STEELD,4),
    label(340,130,"Aspiración de espinas"),
    label(360,400,"300–2000 kg/h (referencia a replicar)")))

S["no_lav_inmersion"]=svg(title("Lavadora por inmersión")+_b(
    tank(210,180,340,190),
    rr(280,210,200,110,STEEL,rx=8,stroke=STEELD,sw=2),
    nopal(330,265,0.55),nopal(400,270,0.55),nopal(450,262,0.55),
    ci(250,340,7,WHITE),ci(300,350,6,WHITE),ci(470,345,7,WHITE),
    motor(560,270),
    label(380,410,"Tina + canastilla inox 304")))

S["no_lav_burbujas"]=svg(title("Lavado por burbujas y aspersión")+_b(
    tank(210,190,360,180),
    spray(300,160),spray(400,160),spray(480,160),
    *[ci(260+i*40,330+((i%2)*12),6,WHITE) for i in range(8)],
    nopal(340,280,0.55),nopal(430,285,0.55),
    label(390,410,"Aspersores + burbujeo (recircula agua)")))

S["no_picadora"]=svg(title("Picadora / cortadora de nopal")+_b(
    hopper(280,110,180,70),nopal(370,120,0.55),
    rr(250,180,240,120,STEEL,rx=12,stroke=STEELD,sw=3),
    ci(370,240,42,LIGHT,stroke=STEELD,sw=2),
    *[line(370,240,370+38*math.cos(k*60*math.pi/180),240+38*math.sin(k*60*math.pi/180),NAVY,4) for k in range(6)],
    motor(150,220),
    *[rr(320+i*20,320,10,26,GREEN,rx=2) for i in range(6)],
    label(560,240,"Cuchillas")+leader(520,240,412,240),
    label(370,410,"Cubos / tiras")))

S["no_cortadora_cubos"]=svg(title("Corte en cubos / juliana")+_b(
    rr(230,170,300,150,STEEL,rx=12,stroke=STEELD,sw=3),
    *[line(250+i*40,180,250+i*40,310,STEELD,3) for i in range(8)],
    *[line(240,190+i*30,520,190+i*30,STEELD,3) for i in range(5)],
    *[rr(560,190+i*40,26,26,GREEN,rx=3) for i in range(3)],
    label(380,150,"Rejilla de discos y cuchillas inox"),
    label(573,340,"Cubos")))

S["no_escaldado"]=svg(title("Escaldado (quita la baba)")+_b(
    tank(230,190,300,170,STEEL,"#E88"),
    *[line(280+i*45,175,280+i*45,150,WHITE,4,"round") for i in range(5)],
    flame(300,400),flame(360,400),flame(420,400),flame(460,400),
    nopal(330,270,0.5),nopal(410,275,0.5),
    label(600,220,"Vapor")+label(380,150,"Agua 90–100 °C"),
    label(380,435,"Inactiva enzimas · reduce mucílago")))

S["no_bandas"]=svg(title("Banda y mesa de selección")+_b(
    belt(120,300,520,6),
    nopal(200,255,0.55),nopal(300,258,0.55),nopal(410,255,0.55),nopal(520,258,0.55),
    person(200,230),person(520,230),
    label(360,410,"Transporte y selección (inox 304)")))

S["no_deshid_charolas"]=svg(title("Deshidratador de charolas")+_b(
    cabinet(250,110,280,290,trays=5),
    fan(190,180,32,BLUE),arrow(222,180,246,180,BLUE,5),
    rr(260,410,260,16,AMBER,rx=6),
    label(160,250,"Aire caliente")+leader(170,235,190,205),
    label(600,235,"Charolas")+leader(560,235,520,235),
    label(380,455,"55–65 °C")))

S["no_deshid_solar"]=svg(title("Deshidratador solar (≤60 °C)")+_b(
    sun(150,140,32),
    f'<g transform="rotate(-20 300 250)">'+rr(200,230,220,40,BLUE,rx=8)+'</g>',
    cabinet(430,190,180,180,trays=4),
    arrow(250,150,300,210,AMBER,4),
    label(300,320,"Colector solar")+label(520,400,"Cámara de charolas")))

S["no_molino"]=svg(title("Molino de martillos (harina)")+_b(
    ci(370,260,115,STEEL,stroke=STEELD,sw=4),
    *[_b(line(370,260,370+105*math.cos(k*45*math.pi/180),260+105*math.sin(k*45*math.pi/180),NAVY,6),
         rr(370+100*math.cos(k*45*math.pi/180)-10,260+100*math.sin(k*45*math.pi/180)-10,20,20,AMBER,rx=4)) for k in range(8)],
    ci(370,260,14,NAVY),hopper(310,90,120,55),
    f'<path d="M270 370 h200" stroke="{STEELD}" stroke-width="4" stroke-dasharray="8 6"/>',
    label(575,260,"Martillos")+leader(540,260,455,230),
    label(370,405,"Criba (finura de harina)")))

S["no_tamizado"]=svg(title("Tamizado / cernido")+_b(
    f'<g transform="rotate(-12 380 260)">'+rr(230,240,300,26,STEELD,rx=8)+
    "".join(line(240+i*20,246,240+i*20,260,WHITE,1) for i in range(14))+'</g>',
    *[ci(300+i*30,330+((i%2)*8),4,AMBER) for i in range(8)],
    arrow(250,200,250,235,BLUE,5),
    label(380,410,"Criba vibratoria (mallas inox)")))

S["no_despulpadora"]=svg(title("Despulpadora / extractor")+_b(
    hopper(260,110,160,60),pear(340,120,0.5),
    rr(230,170,300,120,STEEL,rx=12,stroke=STEELD,sw=3),
    ci(320,230,40,LIGHT,stroke=STEELD,sw=2),
    *[ci(320+16*math.cos(k*45*math.pi/180),230+16*math.sin(k*45*math.pi/180),2.5,STEELD) for k in range(8)],
    line(360,230,500,230,STEELD,10),
    motor(150,205),
    line(400,290,400,340,CYAN,10),ci(400,350,10,CYAN),
    label(560,230,"Criba + sinfín")+label(400,400,"Jugo / pulpa",CYAN)))

S["no_valor"]=svg(title("Valor agregado (tuna)")+_b(
    rr(230,190,80,180,RED,rx=14),rr(255,160,30,30,STEELD,rx=4),label(270,300,"jugo",WHITE),
    rr(360,230,90,140,"#E7B84B",rx=12,stroke="#B9791A",sw=2),rr(375,205,60,26,STEELD,rx=4),label(405,320,"mermelada",INK,size=15),
    rr(500,220,80,150,"#B03A6E",rx=12),label(540,310,"colorante",WHITE,size=15),
    label(400,415,"Jugo · mermelada · colorante · aceite")))

S["no_dosificadora"]=svg(title("Dosificadora de polvo (auger)")+_b(
    hopper(300,100,160,70),
    rr(350,170,60,120,STEEL,rx=8,stroke=STEELD,sw=3),
    f'<path d="M362 185 q18 12 0 24 q-18 12 0 24 q18 12 0 24 q-18 12 0 24" fill="none" stroke="{NAVY}" stroke-width="6"/>',
    poly([(360,300),(400,300),(392,380),(368,380)],AMBER,"#B9791A",2),
    label(380,120,"Tornillo dosificador",WHITE if False else GRAY)+leader(430,175,400,210),
    label(380,420,"Envasa 10 g – 5 kg")))

S["no_map"]=svg(title("Empaque: MAP y salmuera")+_b(
    rr(200,200,180,150,LIGHT,rx=12,stroke=STEELD,sw=3),nopal(290,275,0.55),
    label(290,190,"O₂ 2–5% · CO₂ 3–10%",BLUE,size=15),
    rr(470,180,110,180,CYAN,rx=14,stroke=STEELD,sw=3),rr(495,150,60,30,STEELD,rx=4),
    nopal(525,250,0.5),
    label(290,375,"Fresco (MAP)")+label(525,385,"Salmuera")))

# ---------------------------------------------------------------------------
def render_all(outdir):
    os.makedirs(outdir,exist_ok=True)
    for k,v in S.items():
        cairosvg.svg2png(bytestring=v.encode(),write_to=os.path.join(outdir,k+".png"),
                         output_width=W*2,output_height=H*2)
    return list(S.keys())

if __name__=="__main__":
    here=os.path.dirname(os.path.abspath(__file__))
    ks=render_all(os.path.join(here,"assets","img"))
    print("rendered",len(ks),"images:",", ".join(ks))
