"""Genera el PDF con el guión del video de presentación (7 personas, ~17:30 min).

Ejecutar:  python generar_guion.py
Produce:   Guion_video_El_Gran_Escape.pdf

Si quieren retocar textos o tiempos, editen las estructuras SECCIONES /
PORTADA de abajo y vuelvan a ejecutar.
"""
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

AZUL = colors.HexColor("#1f4e79")
CELESTE = colors.HexColor("#5aaaff")
ROJO = colors.HexColor("#c0392b")
VERDE = colors.HexColor("#1e8449")
GRIS_FONDO = colors.HexColor("#f2f4f8")
GRIS_LINEA = colors.HexColor("#c8cdd6")

base = getSampleStyleSheet()
S = {
    "titulo": ParagraphStyle("titulo", parent=base["Title"], fontSize=26,
                             textColor=AZUL, spaceAfter=6),
    "subtitulo": ParagraphStyle("subtitulo", parent=base["Normal"], fontSize=13,
                                alignment=1, textColor=colors.HexColor("#444"),
                                spaceAfter=18),
    "h_persona": ParagraphStyle("h_persona", parent=base["Heading1"], fontSize=16,
                                textColor=colors.white, backColor=AZUL,
                                borderPadding=(6, 8, 6, 8), spaceBefore=10,
                                spaceAfter=2, leading=20),
    "h_bloque": ParagraphStyle("h_bloque", parent=base["Heading2"], fontSize=12,
                               textColor=AZUL, spaceBefore=10, spaceAfter=4),
    "normal": ParagraphStyle("normal", parent=base["Normal"], fontSize=10.5,
                             leading=14.5, spaceAfter=6),
    "guion": ParagraphStyle("guion", parent=base["Normal"], fontSize=10.5,
                            leading=15, spaceAfter=8, leftIndent=10,
                            borderPadding=(5, 8, 5, 8), backColor=GRIS_FONDO),
    "item": ParagraphStyle("item", parent=base["Normal"], fontSize=10.5,
                           leading=14, leftIndent=22, bulletIndent=8,
                           spaceAfter=3),
    "qa_p": ParagraphStyle("qa_p", parent=base["Normal"], fontSize=10,
                           leading=13.5, leftIndent=10, spaceAfter=2,
                           textColor=ROJO),
    "qa_r": ParagraphStyle("qa_r", parent=base["Normal"], fontSize=10,
                           leading=13.5, leftIndent=24, spaceAfter=7),
    "nota": ParagraphStyle("nota", parent=base["Normal"], fontSize=9.5,
                           leading=13, textColor=colors.HexColor("#555"),
                           spaceAfter=4),
}


def code(t):
    return f'<font face="Courier" size="9.5" color="#1f4e79">{t}</font>'


def b(t):
    return f"<b>{t}</b>"


# ====================================================================== #
# CONTENIDO
# ====================================================================== #

RESUMEN = [
    ("Quién", "Tema", "Tiempo", "Qué muestra"),
    ("Persona 1", "Estructura principal + demo", "2:30",
     "main.py, el juego y README.md"),
    ("Persona 2", "Laberinto procedural", "2:30",
     "juego/laberinto.py + demo ASCII en consola"),
    ("Persona 3", "Motor: física y radar", "2:30",
     "juego/entidad.py, camara.py, render.py"),
    ("Persona 4", "Reglas y bots", "2:30",
     "juego/partida.py, bots.py, tests_fase2.py"),
    ("Persona 5", "PostgreSQL y ranking", "2:30",
     "db/esquema.sql, conexion.py, repositorio.py"),
    ("Persona 6", "Multijugador y lobby", "2:30",
     "db/red.py, juego/partida_multi.py + demo"),
    ("Persona 7", "Arbitraje y pruebas", "2:30",
     "db/repositorio.py, tests_fase4.py"),
]

SECCIONES = [
    # ------------------------------------------------------------------ #
    dict(
        encabezado="PERSONA 1 - Estructura principal y demo del juego (2:30)",
        mision="Abrir el video: mostrar la estructura del código en main.py y una demo rápida del juego.",
        pantalla=[
            "main.py: la definición de las constantes de estado (línea 28) y el loop principal (while corriendo).",
            "Tener el juego ya abierto (python main.py).",
            "Pantalla de nombre, menú, partida rápida de escapista, pantalla fin y ranking (tecla T).",
            "README.md mostrando el plan de fases.",
        ],
        guion=[
            "Hola, somos el grupo [nombres] y presentamos El Gran Escape. Un "
            "juego multijugador asimétrico en Python, Pygame y PostgreSQL. "
            "Tres escapistas buscan salidas y dos cazadores los persiguen.",
            "[MOSTRÁ: main.py, línea 28 y el while corriendo.] A nivel código, "
            "el flujo funciona con una máquina de estados. Dependiendo de si "
            "estamos en MENU, LOBBY o JUGANDO, el loop principal procesa los eventos "
            "del teclado de manera distinta y le pide al módulo render que dibuje la pantalla correspondiente.",
            "[MOSTRÁ: el juego.] Desde el menú podés jugar solo o ir al "
            "multijugador por base de datos, que luego explicaremos. Juguemos "
            "una partida rápida.",
            "[MOSTRÁ: jugá 30 segs de escapista.] El laberinto se genera "
            "solo. La cámara sigue al jugador. Abajo está el radar: los cazadores "
            "son más rápidos, pero con el radar podemos anticiparlos.",
            "[MOSTRÁ: dejate atrapar o escapá, pantalla de fin, luego T.] "
            "Al final el resultado se guarda y vemos el ranking global.",
            "[MOSTRÁ: README.md.] Desarrollamos esto en cuatro fases, y así nos "
            "repartimos la explicación. [Persona 2] arranca con el laberinto.",
        ],
        preguntas=[
            ("¿Por qué un laberinto tan grande no es injugable?",
             "La cámara centrada y el minimapa evitan que sea frustrante, lo fuimos iterando."),
        ],
    ),
    # ------------------------------------------------------------------ #
    dict(
        encabezado="PERSONA 2 - El laberinto procedural (2:30)",
        mision="Explicar generación, braiding y el concepto de la seed.",
        pantalla=[
            "juego/laberinto.py: _excavar(), _abrir_atajos() y __init__.",
            "Consola: python -m juego.laberinto",
        ],
        guion=[
            "[MOSTRÁ: juego/laberinto.py, _excavar().] Usamos Recursive Backtracking "
            "para generar el mapa. Como la recursión nativa en Python rompería por límite "
            "de profundidad en mapas tan grandes, lo programamos iterativo usando una pila explícita.",
            "[MOSTRÁ: _abrir_atajos().] Un laberinto 'perfecto' tiene una sola ruta entre "
            "dos puntos. Para un juego de persecución eso es fatal porque te bloquean fácil. "
            "Aplicamos 'braiding': abrimos un 20% de los callejones sin salida para crear múltiples rutas.",
            "[MOSTRÁ: __init__.] Todo el azar sale de una semilla. Misma seed, mismo laberinto. "
            "En el multijugador no mandamos por red el mapa, solo la seed y cada cliente lo recrea.",
            "[MOSTRÁ: python -m juego.laberinto.] Este módulo incluye una demo ASCII que "
            "verifica con un BFS que las 3 salidas sean siempre alcanzables. Sigue [Persona 3].",
        ],
        preguntas=[
            ("¿Qué pasa si la seed es la misma?",
             "El nivel es idéntico. Se puede probar lanzando el juego con --seed 1234."),
        ],
    ),
    # ------------------------------------------------------------------ #
    dict(
        encabezado="PERSONA 3 - Motor: física, cámara y radar (2:30)",
        mision="Explicar colisiones por ejes, recorte de cámara y el radar.",
        pantalla=[
            "juego/entidad.py: mover().",
            "juego/camara.py: a_pantalla().",
            "juego/render.py: dibujar_laberinto() y dibujar_minimapa().",
        ],
        guion=[
            "[MOSTRÁ: juego/entidad.py.] Tanto humanos como bots instancian la misma clase Entidad "
            "y física. Ningún bot puede hacer trampa ni traspasar paredes.",
            "[MOSTRÁ: mover().] Resolvemos colisiones eje por eje (X primero, luego Y). "
            "Así al ir en diagonal contra un muro, te deslizás suavemente. Y normalizamos "
            "el vector para no movernos más rápido en las diagonales.",
            "[MOSTRÁ: camara.py y render.py.] El laberinto tiene más de 10.000 tiles. La cámara "
            "sigue al jugador y dibujamos sólo lo visible. Así garantizamos 60 FPS estables.",
            "[MOSTRÁ: dibujar_minimapa().] Para el balance, el cazador es un 9% más rápido, "
            "pero el escapista tiene ventaja de radar: las salidas siempre se ven, y los enemigos "
            "sólo si están cerca. Le toca a [Persona 4].",
        ],
        preguntas=[
            ("¿Por qué no usar sprites en vez de círculos?",
             "Priorizamos las lógicas y mecánicas. Todo está desacoplado en render.py para cambiarse fácil."),
        ],
    ),
    # ------------------------------------------------------------------ #
    dict(
        encabezado="PERSONA 4 - Reglas del juego e IA de los bots (2:30)",
        mision="Explicar bucle lógico separado de Pygame y la decisión de IA de los bots.",
        pantalla=[
            "juego/partida.py: actualizar().",
            "juego/bots.py: CerebroCazador y CerebroEscapista.",
            "Consola: python tests_fase2.py.",
        ],
        guion=[
            "[MOSTRÁ: juego/partida.py.] Las reglas están 100% separadas de Pygame. "
            "Cada ciclo actualiza posiciones y chequea capturas o escapes.",
            "[MOSTRÁ: juego/bots.py.] Los cazadores patrullan al azar, y persiguen con BFS "
            "sólo si tienen línea de visión directa. El escapista fue un reto: al principio "
            "usaban el camino óptimo y ganaban siempre en segundos. Los empeoramos: ahora "
            "exploran y si una salida entra a su radar, recién ahí van a ella.",
            "[MOSTRÁ: tests_fase2.py.] Como la lógica no depende de gráficos, hicimos este script "
            "que corre 5 partidas de bots contra bots en segundos, para comprobar el balanceo final. "
            "Paso a [Persona 5].",
        ],
        preguntas=[
            ("¿Por qué usan BFS y no A* para el camino?",
             "En un grid sin pesos, BFS te da la ruta más corta y es súper eficiente. A* no era necesario."),
        ],
    ),
    # ------------------------------------------------------------------ #
    dict(
        encabezado="PERSONA 5 - PostgreSQL: esquema, guardado y ranking (2:30)",
        mision="Explicar tablas UNLOGGED, creación automática y tolerancia a fallos.",
        pantalla=[
            "db/esquema.sql: posiciones UNLOGGED y vistas.",
            "db/conexion.py y repositorio.py.",
            "Juego: pantalla de ranking.",
        ],
        guion=[
            "[MOSTRÁ: db/esquema.sql.] Nuestro modelo tiene 4 tablas. La tabla clave es "
            "posiciones, que es UNLOGGED. Se usa para el multijugador porque son datos "
            "efímeros de alta rotación. Al ser unlogged, no escriben en el diario de transacciones "
            "(WAL), haciendo las escrituras ultra rápidas.",
            "[MOSTRÁ: db/conexion.py.] La base se autoconfigura al conectarse. Si hay error de red, "
            "lanza DBNoDisponible, el juego lo atrapa y sigue. La caída de la base no congela la partida.",
            "[MOSTRÁ: db/repositorio.py y juego ranking.] Guardamos a los 5 participantes marcando "
            "quién es bot. Las vistas de SQL los filtran y el ranking usa MIN(tiempo) y GROUP BY "
            "para mostrar sólo el récord de cada persona y evitar monopolios. Sigue [Persona 6].",
        ],
        preguntas=[
            ("¿Qué es UNLOGGED?", "Omite logs de transacción (WAL), ganando mucho rendimiento a costa de persistencia ante fallos críticos."),
        ],
    ),
    # ------------------------------------------------------------------ #
    dict(
        encabezado="PERSONA 6 - Multijugador: lobby y sincronización (2:30)",
        mision="Explicar que no hay server de juego sino PostgreSQL y el suavizado.",
        pantalla=[
            "Dos instancias del juego conectadas en la misma sala (grabar demo).",
            "db/red.py y juego/partida_multi.py.",
        ],
        guion=[
            "[MOSTRÁ: demo 2 ventanas online.] La mayor innovación es que el multiplayer NO tiene servidor "
            "de juego. Toda la red pasa por PostgreSQL. Acá vemos dos instancias jugando sincronizadas.",
            "[MOSTRÁ: db/red.py.] Un hilo paralelo de red hace upsert de nuestra posición cada 100 ms "
            "y lee las enemigas. Así el loop del juego nunca frena esperando la red, manteniendo 60 FPS.",
            "[MOSTRÁ: partida_multi.py.] A 10 Hz los rivales darían saltos. Lo solucionamos con "
            "'suavizado exponencial', acercándolos progresivamente cada frame para lograr movimiento fluido. "
            "En cambio, nuestro propio jugador usa física local para moverse sin input lag.",
            "Si faltan humanos en la sala, el cliente del 'host' los reemplaza simulando bots "
            "que envían sus posiciones a la DB, lo cual es transparente para el resto. Cierra [Persona 7].",
        ],
        preguntas=[
            ("¿Cuánta carga le pone a la DB?",
             "Son unas 10 escrituras chicas por segundo por cliente. En una red local no genera impacto."),
        ],
    ),
    # ------------------------------------------------------------------ #
    dict(
        encabezado="PERSONA 7 - Arbitraje atómico, pruebas y cierre (2:30)",
        mision="Mostrar cómo Postgres arbitra las capturas de forma atómica y cerrar.",
        pantalla=[
            "db/repositorio.py: intentar_captura().",
            "Consola: python tests_fase4.py.",
            "README.md: limitaciones.",
        ],
        guion=[
            "Si un cazador dice 'te atrapé' y un escapista dice 'escapé', ¿quién gana ante el lag? "
            "No lo decide el cliente, lo decide la base de datos atómicamente.",
            "[MOSTRÁ: intentar_captura().] Hacemos un UPDATE condicional. Verifica primero que las "
            "distancias almacenadas sean cortas. Postgres serializa estas transacciones. Si hay "
            "conflicto simultáneo, el primer UPDATE marca la captura y el segundo falla (rowcount 0).",
            "[MOSTRÁ: python tests_fase4.py.] Corremos una simulación de clientes reales en hilos "
            "que colisionan al mismo tiempo. El test prueba que el arbitraje rechaza reclamos falsos o lejanos.",
            "[MOSTRÁ: README.md.] Como conclusión, sabemos que por internet habría latencia de input, "
            "y si el host se desconecta, sus bots quedan quietos. Asumir limitaciones es parte de "
            "la ingeniería. Este fue nuestro proyecto El Gran Escape, ¡muchas gracias!",
        ],
        preguntas=[
            ("¿Qué mejorarían con más tiempo?",
             "Migraríamos a LISTEN/NOTIFY en Postgres para bajar el polling y aplicaríamos un anti-cheat básico."),
        ],
    ),
]

CONSEJOS = [
    ("Cómo grabar",
     ["Graben cada bloque por separado (cada uno el suyo) y júntenlo en la "
      "edición; queda mucho mejor que una llamada grupal continua.",
      "Aumenten la fuente del editor (Ctrl + + un par de veces).",
      "Las demos del juego grábenlas ANTES y pongan la voz en post.",
      "Para la demo multijugador: dos consolas, python main.py, ventanas lado a lado."]),
    ("Manejo del tiempo (Total ~17:30)",
     ["Cada persona tiene exactamente 2:30 asignado para hablar y mostrar.",
      "No incluyan las preguntas 'SI EL PROFESOR PREGUNTA' en el video."]),
    ("Comandos que se usan en el video",
     ["python main.py",
      "python -m juego.laberinto",
      "python tests_fase2.py",
      "python tests_fase4.py"]),
    ("Regla de oro",
     ["No lean textualmente: cuéntenlo natural. Las marcas [MOSTRÁ: ...] sí respétenlas "
      "porque indican qué debe verse."]),
]


# ====================================================================== #
# ARMADO DEL PDF
# ====================================================================== #

def pie(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#888888"))
    canvas.drawString(2 * cm, 1.1 * cm, "El Gran Escape - Guión del video de presentación (Max 17:30m)")
    canvas.drawRightString(A4[0] - 2 * cm, 1.1 * cm, f"Página {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(
    "Guion_video_El_Gran_Escape.pdf", pagesize=A4,
    leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm,
    bottomMargin=1.8 * cm, title="El Gran Escape - Guión del video",
    author="Grupo El Gran Escape")

story = []

# --- Portada ----------------------------------------------------------- #
story.append(Spacer(1, 8))
story.append(Paragraph("EL GRAN ESCAPE", S["titulo"]))
story.append(Paragraph(
    "Guión del video de presentación - 7 personas - 2:30 min cada uno",
    S["subtitulo"]))
story.append(Paragraph(
    "Proyecto final: juego multijugador de persecución en un laberinto "
    "procedural. 3 escapistas vs 2 cazadores. Python 3 + Pygame (pygame-ce) "
    "+ PostgreSQL 17 (psycopg 3). El multijugador se sincroniza por completo "
    "a través de la base de datos, sin servidor de juego.", S["normal"]))
story.append(Spacer(1, 8))

tabla = Table([[Paragraph(b(c) if i == 0 else c, S["normal"]) for c in fila]
               for i, fila in enumerate(RESUMEN)],
              colWidths=[2.3 * cm, 5.9 * cm, 2.0 * cm, 6.8 * cm])
tabla.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), AZUL),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, GRIS_FONDO]),
    ("GRID", (0, 0), (-1, -1), 0.5, GRIS_LINEA),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(tabla)
story.append(Spacer(1, 12))
story.append(Paragraph(
    "Cómo usar este guión: cada sección tiene tres partes. "
    + b("EN PANTALLA") + " es lo que tiene que verse mientras hablás. "
    + b("GUIÓN") + " es el texto sugerido, con marcas [MOSTRÁ: ...] "
    "para cambiar el contenido visual. " + b("SI EL PROFESOR PREGUNTA") + " "
    "es solo de preparación.", S["normal"]))
story.append(Paragraph(
    "Asignen los nombres acá: P1 ______, P2 ______, P3 ______, "
    "P4 ______, P5 ______, P6 ______, P7 ______.", S["nota"]))
story.append(PageBreak())

# --- Secciones por persona --------------------------------------------- #
for sec in SECCIONES:
    bloque = [Paragraph(sec["encabezado"], S["h_persona"]),
              Paragraph("<i>" + sec["mision"] + "</i>", S["nota"]),
              Paragraph("EN PANTALLA (en este orden)", S["h_bloque"])]
    for item in sec["pantalla"]:
        bloque.append(Paragraph(item, S["item"], bulletText="•"))
    story.append(KeepTogether(bloque))

    story.append(Paragraph("GUIÓN (lo que decís)", S["h_bloque"]))
    for p in sec["guion"]:
        p = re.sub(r"\[MOSTRÁ:[^\]]*\]",
                   lambda m: "<b>" + m.group(0) + "</b>", p)
        story.append(Paragraph(p, S["guion"]))

    qa = [Paragraph("SI EL PROFESOR PREGUNTA (no va en el video)", S["h_bloque"])]
    for pregunta, respuesta in sec["preguntas"]:
        qa.append(Paragraph("P: " + pregunta, S["qa_p"]))
        qa.append(Paragraph("R: " + respuesta, S["qa_r"]))
    story.append(KeepTogether(qa))
    story.append(PageBreak())

# --- Consejos finales --------------------------------------------------- #
story.append(Paragraph("CONSEJOS DE GRABACIÓN Y EDICIÓN", S["h_persona"]))
for titulo, items in CONSEJOS:
    bloque = [Paragraph(titulo, S["h_bloque"])]
    for item in items:
        bloque.append(Paragraph(item, S["item"], bulletText="•"))
    story.append(KeepTogether(bloque))

doc.build(story, onFirstPage=pie, onLaterPages=pie)
print("OK -> Guion_video_El_Gran_Escape.pdf actualizado con la máquina de estados en la Persona 1.")
