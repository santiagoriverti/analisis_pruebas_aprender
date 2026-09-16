"""Genera 04_contexto.ipynb (celdas con nbformat.v4) en la raíz del repo.

Uso (desde la raíz del repo):
  python scripts/generar_04_contexto.py                 # reescribe 04_contexto.ipynb SIN salidas → luego ejecutarlo con nbconvert
  python scripts/generar_04_contexto.py --debug         # ejecuta las celdas de código como script (prueba rápida, no escribe el notebook)
  python scripts/generar_04_contexto.py --debug --hasta N --post archivo.py   # corre hasta la celda N y luego un script con ese namespace

OJO: regenerar reemplaza el notebook versionado. Si solo hay que cambiar una celda, puede ser más simple editarla con
nbformat (ver CLAUDE.md). Después: python -m jupyter nbconvert --to notebook --execute --inplace 04_contexto.ipynb
"""
import sys, os
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # raíz del repo (scripts/..)
CELDAS = []
def md(s): CELDAS.append(('md', s.strip('\n')))
def code(s): CELDAS.append(('code', s.strip('\n')))

# ----------------------------------------------------------------------------------------------------------------------
md(r'''
# 04 · Contexto del estudiante en el tiempo — Pruebas APRENDER y Relevamiento Anual

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/santiagoriverti/analisis_pruebas_aprender/blob/main/04_contexto.ipynb)

Análisis **descriptivo** de cómo cambió el **contexto de los estudiantes** que rinden APRENDER, **dentro de cada cohorte
comparable** (misma nivel, grado y cobertura censal), y de las trayectorias escolares del **Relevamiento Anual (RA)**.

| Cohorte | Operativos |
|---|---|
| Primaria 6° grado (censal) | 2016 · 2018 · 2021 · 2023 · 2025 |
| Secundaria 5°/6° año (censal) | 2016 · 2017 · 2019 · 2022 · 2024 |

**Qué se mide (APRENDER, cuestionario complementario del estudiante):**
- **Trayectoria:** repitencia declarada, asistencia al jardín (desde sala de 3), sobreedad.
- **Hogar:** nivel educativo de la madre y del padre, libros en el hogar.
- **Acceso digital:** internet y computadora en el hogar, celular propio.
- **Trabajo y cuidados:** ayudar en el trabajo de familiares, trabajar para otros, cuidar familiares.

Cada indicador es el **% de estudiantes** (conteos ponderados del cuestionario `Solo CC`) que responde la opción indicada,
emparejando la **misma pregunta** entre años aunque cambie su código. Se abre por **país, sector, ámbito y provincia**.

**Cómo leerlo (importante):**
- Del denominador se excluyen las respuestas en **blanco, multimarca, sin dato y "No sé"**. Algunos años no ofrecen la
  opción "No sé" (p. ej. nivel educativo de la madre desde 2022/2023). El % que responde "No sé" figura en la sección 2
  (`pct_no_se`).
- Cuando la **redacción, el período de referencia o el formato** de la pregunta cambia (p. ej. "la semana pasada" frente a
  "habitualmente", o "marcá si hay" frente a "¿cuántos hay?"), **la línea se corta**: esos puntos no forman una serie.
  También se corta cuando **más del 10 % responde "No sé"** en un año y la opción no existe en otro (libros hasta
  2019/2021; nivel educativo de la madre en Primaria hasta 2021): al excluirlos cambia la base de comparación.
  El detalle de qué pregunta se usó cada año está en la sección 2 y en la hoja `preguntas_por_anio`.
- **Primaria 2025 no tiene diccionario de variables** y el cuestionario está renumerado. Jardín (`ap06`), repitencia (`ap07`)
  y libros (`ap24`) se identifican sin ambigüedad por sus opciones. Las preguntas de **acceso digital y de trabajo** tienen
  varias candidatas con distribución parecida: **no se imputan** y quedan sin dato en 2025.
- **Secundaria 2016** registra los objetos del hogar solo con la opción "Sí" (sin "No"): no permite calcular porcentajes.
- Son bases **agregadas**: no hay cruce por estudiante con el desempeño. **Sin econometría.**

**RA (2011–2025):** sobreedad, repitencia y abandono **por año de estudio**, egresados y brecha **mujeres/varones**.
La base *Trayectoria* del año *t* informa el **ciclo lectivo t−1**.

Requiere haber corrido antes `00_consolidacion.ipynb` (lee de *Mi unidad/`pruebas_aprender`*). No necesita el 01, 02 ni 03.
''')

md(r'''
---
## 0 · Setup y carga
''')
code(r'''
import os, re, glob, shutil, textwrap, unicodedata
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.lines import Line2D
import pyarrow.dataset as pads

def in_colab():
    try:
        import google.colab  # noqa
        return True
    except ImportError:
        return False

if in_colab():
    from google.colab import drive
    drive.mount('/content/drive')
    OUT = '/content/drive/MyDrive/pruebas_aprender/parquet'
else:
    OUT = os.path.join(os.getcwd(), 'datos_consolidados')
assert os.path.isdir(os.path.join(OUT, 'aprender_long')), (
    f'No encuentro el dataset en {OUT}. Corré primero 00_consolidacion.ipynb.')

# Paleta validada: fondo claro, grilla y ejes recesivos; azul/naranja para dos grupos; azul/rojo para cambios (+/−);
# rampa azul (claro → oscuro) para magnitudes en los mapas de calor
SUPERFICIE, TINTA, TINTA_2, TENUE, GRILLA, EJE = '#fcfcfb', '#0b0b0b', '#52514e', '#898781', '#e1e0d9', '#c3c2b7'
AZUL, NARANJA, ROJO, NEUTRO = '#2a78d6', '#eb6834', '#e34948', '#f0efec'
DIVERGENTE = LinearSegmentedColormap.from_list('divergente', [ROJO, NEUTRO, AZUL])
SECUENCIAL = LinearSegmentedColormap.from_list('secuencial', ['#f4f8fe', '#cde2fb', '#86b6ef', '#2a78d6', '#184f95', '#0d366b'])
plt.rcParams.update({
    'figure.dpi': 110, 'figure.facecolor': SUPERFICIE, 'axes.facecolor': SUPERFICIE, 'savefig.facecolor': SUPERFICIE,
    'font.family': 'sans-serif', 'font.sans-serif': ['Segoe UI', 'DejaVu Sans', 'Arial'],
    'text.color': TINTA, 'axes.labelcolor': TINTA_2, 'axes.edgecolor': EJE, 'axes.titlecolor': TINTA,
    'xtick.color': TENUE, 'ytick.color': TINTA_2, 'axes.grid': True, 'grid.color': GRILLA, 'grid.linewidth': 0.6,
    'axes.spines.top': False, 'axes.spines.right': False, 'axes.axisbelow': True})

# Carpeta de salida: gráficos a 300 dpi + Excel con las tablas (se descargan en un zip al final)
GRAF = os.path.abspath('graficos_contexto'); os.makedirs(GRAF, exist_ok=True)
def guardar(fig, nombre):
    fig.savefig(os.path.join(GRAF, nombre + '.png'), dpi=300, bbox_inches='tight')
    return fig
def nota(fig, texto, y=-0.01):
    fig.text(0.01, y, texto, fontsize=8, color=TENUE, ha='left', va='top')
FUENTE_AP = 'Fuente: Pruebas APRENDER, cuestionario complementario del estudiante (Secretaría de Educación). % ponderado sin blancos ni "No sé".'
FUENTE_RA = 'Fuente: Relevamiento Anual (RA), Secretaría de Educación.'
print('Datos consolidados en:', OUT)
print('Salidas (gráficos 300 dpi + Excel) en:', GRAF)
''')

md(r'''
---
## 1 · Funciones y especificación de indicadores
Cada indicador define, **por año**, el código de la pregunta, las opciones que cuentan en el numerador (o las que se
excluyen) y una etiqueta de **redacción**: años consecutivos con la misma etiqueta forman una serie; si la etiqueta
cambia, la línea se corta. Los `assert` verifican que cada opción exista en los datos (si el cuestionario cambia, falla).
''')
code(r'''
def _n(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()

# Nombres de provincia homogéneos entre años y entre APRENDER y el Relevamiento Anual
PROV_ALIAS = {'buenos aires': 'Buenos Aires', 'ciudad autonoma de buenos aires': 'CABA', 'ciudad de buenos aires': 'CABA',
              'tierra del fuego': 'Tierra del Fuego', 'tierra del fuego antartida e islas del atlantico sur': 'Tierra del Fuego'}
def norm_prov(s):
    return PROV_ALIAS.get(_n(s), str(s).strip())
SECTOR = {'Estatal': 'Estatal', 'Privado': 'Privado', 'Privada': 'Privado'}

COHORTES = {'Primaria 6°':     dict(nivel='Primaria',   grado='6 grado', anios=[2016, 2018, 2021, 2023, 2025]),
            'Secundaria 5-6°': dict(nivel='Secundaria', grado='5-6 año', anios=[2016, 2017, 2019, 2022, 2024])}
BLANCOS = {'Blanco', 'No_disponible', 'Multimarca', 'Dato_faltante'}
NO_SABE = re.compile(r'^(\d+_)?No_s[eé]$')

def archivos(anio):
    return sorted(glob.glob(os.path.join(OUT, 'aprender_long', f'anio={anio}', '*.parquet')))

_cache_cc = {}
def cuestionario(coh, anio, codigos):
    """Cuestionario Solo CC del operativo censal, solo con los códigos pedidos (para ahorrar memoria)."""
    k = (coh, anio)
    if k not in _cache_cc:
        c = COHORTES[coh]
        f = ((pads.field('area') == 'Solo CC') & (pads.field('cobertura') == 'Censal')
             & (pads.field('nivel') == c['nivel']) & (pads.field('grado') == c['grado']))
        d = (pads.dataset(archivos(anio), format='parquet')
             .to_table(filter=f, columns=['jurisdiccion', 'sector', 'ambito', 'variable', 'valor']).to_pandas())
        sp = d.variable.str.split('_', n=1)
        d['codigo'], d['opcion'] = sp.str[0], sp.str[1]
        d = d[d.codigo.isin(codigos)].copy()
        d['provincia'] = d.jurisdiccion.map(norm_prov)
        d['sector'] = d.sector.map(SECTOR)
        _cache_cc[k] = d.drop(columns=['jurisdiccion', 'variable'])
    return _cache_cc[k]

def S(codigo, r='misma pregunta', **kw):
    """Especificación de un año: código, etiqueta de redacción y num= (opciones) | excluir= | prefijo= | solo_nosabe=True."""
    return dict(codigo=codigo, r=r, **kw)

def conteos(d, s):
    """Numerador y denominador ponderados por provincia × sector × ámbito para una especificación."""
    x = d[d.codigo == s['codigo']]
    assert len(x), f"código {s['codigo']} sin datos"
    op = x.opcion
    if s.get('prefijo'):
        m_pref = op.str.startswith(s['prefijo'])
        x, op = x[m_pref], op[m_pref].str[len(s['prefijo']):]
    valido = ~op.isin(BLANCOS)
    nosabe = op.str.match(NO_SABE)
    if s.get('solo_nosabe'):
        assert nosabe.any(), f"{s['codigo']}: sin opción 'No sé'"
        num = nosabe
    else:
        valido &= ~nosabe
        ops = set(op[valido])
        if 'excluir' in s:
            assert set(s['excluir']) <= ops, f"{s['codigo']}: opciones a excluir inexistentes {set(s['excluir']) - ops}"
            num = ~op.isin(s['excluir'])
        elif callable(s['num']):
            num = op.map(s['num']).astype(bool)
        else:
            assert set(s['num']) <= ops, f"{s['codigo']} {s.get('prefijo') or ''}: opciones inexistentes {set(s['num']) - ops}"
            num = op.isin(s['num'])
    num &= valido
    assert num.any(), f"{s['codigo']}: numerador vacío"
    t = x.assign(num=x.valor.where(num, 0.0), den=x.valor.where(valido, 0.0))
    return t.groupby(['provincia', 'sector', 'ambito'])[['num', 'den']].sum().reset_index()

def pct_nosabe(d, s):
    """% del país que responde "No sé" (sobre respuestas válidas); 0 si la pregunta no ofrece esa opción."""
    x = d[d.codigo == s['codigo']]
    op = x.opcion
    if s.get('prefijo'):
        m_pref = op.str.startswith(s['prefijo'])
        x, op = x[m_pref], op[m_pref].str[len(s['prefijo']):]
    valido = ~op.isin(BLANCOS)
    return 100 * x.valor[valido & op.str.match(NO_SABE)].sum() / x.valor[valido].sum()
UMBRAL_NOSABE = 10   # si más del 10 % responde "No sé", excluirlo cambia la base: ese año forma otro tramo

NO_REALICE_22, NO_HICE_24 = {'No_realicé_esta_tarea'}, {'No_hice_estas_actividades'}
SOBRE = lambda o: 'de_sobreedad' in o
''')

code(r'''
# (tema, indicador, {año: especificación}); los años ausentes no tienen una pregunta equivalente identificable
IND = {
 'Primaria 6°': [
  ('Trayectoria', 'Repitió algún grado', {
      2016: S('Ap12', excluir={'1_Nunca'}), 2018: S('ap17', excluir={'No'}), 2021: S('ap25', excluir={'No'}),
      2023: S('ap22', excluir={'No'}), 2025: S('ap07', excluir={'No'})}),
  ('Trayectoria', 'Fue al jardín desde sala de 3 o antes', {
      2016: S('Ap11', num={'1_Sí_fui_al_jardín_antes_de_los_cuatro_años'}), 2018: S('ap16', num={'Sí_fui_al_jardín_antes_de_los_cuatro_años'}),
      2021: S('ap24', num={'Sí_fui_al_jardín_antes_de_los_4_años'}), 2023: S('ap21', num={'Sí_fui_al_jardín_desde_sala_de_3_o_antes'}),
      2025: S('ap06', num={'Sí_fui_al_jardín_desde_sala_de_3_o_antes'})}),
  ('Trayectoria', 'No fue al jardín', {
      2016: S('Ap11', num={'4_No_fui_al_jardín'}), 2018: S('ap16', num={'No_fui_al_jardín'}), 2021: S('ap24', num={'No_fui_al_jardín'}),
      2023: S('ap21', num={'No_no_fui_al_jardín'}), 2025: S('ap06', num={'No_no_fui_al_jardín'})}),
  ('Trayectoria', 'Con sobreedad (1 año o más)', {
      2021: S('sobreedad', num=SOBRE), 2023: S('sobreedad', num=SOBRE), 2025: S('sobreedad', num=SOBRE)}),
  ('Hogar', 'Madre con secundaria completa o más', {
      2016: S('Ap7', num={'Fue_a_la_escuela_secundaria_y_la_completó', 'Estudio_el_nivel_terciario_o_en_una_universidad'}),
      2018: S('ap9', num={'Secundaria_completa', 'Universitario_o_terciario_incompleto', 'Universitario_o_terciario_completo'}),
      2021: S('Nivel', prefijo='Ed_Madre_', num={'Secundario_completo', 'Terciario_Universitario_incompleto', 'Terciario_Universitario_completo', 'Posgrado_especialización_maestría_doctorado_etc'}),
      2023: S('Nivel', prefijo='Ed_Madre_', num={'Secundaria_completa', 'Terciario_universitario_posgrado_incompleto', 'Terciario_universitario_posgrado_completo'}),
      2025: S('Nivel', prefijo='Ed_Madre_', num={'Secundaria_completa', 'Terciario_universitario_posgrado_incompleto', 'Terciario_universitario_posgrado_completo'})}),
  ('Hogar', 'Madre con terciario o universitario completo', {
      2018: S('ap9', num={'Universitario_o_terciario_completo'}),
      2021: S('Nivel', prefijo='Ed_Madre_', num={'Terciario_Universitario_completo', 'Posgrado_especialización_maestría_doctorado_etc'}),
      2023: S('Nivel', prefijo='Ed_Madre_', num={'Terciario_universitario_posgrado_completo'}),
      2025: S('Nivel', prefijo='Ed_Madre_', num={'Terciario_universitario_posgrado_completo'})}),
  ('Hogar', 'Padre con secundaria completa o más', {
      2016: S('Ap8', num={'Fue_a_la_escuela_secundaria_y_la_completó', 'Estudio_el_nivel_terciario_o_en_una_universidad'}),
      2018: S('ap10', num={'Secundaria_completa', 'Universitario_o_terciario_incompleto', 'Universitario_o_terciario_completo'}),
      2021: S('Nivel', prefijo='Ed_Padre_', num={'Secundario_completo', 'Terciario_Universitario_incomple', 'Terciario_Universitario_completo', 'Posgrado_especialización_maestría_doctorado_etc'}),
      2023: S('Nivel', prefijo='Ed_Padre_', num={'Secundaria_completa', 'Terciario_universitario_posgrado_incompleto', 'Terciario_universitario_posgrado_completo'}),
      2025: S('Nivel', prefijo='Ed_Padre_', num={'Secundaria_completa', 'Terciario_universitario_posgrado_incompleto', 'Terciario_universitario_posgrado_completo'})}),
  ('Hogar', 'No sabe el nivel educativo de la madre', {
      2016: S('Ap7', solo_nosabe=True), 2018: S('ap9', solo_nosabe=True), 2021: S('Nivel', prefijo='Ed_Madre_', solo_nosabe=True)}),
  ('Hogar', 'Más de 50 libros en el hogar', {
      2018: S('ap8', num={'De_51_a_100_libros', 'Más_de_100_libros'}), 2021: S('ap15', num={'De_51_a_100_libros', 'Más_de_100_libros'}),
      2023: S('ap10', num={'De_51_a_100_libros', 'Más_de_100_libros'}), 2025: S('ap24', num={'51_a_100_libros', 'Más_de_100_libros'})}),
  ('Hogar', 'Sin libros en el hogar', {
      2018: S('ap8', num={'No_hay_libros'}), 2021: S('ap15', num={'No_hay_libros'}),
      2023: S('ap10', num={'No_tengo_libros_en_formato_papel'}), 2025: S('ap24', num={'No_hay_libros'})}),
  ('Acceso digital', 'Internet en el hogar', {
      2016: S('Ap28j', num={'Si'}), 2018: S('ap7a', num={'Sí'}),
      2021: S('ap10c', 'marcar de una lista', num={'Si'}), 2023: S('ap09d', num={'Sí'})}),
  ('Acceso digital', 'Computadora en el hogar', {
      2018: S('ap7c', num={'Sí'}), 2021: S('ap11d', '¿cuántas hay?', excluir={'Ninguno'}), 2023: S('ap09i', num={'Sí'})}),
  ('Acceso digital', 'Celular propio', {
      2016: S('Ap29', num={'1_Sí'}), 2018: S('ap27a', num={'Sí'}), 2023: S('ap11', num={'Sí'})}),
  ('Trabajo y cuidados', 'Ayuda a familiares en su trabajo', {
      2016: S('Ap9a', 'la semana pasada', num={'Si'}), 2018: S('ap14', 'habitualmente', num={'Sí'}),
      2021: S('ap20a', 'habitualmente', num={'Si'}), 2023: S('ap07a', 'la semana pasada', excluir=NO_REALICE_22)}),
  ('Trabajo y cuidados', 'Trabaja para alguien que no es de su familia', {
      2016: S('Ap10', 'trabajó fuera de casa la semana pasada', num={'1_Sí'}), 2018: S('ap15', 'habitualmente, fuera de casa', num={'Sí'}),
      2021: S('ap20b', 'habitualmente', num={'Si'}), 2023: S('ap07b', 'la semana pasada', excluir=NO_REALICE_22)}),
  ('Trabajo y cuidados', 'Cuida a hermanos u otros familiares', {
      2016: S('Ap9b', 'la semana pasada, solo/a', num={'Si'}), 2018: S('ap13a', 'con qué frecuencia', excluir={'Nunca'}),
      2021: S('ap19a', 'con qué frecuencia', excluir={'Nunca'}), 2023: S('ap06a', 'la semana pasada', excluir=NO_REALICE_22)}),
 ],
 'Secundaria 5-6°': [
  ('Trayectoria', 'Repitió en la primaria', {
      2016: S('Ap15', excluir={'1_Nunca'}), 2017: S('ap20', excluir={'No'}), 2019: S('ap25', prefijo='01_', excluir={'No'}),
      2022: S('ap25a', excluir={'No'}), 2024: S('ap25a', excluir={'No'})}),
  ('Trayectoria', 'Repitió en la secundaria (algún año)', {
      2016: S('Ap16', excluir={'1_Nunca'}), 2017: S('ap21', excluir={'No'})}),
  ('Trayectoria', 'Repitió en el ciclo básico', {
      2019: S('ap25', prefijo='02_', excluir={'No'}), 2022: S('ap25b', excluir={'No'}), 2024: S('ap25b', excluir={'No'})}),
  ('Trayectoria', 'Fue al jardín desde sala de 3 o antes', {
      2016: S('Ap14', num={'1_Sí_fui_al_jardín_antes_de_los_cuatro_años'}), 2017: S('ap19', num={'Sí_fui_al_jardín_antes_de_los_cuatro_años'}),
      2019: S('ap24', num={'Sí_antes_de_los_cuatro_años'}), 2022: S('ap24', num={'Sí_desde_sala_de_3_años'}),
      2024: S('ap24', num={'Sí_desde_sala_de_3_o_antes'})}),
  ('Trayectoria', 'No fue al jardín', {
      2016: S('Ap14', num={'4_No_fui_al_jardín'}), 2017: S('ap19', num={'No_fui_al_jardín'}), 2019: S('ap24', num={'No_asistí'}),
      2022: S('ap24', num={'No_no_fui_al_jardín'}), 2024: S('ap24', num={'No_no_fui_al_jardín'})}),
  ('Trayectoria', 'Con sobreedad (1 año o más)', {
      2019: S('sobreedad', num=SOBRE), 2022: S('sobreedad', num=SOBRE), 2024: S('sobreedad', num=SOBRE)}),
  ('Hogar', 'Madre con secundaria completa o más', {
      2016: S('Ap7', num={'4_Terminó_la_escuela_secundaria', '5_Tiene_estudios_terciarios', '6_Tiene_estudios_universitarios'}),
      2017: S('ap10', num={'Secundaria_completa', 'Universitario_o_terciario_incompleto', 'Universitario_o_terciario_completo'}),
      2019: S('ap16', num={'Secundaria_completa', 'Educación_superior_terciaria', 'Educación_superior_universitaria', 'Posgrado'}),
      2022: S('Nivel', prefijo='Ed_Madre_', num={'Secundaria_completa', 'Terciario_universitario_posgrado_incompleto', 'Terciario_universitario_posgrado_completo'}),
      2024: S('Nivel', prefijo='Ed_Madre_', num={'Secundaria_completo', 'Terciariouniversitarioposgrado_incompleto', 'Terciariouniversitarioposgrado_completo'})}),
  ('Hogar', 'Madre con terciario o universitario completo', {
      2017: S('ap10', num={'Universitario_o_terciario_completo'}),
      2022: S('Nivel', prefijo='Ed_Madre_', num={'Terciario_universitario_posgrado_completo'}),
      2024: S('Nivel', prefijo='Ed_Madre_', num={'Terciariouniversitarioposgrado_completo'})}),
  ('Hogar', 'Padre con secundaria completa o más', {
      2016: S('Ap8', num={'4_Terminó_la_escuela_secundaria', '5_Tiene_estudios_terciarios', '6_Tiene_estudios_universitarios'}),
      2017: S('ap11', num={'Secundaria_completa', 'Universitario_o_terciario_incompleto', 'Universitario_o_terciario_completo'}),
      2019: S('ap17', num={'Secundaria_completa', 'Educación_superior_terciaria', 'Educación_superior_universitaria', 'Posgrado'}),
      2022: S('Nivel', prefijo='Ed_Padre_', num={'Secundaria_completa', 'Terciario_universitario_posgrado_incompleto', 'Terciario_universitario_posgrado_completo'}),
      2024: S('Nivel', prefijo='Ed_Padre_', num={'Secundaria_completo', 'Terciariouniversitarioposgrado_incompleto', 'Terciariouniversitarioposgrado_completo'})}),
  ('Hogar', 'No sabe el nivel educativo de la madre', {
      2016: S('Ap7', solo_nosabe=True), 2019: S('ap16', solo_nosabe=True)}),
  ('Hogar', 'Más de 50 libros en el hogar', {
      2017: S('ap9', num={'De_51_a_100_libros', 'Más_de_100_libros'}), 2019: S('ap15', num={'De_51_a_100_libros', 'Más_de_100_libros'}),
      2022: S('ap15', num={'De_51_a_100_libros', 'Más_de_100_libros'}), 2024: S('ap19', num={'De_51_a_100_libros', 'Más_de_100_libros'})}),
  ('Hogar', 'Sin libros en el hogar', {
      2017: S('ap9', num={'No_hay_libros'}), 2019: S('ap15', num={'No_hay_libros'}),
      2022: S('ap15', num={'No_tengo_libros_en_formato_papel'}), 2024: S('ap19', num={'No_hay_libros_en_formato_papel'})}),
  ('Acceso digital', 'Internet en el hogar', {
      2017: S('ap7d', num={'Sí'}), 2019: S('ap11', prefijo='08_', num={'Si'}), 2022: S('ap12k', num={'Sí'}), 2024: S('ap16k', num={'Sí'})}),
  ('Acceso digital', 'Computadora en el hogar', {
      2017: S('ap8b', num={'Sí'}), 2019: S('ap11', '¿cuántas hay?', prefijo='06_', excluir={'Ninguno'}),
      2022: S('ap12g', num={'Sí'}), 2024: S('ap16g', num={'Sí'})}),
  ('Acceso digital', 'Celular propio', {
      2016: S('Ap41', num={'1_Sí'}), 2017: S('ap46a', num={'Sí'}), 2019: S('ap12', num={'Sí'}), 2022: S('ap13', num={'Sí'}), 2024: S('ap16f', num={'Sí'})}),
  ('Trabajo y cuidados', 'Ayuda a familiares en su trabajo', {
      2016: S('Ap10a', 'la semana pasada', num={'Si'}), 2019: S('ap19', 'las últimas dos semanas', num={'Sí'}),
      2024: S('ap22c', 'la semana pasada', excluir=NO_HICE_24)}),
  ('Trabajo y cuidados', 'Trabaja para un empleador o no familiar', {
      2016: S('Ap11', 'trabajó fuera de casa la semana pasada', num={'1_Sí'}), 2017: S('ap17', 'habitualmente', num={'Sí'}),
      2022: S('ap19a', 'la semana pasada', excluir=NO_REALICE_22), 2024: S('ap22b', 'la semana pasada', excluir=NO_HICE_24)}),
  ('Trabajo y cuidados', 'Cuida a familiares sin ayuda', {
      2016: S('Ap10b', 'la semana pasada', num={'Si'}), 2017: S('ap15a', 'con qué frecuencia', excluir={'Nunca'}),
      2022: S('ap18b', 'la semana pasada', excluir=NO_REALICE_22), 2024: S('ap21b', 'la semana pasada', excluir=NO_HICE_24)}),
 ]}

# Diccionario usado para mostrar el texto de cada pregunta (2025 no tiene diccionario propio)
DIC_ANIO = {('Primaria 6°', 2016): (2016, 'Primaria'), ('Primaria 6°', 2018): (2018, 'General'), ('Primaria 6°', 2021): (2021, 'General'),
            ('Primaria 6°', 2023): (2023, 'General'), ('Secundaria 5-6°', 2016): (2016, 'Secundaria'),
            ('Secundaria 5-6°', 2017): (2017, 'Secundaria'), ('Secundaria 5-6°', 2019): (2019, 'General'),
            ('Secundaria 5-6°', 2022): (2022, 'General'), ('Secundaria 5-6°', 2024): (2024, 'Secundaria')}
dic = pd.read_parquet(os.path.join(OUT, 'diccionario_aprender.parquet'))
dic['cod'] = dic.variable.str.split('_').str[0].str.lower()

filas, preguntas = [], []
for coh, lista in IND.items():
    codigos = {s['codigo'] for _, _, sp in lista for s in sp.values()}
    for anio in COHORTES[coh]['anios']:
        d = cuestionario(coh, anio, codigos)
        for orden, (tema, nombre, sp) in enumerate(lista):
            if anio not in sp: continue
            s = sp[anio]
            ns = pct_nosabe(d, s)
            red = s['r'] + (' · con "No sé" > 10 %' if ns > UMBRAL_NOSABE and not s.get('solo_nosabe') else '')
            filas.append(conteos(d, s).assign(cohorte=coh, orden=orden, tema=tema, indicador=nombre, anio=anio, redaccion=red))
            if (coh, anio) in DIC_ANIO:
                ya, nv = DIC_ANIO[(coh, anio)]
                txt = dic[(dic.anio_dic == ya) & (dic.nivel_dic == nv) & (dic.cod == s['codigo'].lower())].pregunta_texto
                texto = txt.iloc[0] if len(txt) else '(sin texto en el diccionario)'
            else:
                texto = '(sin diccionario 2025: identificada por sus opciones)'
            num = ('"No sé"' if s.get('solo_nosabe') else 'todas menos: ' + ', '.join(sorted(s['excluir'])) if 'excluir' in s
                   else 'opciones con sobreedad' if callable(s.get('num')) else ', '.join(sorted(s['num'])))
            preguntas.append(dict(cohorte=coh, tema=tema, indicador=nombre, anio=anio, codigo=s['codigo'] + (' ' + s['prefijo'] if s.get('prefijo') else ''),
                                  pregunta=texto, numerador=num, pct_no_se=round(ns, 1), redaccion=red))
BASE = pd.concat(filas, ignore_index=True)
PREGUNTAS = pd.DataFrame(preguntas)

def tabla(por):
    """% por indicador y año, abierto por las columnas `por` ([] = país)."""
    k = ['cohorte', 'orden', 'tema', 'indicador', 'anio', 'redaccion'] + por
    t = BASE.groupby(k)[['num', 'den']].sum().reset_index()
    t['pct'] = 100 * t.num / t.den
    return t.sort_values(['cohorte', 'orden', 'anio'] + por, kind='stable')

PAIS, POR_SECTOR, POR_AMBITO, POR_PROV = tabla([]), tabla(['sector']), tabla(['ambito']), tabla(['provincia'])
assert POR_PROV.groupby(['cohorte', 'indicador', 'anio']).provincia.nunique().min() >= 23
assert set(POR_SECTOR.sector) == {'Estatal', 'Privado'} and set(POR_AMBITO.ambito) == {'Rural', 'Urbano'}
print('Indicadores:', {c: len(l) for c, l in IND.items()}, '· combinaciones indicador × año:', len(PAIS))
''')

md(r'''
---
## 2 · Qué pregunta se usa cada año
`redaccion` indica el tramo comparable: la línea de los gráficos solo une años **consecutivos** con la misma etiqueta.
''')
code(r'''
pd.set_option('display.max_colwidth', 90)
for coh in COHORTES:
    print(f'\n### {coh}')
    display(PREGUNTAS[PREGUNTAS.cohorte == coh].drop(columns='cohorte').set_index(['tema', 'indicador', 'anio']))
''')

# ---------------------------------------------------------------- A · país
md(r'''
---
## A · Evolución en el país
% de estudiantes de cada cohorte. **Línea cortada = cambió la redacción, el período o el formato de la pregunta** (esos
puntos no son comparables entre sí). Valores del último año rotulados; todos los valores en la tabla.
''')
code(r'''
def tramos(anios, tags):
    """Años consecutivos (de la cohorte) con la misma etiqueta de redacción; None corta el tramo."""
    out, cur, prev = [], [], object()
    for a, t in zip(anios, tags):
        if t is None or (cur and t != prev):
            if cur: out.append(cur)
            cur = []
        if t is not None: cur.append(a)
        prev = t
    if cur: out.append(cur)
    return out

def panel(ax, t, anios, grupos, colores, rotular):
    """Dibuja un indicador: una serie por grupo, cortada donde cambia la redacción."""
    for g, col in zip(grupos, colores):
        s = (t if g is None else t[t.grupo == g]).set_index('anio').reindex(anios)
        tags = [None if pd.isna(v) else v for v in s.redaccion]
        for tr in tramos(anios, tags):
            ax.plot(tr, s.loc[tr, 'pct'], color=col, lw=2, marker='o', ms=5, mec=SUPERFICIE, mew=1)
        if rotular and s.pct.notna().any():
            a = s.pct.last_valid_index()
            ax.annotate(f'{s.pct[a]:.0f}', (a, s.pct[a]), xytext=(4, 0), textcoords='offset points', fontsize=7.5,
                        color=TINTA_2, va='center')
    ax.set_xticks(anios); ax.set_xticklabels([str(a)[2:] for a in anios], fontsize=8)
    ax.set_xlim(anios[0] - 0.7, anios[-1] + 1.2)
    ax.tick_params(axis='y', labelsize=8)

def multiples(tabla_larga, coh, grupos=(None,), colores=(AZUL,), titulo='', leyenda=None, rotular=True):
    lista = IND[coh]; anios = COHORTES[coh]['anios']
    n = len(lista); nc = 5; nf = int(np.ceil(n / nc))
    fig, axs = plt.subplots(nf, nc, figsize=(15.5, 2.55 * nf + 0.6), squeeze=False)
    for i, (tema, nombre, _) in enumerate(lista):
        ax = axs.flat[i]
        t = tabla_larga[(tabla_larga.cohorte == coh) & (tabla_larga.indicador == nombre)]
        panel(ax, t, anios, grupos, colores, rotular)
        top = t.pct.max()
        ax.set_ylim(0, min(100, top * 1.25 + 2) if top > 8 else top * 1.6 + 0.5)
        tit = textwrap.fill(nombre, 30)
        ax.set_title(tit, fontsize=9.5, loc='left')
        ax.annotate(tema.upper(), xy=(0, 1), xycoords='axes fraction', xytext=(0, 9 + 13 * (tit.count('\n') + 1)),
                    textcoords='offset points', fontsize=7, color=TENUE, va='bottom')
    for ax in axs.flat[n:]: ax.set_visible(False)
    fig.suptitle(titulo, x=0.01, ha='left', fontsize=13, y=1.0)
    if leyenda:
        fig.legend(handles=[Line2D([], [], color=c, lw=2, marker='o', label=l) for l, c in zip(leyenda, colores)],
                   loc='upper right', ncol=len(leyenda), frameon=False, bbox_to_anchor=(0.99, 1.01))
    fig.tight_layout(h_pad=1.6)
    nota(fig, FUENTE_AP + ' Línea cortada: cambia la redacción/período/formato de la pregunta (ver sección 2).')
    return fig

def ancho(t, por=None):
    idx = ['tema', 'indicador'] + ([por] if por else [])
    w = t.pivot_table(index=['orden'] + idx, columns='anio', values='pct').round(1)
    return w.droplevel('orden')

for i, coh in enumerate(COHORTES, start=1):
    guardar(multiples(PAIS, coh, titulo=f'A{i} · {coh}: contexto de los estudiantes (% del total del país)'), f'A{i}_pais_{"primaria" if i == 1 else "secundaria"}')
    plt.show()
    display(ancho(PAIS[PAIS.cohorte == coh]))
''')

# ---------------------------------------------------------------- B · sector y ámbito
md(r'''
---
## B · Por sector de gestión y ámbito
Mismos indicadores para **estatal vs privado** (B1, B2) y **urbano vs rural** (B3, B4). La tabla muestra la **brecha en
puntos porcentuales** (privado − estatal; urbano − rural) por año.
''')
code(r'''
def brecha(t, col, a, b):
    w = t.pivot_table(index=['cohorte', 'orden', 'tema', 'indicador', 'anio'], columns=col, values='pct')
    return (w[a] - w[b]).rename(f'{a} − {b} (pp)').reset_index()

BRECHAS = {}
k = 1
for dim, col, grupos, etiq in [('sector', 'sector', ['Estatal', 'Privado'], ['Estatal', 'Privado']),
                               ('ámbito', 'ambito', ['Urbano', 'Rural'], ['Urbano', 'Rural'])]:
    t = (POR_SECTOR if col == 'sector' else POR_AMBITO).rename(columns={col: 'grupo'})
    for coh in COHORTES:
        fig = multiples(t, coh, grupos=grupos, colores=[AZUL, NARANJA], leyenda=etiq, rotular=False,
                        titulo=f'B{k} · {coh}: contexto por {dim} (% de estudiantes)')
        guardar(fig, f'B{k}_{col}_{"primaria" if coh.startswith("Prim") else "secundaria"}'); plt.show()
        k += 1
    a, b = ('Privado', 'Estatal') if col == 'sector' else ('Urbano', 'Rural')
    br = brecha(t.rename(columns={'grupo': col}), col, a, b)
    BRECHAS[col] = br
    for coh in COHORTES:
        print(f'\nBrecha {a} − {b} (pp) · {coh}')
        display(br[br.cohorte == coh].pivot_table(index=['orden', 'tema', 'indicador'], columns='anio', values=f'{a} − {b} (pp)').round(1).droplevel('orden'))
''')

# ---------------------------------------------------------------- C · provincias
md(r'''
---
## C · Provincias
Para cada indicador se toma el **último tramo comparable** (años consecutivos con la misma redacción, de al menos dos
operativos y que llega a uno de los dos últimos) y se calcula el **cambio en pp** entre su primer y último año, por provincia. Azul = sube,
rojo = baja (sin juicio de valor: que baje la repitencia o el trabajo infantil es una mejora). Escala recortada a ±15 pp;
el número es el valor exacto. Los valores de todos los años están en la hoja `provincias` del Excel.
''')
code(r'''
def ultimo_tramo(coh, nombre):
    """Último tramo comparable (≥ 2 años) si termina en alguno de los dos últimos operativos; si no, None."""
    anios = COHORTES[coh]['anios']
    t = PAIS[(PAIS.cohorte == coh) & (PAIS.indicador == nombre)].set_index('anio').reindex(anios)
    trs = [tr for tr in tramos(list(t.index), [None if pd.isna(v) else v for v in t.redaccion]) if len(tr) >= 2]
    return trs[-1] if trs and trs[-1][-1] in anios[-2:] else None

CAMBIO_PROV, CAMBIO_PAIS = {}, {}
for i, coh in enumerate(COHORTES, start=1):
    cols, paises = {}, {}
    for tema, nombre, _ in IND[coh]:
        tr = ultimo_tramo(coh, nombre)
        if tr is None: continue
        p = POR_PROV[(POR_PROV.cohorte == coh) & (POR_PROV.indicador == nombre)].pivot_table(index='provincia', columns='anio', values='pct')
        etiqueta = f'{nombre} ({str(tr[0])[2:]}→{str(tr[-1])[2:]})'
        cols[etiqueta] = p[tr[-1]] - p[tr[0]]
        n = PAIS[(PAIS.cohorte == coh) & (PAIS.indicador == nombre)].set_index('anio').pct
        paises[etiqueta] = n[tr[-1]] - n[tr[0]]
    c = pd.DataFrame(cols)
    c = c.sort_index(key=lambda i: i.map(_n))
    CAMBIO_PROV[coh], CAMBIO_PAIS[coh] = c, pd.Series(paises, name='País')
    assert len(c) == 24 or coh.startswith('Sec'), coh

    fig, ax = plt.subplots(figsize=(0.62 * c.shape[1] + 3.2, 0.34 * (len(c) + 1) + 2.2))
    m = pd.concat([c, CAMBIO_PAIS[coh].to_frame().T])
    im = ax.imshow(m.values, cmap=DIVERGENTE, norm=TwoSlopeNorm(0, -15, 15), aspect='auto')
    ax.set_xticks(range(m.shape[1])); ax.set_xticklabels([textwrap.fill(x, 26) for x in m.columns], rotation=90, fontsize=8)
    ax.set_yticks(range(len(m))); ax.set_yticklabels(m.index, fontsize=8.5)
    ax.get_yticklabels()[-1].set_fontweight('bold')
    ax.axhline(len(m) - 1.5, color=TINTA, lw=1)
    for (r, q), v in np.ndenumerate(m.values):
        if pd.notna(v):
            ax.text(q, r, f'{v:+.0f}', ha='center', va='center', fontsize=6.5, color=SUPERFICIE if abs(v) > 9 else TINTA)
    ax.grid(False); ax.xaxis.tick_top()
    for s in ax.spines.values(): s.set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.01); cb.set_label('cambio (pp)', fontsize=8); cb.ax.tick_params(labelsize=7)
    ax.set_title(f'C{i} · {coh}: cambio por provincia en el último tramo comparable (pp)', loc='left', fontsize=12, pad=12)
    nota(fig, FUENTE_AP + (' Celdas vacías: provincia sin dato en el año inicial (Chubut, Secundaria 2019).' if c.isna().any().any() else ''))
    guardar(fig, f'C{i}_provincias_{"primaria" if i == 1 else "secundaria"}'); plt.show()
    display(m.round(1))
''')

# ---------------------------------------------------------------- D · RA
md(r'''
---
## D · Trayectorias en el Relevamiento Anual (2011–2025)
Series de tiempo del sistema completo (no solo de quienes rinden APRENDER). Años de estudio 1 a 12 (1–6 primaria,
7–12 secundaria, homogeneizados por la fuente). **Trayectoria del año *t* = ciclo lectivo *t−1***: repitencia
(`nopromo`), abandono (`ssp`, salidos sin pase) y egresados se muestran por ciclo lectivo. La sobreedad es de la
matrícula del año relevado.
''')
code(r'''
def cargar_ra(base):
    return pd.read_parquet(os.path.join(OUT, 'ra', f'ra_{base}.parquet'))
def num(df, cols):
    return df[cols].apply(pd.to_numeric, errors='coerce').astype('float64').fillna(0)

MAT, TRA = cargar_ra('matricula'), cargar_ra('trayectoria')
AE = list(range(1, 13)); PRIM, SEC = range(1, 7), range(7, 13)
ETQ_AE = [f'{i}°' for i in AE]   # años de estudio homogeneizados: 1°–6° primaria, 7°–12° secundaria

def por_anio(df, prefijo, anios_estudio, por='anio'):
    cols = [f'{prefijo}_{i}' for i in anios_estudio]
    return num(df, cols).groupby(df[por] if isinstance(por, str) else [df[p] for p in por]).sum().set_axis(list(anios_estudio), axis=1)

# D1 · sobreedad por año de estudio (matrícula del año)
SOBREEDAD_AE = 100 * por_anio(MAT, 's', AE) / por_anio(MAT, '', AE)
# D2 · repitencia y abandono por año de estudio (ciclo lectivo = año − 1)
ini = por_anio(TRA, 'inicial', AE)
REPITENCIA_AE = (100 * por_anio(TRA, 'nopromo', AE) / ini).rename(index=lambda a: a - 1)
ABANDONO_AE = (100 * por_anio(TRA, 'ssp', AE) / ini).rename(index=lambda a: a - 1)
for t in (REPITENCIA_AE, ABANDONO_AE): t.index.name = 'ciclo_lectivo'
SOBREEDAD_AE.index.name = 'anio'

def mapa_calor(ax, t, titulo, fmt='{:.0f}', vmax=None):
    m = t.T.values
    im = ax.imshow(m, cmap=SECUENCIAL, aspect='auto', vmin=0, vmax=vmax or np.nanmax(m))
    ax.set_xticks(range(t.shape[0])); ax.set_xticklabels([str(a)[2:] for a in t.index], fontsize=8)
    ax.set_yticks(range(t.shape[1])); ax.set_yticklabels(ETQ_AE if t.shape[1] == 12 else t.columns, fontsize=8)
    lim = (vmax or np.nanmax(m)) * 0.55
    for (r, q), v in np.ndenumerate(m):
        ax.text(q, r, fmt.format(v), ha='center', va='center', fontsize=6.5, color=SUPERFICIE if v > lim else TINTA)
    ax.axhline(5.5, color=SUPERFICIE, lw=2.5)
    ax.grid(False); ax.set_title(titulo, loc='left', fontsize=10.5)
    ax.set_ylabel('año de estudio  (primaria 1°–6° · secundaria 7°–12°)', fontsize=8)
    for s in ax.spines.values(): s.set_visible(False)
    return im

fig, ax = plt.subplots(figsize=(10, 5.2))
mapa_calor(ax, SOBREEDAD_AE, 'D1 · % de alumnos con sobreedad por año de estudio y año')
ax.set_xlabel('año del relevamiento')
nota(fig, FUENTE_RA + ' Base Matrícula: s_i / matrícula del año de estudio i.')
guardar(fig, 'D1_ra_sobreedad_anio_estudio'); plt.show()
display(SOBREEDAD_AE.T.set_axis(ETQ_AE).round(1))

fig, axs = plt.subplots(1, 2, figsize=(15, 5.2))
mapa_calor(axs[0], REPITENCIA_AE, 'D2 · Repitencia (%) por año de estudio', fmt='{:.0f}')
mapa_calor(axs[1], ABANDONO_AE, 'D2 · Abandono (%) por año de estudio', fmt='{:.1f}')
for ax in axs: ax.set_xlabel('ciclo lectivo')
fig.tight_layout()
nota(fig, FUENTE_RA + ' Base Trayectoria del año t = ciclo lectivo t−1. Repitencia = no promovidos / matrícula inicial (en 12° incluye a quienes no egresan por materias adeudadas); abandono = salidos sin pase / matrícula inicial.')
guardar(fig, 'D2_ra_repitencia_abandono_anio_estudio'); plt.show()
print('Repitencia por año de estudio (%)'); display(REPITENCIA_AE.T.set_axis(ETQ_AE).round(1))
print('Abandono por año de estudio (%)'); display(ABANDONO_AE.T.set_axis(ETQ_AE).round(1))
''')

code(r'''
# D3 · egresados por ciclo lectivo y % de mujeres
cols_eg = ['primaria_egresados', 'primaria_m_egresados', 'secundaria_egresados', 'secundaria_m_egresados']
eg_prov = num(TRA, cols_eg).assign(anio=TRA.anio, provincia=TRA.provincia.map(norm_prov)).groupby(['anio', 'provincia']).sum()
eg = eg_prov.groupby('anio').sum()
# Cobertura: en los primeros relevamientos varias provincias informan 0 egresados → ese ciclo no es comparable
sin_dato = {niv: (eg_prov[f'{niv}_egresados'] == 0).groupby('anio').sum() for niv in ['primaria', 'secundaria']}
eg.index = eg.index - 1; eg.index.name = 'ciclo_lectivo'
EGRESADOS = pd.DataFrame({
    'egresados primaria (miles)': eg.primaria_egresados / 1e3, 'egresados secundaria (miles)': eg.secundaria_egresados / 1e3,
    '% mujeres · primaria': 100 * eg.primaria_m_egresados / eg.primaria_egresados,
    '% mujeres · secundaria': 100 * eg.secundaria_m_egresados / eg.secundaria_egresados})
for niv in ['primaria', 'secundaria']:
    malos = [a - 1 for a, n in sin_dato[niv].items() if n > 0]
    EGRESADOS.loc[malos, [f'egresados {niv} (miles)', f'% mujeres · {niv}']] = np.nan
    print(f'Egresados de {niv}: ciclos excluidos por provincias sin dato (0 egresados):',
          {a - 1: int(n) for a, n in sin_dato[niv].items() if n > 0} or 'ninguno')

# D4 · brecha mujeres / varones en repitencia y abandono (por nivel)
def tasa_sexo(prefijo, rango):
    tot, muj = por_anio(TRA, prefijo, rango).sum(axis=1), por_anio(TRA, f'm_{prefijo}', rango).sum(axis=1)
    it, im_ = por_anio(TRA, 'inicial', rango).sum(axis=1), por_anio(TRA, 'm_inicial', rango).sum(axis=1)
    out = pd.DataFrame({'Mujeres': 100 * muj / im_, 'Varones': 100 * (tot - muj) / (it - im_)})
    out.index = out.index - 1; out.index.name = 'ciclo_lectivo'
    return out
GENERO = {(ind, niv): tasa_sexo(p, r) for ind, p in [('Repitencia', 'nopromo'), ('Abandono', 'ssp')]
          for niv, r in [('primaria', PRIM), ('secundaria', SEC)]}

fig, axs = plt.subplots(1, 2, figsize=(13, 4))
for col, c in [('egresados primaria (miles)', AZUL), ('egresados secundaria (miles)', NARANJA)]:
    axs[0].plot(EGRESADOS.index, EGRESADOS[col], color=c, lw=2, marker='o', ms=4, label=col.replace(' (miles)', ''))
for col, c in [('% mujeres · primaria', AZUL), ('% mujeres · secundaria', NARANJA)]:
    axs[1].plot(EGRESADOS.index, EGRESADOS[col], color=c, lw=2, marker='o', ms=4, label=col.replace('% mujeres · ', ''))
axs[0].set_title('D3 · Egresados por ciclo lectivo (miles)', loc='left', fontsize=10.5); axs[0].set_ylim(0)
axs[1].set_title('D3 · % de mujeres entre los egresados', loc='left', fontsize=10.5); axs[1].axhline(50, color=EJE, lw=1, ls='--')
for ax in axs: ax.legend(frameon=False, fontsize=8.5); ax.set_xlabel('ciclo lectivo')
fig.tight_layout(); nota(fig, FUENTE_RA + ' Base Trayectoria del año t = ciclo lectivo t−1. Sin punto: ciclos con provincias que informan 0 egresados.')
guardar(fig, 'D3_ra_egresados'); plt.show()
display(EGRESADOS.round(1))

fig, axs = plt.subplots(2, 2, figsize=(13, 7), sharex=True)
for ax, ((ind, niv), t) in zip(axs.flat, GENERO.items()):
    for col, c in [('Mujeres', AZUL), ('Varones', NARANJA)]:
        ax.plot(t.index, t[col], color=c, lw=2, marker='o', ms=4, label=col)
    ax.set_title(f'D4 · {ind} en {niv} (%)', loc='left', fontsize=10.5); ax.set_ylim(0)
    ax.axvspan(2019.5, 2021.5, color=NEUTRO, zorder=0)
axs[0, 0].legend(frameon=False, fontsize=9)
for ax in axs[1]: ax.set_xlabel('ciclo lectivo')
fig.tight_layout(); nota(fig, FUENTE_RA + ' Varones = total − mujeres. Franja gris: ciclos 2020–2021 (pandemia).')
guardar(fig, 'D4_ra_genero'); plt.show()
display(pd.concat({f'{ind} {niv}': t for (ind, niv), t in GENERO.items()}, axis=1).round(2))
''')

code(r'''
# D5 · abandono y sobreedad en secundaria por provincia
prov_tra = TRA.assign(provincia=TRA.provincia.map(norm_prov))
ab = por_anio(prov_tra, 'ssp', SEC, por=['provincia', 'anio']).sum(axis=1) / por_anio(prov_tra, 'inicial', SEC, por=['provincia', 'anio']).sum(axis=1)
AB_PROV = (100 * ab).unstack('anio').rename(columns=lambda a: a - 1)
prov_mat = MAT.assign(provincia=MAT.provincia.map(norm_prov))
so = por_anio(prov_mat, 's', SEC, por=['provincia', 'anio']).sum(axis=1) / por_anio(prov_mat, '', SEC, por=['provincia', 'anio']).sum(axis=1)
SOB_PROV = (100 * so).unstack('anio')
assert len(AB_PROV) == 24 and len(SOB_PROV) == 24
AB_PROV = AB_PROV.loc[AB_PROV[AB_PROV.columns[-1]].sort_values(ascending=False).index]

fig, ax = plt.subplots(figsize=(11, 8))
m = AB_PROV.values
im = ax.imshow(m, cmap=SECUENCIAL, aspect='auto', vmin=0, vmax=np.nanmax(m))
ax.set_xticks(range(m.shape[1])); ax.set_xticklabels([str(a)[2:] for a in AB_PROV.columns], fontsize=8)
ax.set_yticks(range(len(AB_PROV))); ax.set_yticklabels(AB_PROV.index, fontsize=8.5)
for (r, q), v in np.ndenumerate(m):
    ax.text(q, r, f'{v:.1f}', ha='center', va='center', fontsize=6.3, color=SUPERFICIE if v > np.nanmax(m) * 0.55 else TINTA)
ax.grid(False); ax.set_xlabel('ciclo lectivo')
for s in ax.spines.values(): s.set_visible(False)
ax.set_title('D5 · Abandono en secundaria por provincia (%), ordenado por el último ciclo', loc='left', fontsize=11)
nota(fig, FUENTE_RA + ' Salidos sin pase / matrícula inicial, años de estudio 7 a 12. Base Trayectoria del año t = ciclo t−1.')
guardar(fig, 'D5_ra_abandono_secundaria_provincias'); plt.show()
print('Sobreedad en secundaria por provincia (% , matrícula del año)')
display(SOB_PROV.round(1))
''')

md(r'''
---
## E · Lectura de resultados (corrida 2026-09-16)

**Criterio general.** Un cambio que aparece **parejo en las 24 provincias** entre dos operativos seguidos suele indicar un
cambio del cuestionario más que del contexto real (lo mismo se vio en el 03). Los cambios que difieren entre provincias,
sectores o ámbitos, o que se sostienen en varios operativos, son más confiables.

**1. Trayectoria: menos repitencia y sobreedad, más jardín desde sala de 3.**
- Repitencia declarada en Primaria 6°: 12,1 % (2016) → 7,1 % (2025), baja en las 24 provincias. 2023 (12,8 %) es un
  valor atípico: la opción "tres veces o más" pesa 2,1 %, contra ≈ 0,5 % en los demás años. En Secundaria, quienes
  repitieron en la primaria bajan de 7,8 % a 5,5 % (2016 → 2024) y en el ciclo básico de 13,1 % a 8,3 % (2019 → 2024).
- Sobreedad en Secundaria 5-6°: 26,3 % → 17,7 % (2019 → 2024), baja en todas las provincias con dato (Río Negro −22 pp).
  El RA muestra lo mismo en todo el sistema: la sobreedad de 7° a 12° año cae a la mitad entre 2011 y 2025 (p. ej.,
  10° año: 41,9 % → 22,6 %) y la de 6° grado pasa de 23,5 % a 5,8 %. **Discrepancia:** en Primaria 6°, la sobreedad de
  APRENDER sube (10,2 % → 12,5 %, 2021 → 2025) mientras la del RA baja; conviene no usar ese indicador de APRENDER hasta
  entender cómo se calcula la edad en 2025.
- Jardín desde sala de 3 o antes: Secundaria 43,4 % (2016) → 57,0 % (2024), sube en las 24 provincias; Primaria 55,0 % →
  61,4 %. **Control de coherencia:** la cohorte de nacimiento de ≈ 2005 responde casi lo mismo en Primaria 2016 (55,0 %) y
  en Secundaria 2022 (55,5 %), seis años después. La brecha urbano−rural se mantiene en ≈ 19–23 pp.

**2. Hogar: mejora el nivel educativo de las familias; libros con cambios de cuestionario.**
- Madre con secundaria completa o más: Secundaria 59,9 % → 66,6 % (2016 → 2024), sube en las 24 provincias. La brecha
  privado−estatal baja de 28,7 a 25,4 pp y la urbano−rural de 26,4 a 21,5 pp.
- En Primaria, el salto 2023 → 2025 (66,2 % → 74,8 %) es **parejo en las 24 provincias** (+6 a +11 pp), igual que la
  caída de "más de 50 libros" (−4 a −9 pp en todas) y la suba de "sin libros" (+2 a +12 pp en todas). Probablemente
  refleja el cuestionario renumerado de 2025: **no leerlo como un cambio real** sin el cuestionario oficial.
- Libros: la serie se corta cuando cambian las opciones. Hasta 2019/2021 existía "No sé" (17–24 %), y después no. En
  Secundaria, "más de 50 libros" pasa de 41,8 % (2019) a 21,9 % (2022), un salto de medición y no de contexto.

**3. Acceso digital: internet casi universal; la computadora retrocede y se amplía la brecha por sector.**
- Internet en el hogar: Secundaria 84,1 % (2017) → 95,5 % (2024), sube en las 24 provincias (San Juan +23 pp); la
  brecha urbano−rural se achica de 23,6 a 9,9 pp. Primaria: 62,7 % (2016) → 80,5 % (2018) y 91,9 % (2023).
- Computadora en el hogar: Secundaria 85,7 % (2017) → 73,5 % (2024); Primaria 76,2 % (2018) → 61,8 % (2023). La brecha
  **privado−estatal se amplía**: de 13,2 a 21,6 pp en Secundaria y de 20,5 a 29,3 pp en Primaria. En Secundaria
  2022 → 2024 cae en 15 provincias (Formosa −12 pp).
- Celular propio: ≈ 96–97 % en Secundaria desde 2016; en Primaria 75,9 % (2016) → 90,9 % (2023).

**4. Trabajo y cuidados: preguntas poco comparables entre años; señales parciales.**
- Secundaria: trabajar para un empleador la semana pasada baja de 19,7 % a 15,6 % (2022 → 2024) **en las 24 provincias**
  (−2 a −6 pp); cuidar familiares sin ayuda se mantiene (39,6 % → 39,5 %).
- Ayudar en el trabajo de familiares es ≈ 12–22 pp más frecuente en el ámbito rural, en ambas cohortes y todos los años.
- En Primaria las cuatro mediciones usan períodos distintos (la semana pasada / habitualmente / frecuencia) y **no forman
  una serie**; 2025 no tiene una pregunta identificable.

**5. RA: menos abandono, varones más rezagados y más egresados de secundaria.**
- Abandono en secundaria: mujeres 3,5 % → 1,1 % y varones 4,4 % → 1,4 % (ciclos 2010 → 2024). Repitencia en secundaria:
  varones 20,6 % → 11,3 % y mujeres 16,2 % → 9,1 %. Los varones repiten y abandonan más en todos los ciclos. Los ciclos
  2020–2021 (promoción acompañada) no son comparables.
- Egresados de secundaria: 247 mil (ciclo 2010) → 462 mil (2024). La proporción de mujeres baja de 59,0 % a 53,3 %: los
  varones reducen la brecha de terminalidad. Los egresados de primaria de 2010–2012 se excluyen porque varias provincias
  informan 0.
- Abandono en secundaria por provincia (ciclo 2024): más alto en Formosa (4,0 %), Santa Fe y Misiones (3,7 %) y Salta
  (3,6 %); 0,4 % en CABA, Buenos Aires, Mendoza y San Luis. En Santa Fe el abandono vuelve a subir (3,3 % en 2023 → 3,7 %
  en 2024) y la sobreedad secundaria también (18,8 % → 23,0 %, 2023 → 2025).
- **Control de calidad:** la sobreedad secundaria de Santa Cruz salta de 6,5 % (2024) a 17,6 % (2025) tras bajar de 51 %
  a 6,5 % en 2011–2024: revisar antes de usar esa provincia.

**Qué no se puede afirmar.** Son descripciones de agregados: no permiten atribuir cambios de desempeño a estos factores
(sin econometría) y, en APRENDER, solo describen a quienes rinden la prueba (en Secundaria, a quienes llegaron al último
año).
''')

md(r'''
---
## F · Descargar gráficos y tablas
Guarda todas las tablas en `contexto_estudiantes.xlsx` dentro de `graficos_contexto/`, comprime la carpeta en un `.zip`
y, en **Colab**, **lo descarga**.
''')
code(r'''
hojas = {'preguntas_por_anio': PREGUNTAS.set_index(['cohorte', 'tema', 'indicador', 'anio'])}
for nombre, t, por in [('pais', PAIS, None), ('sector', POR_SECTOR, 'sector'), ('ambito', POR_AMBITO, 'ambito'), ('provincias', POR_PROV, 'provincia')]:
    idx = ['cohorte', 'orden', 'tema', 'indicador'] + ([por] if por else [])
    hojas[nombre] = t.pivot_table(index=idx, columns='anio', values='pct').droplevel('orden')
for col, br in BRECHAS.items():
    v = br.columns[-1]
    hojas[f'brecha_{col}'] = br.pivot_table(index=['cohorte', 'orden', 'tema', 'indicador'], columns='anio', values=v).droplevel('orden')
for coh, suf in [('Primaria 6°', 'prim'), ('Secundaria 5-6°', 'sec')]:
    hojas[f'cambio_provincias_{suf}'] = pd.concat([CAMBIO_PROV[coh], CAMBIO_PAIS[coh].to_frame().T])
hojas['ra_sobreedad_anio_estudio'] = SOBREEDAD_AE.T.set_axis(ETQ_AE)
hojas['ra_repitencia_anio_estudio'] = REPITENCIA_AE.T.set_axis(ETQ_AE)
hojas['ra_abandono_anio_estudio'] = ABANDONO_AE.T.set_axis(ETQ_AE)
hojas['ra_egresados'] = EGRESADOS
hojas['ra_genero'] = pd.concat({f'{ind} {niv}': t for (ind, niv), t in GENERO.items()}, axis=1)
hojas['ra_abandono_sec_provincias'] = AB_PROV
hojas['ra_sobreedad_sec_provincias'] = SOB_PROV
ruta_xlsx = os.path.join(GRAF, 'contexto_estudiantes.xlsx')
with pd.ExcelWriter(ruta_xlsx, engine='openpyxl') as xw:
    for nombre, t in hojas.items():
        t = t.copy()
        if isinstance(t.columns, pd.MultiIndex):
            t.columns = [' | '.join(map(str, c)) for c in t.columns]
        num_cols = t.select_dtypes('number').columns
        t[num_cols] = t[num_cols].round(3)
        t.to_excel(xw, sheet_name=nombre[:31])
print('Archivos a descargar:')
for n in sorted(os.listdir(GRAF)): print('  -', n)
zip_path = shutil.make_archive(os.path.join(os.path.dirname(GRAF), 'graficos_contexto'), 'zip', GRAF)
print('\nZIP:', zip_path, f'({os.path.getsize(zip_path)/1e6:.1f} MB)')
if in_colab():
    from google.colab import files
    files.download(zip_path)
    print('Descargando el zip...')
else:
    print('Entorno local: los archivos quedan en', GRAF)
''')

# ----------------------------------------------------------------------------------------------------------------------
def construir():
    nb = new_notebook()
    nb.metadata = {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                   'language_info': {'name': 'python'}, 'colab': {'provenance': []}}
    for tipo, src in CELDAS:
        nb.cells.append(new_markdown_cell(src) if tipo == 'md' else new_code_cell(src))
    # Bootstrap de Colab igual que el 03: el primer bloque de código ya monta Drive; no clona el repo (no lo necesita)
    nbformat.validate(nb)
    return nb

if __name__ == '__main__':
    if '--debug' in sys.argv:
        import matplotlib; matplotlib.use('Agg')
        os.chdir(R)
        ns = {'display': lambda x: print(x.to_string()[:3000] if hasattr(x, 'to_string') else x)}
        hasta = int(sys.argv[sys.argv.index('--hasta') + 1]) if '--hasta' in sys.argv else 10**6
        n = 0
        for tipo, src in CELDAS:
            if tipo != 'code': continue
            n += 1
            if n > hasta: break
            print(f'\n======== celda de código {n}')
            exec(compile(src, f'celda{n}', 'exec'), ns)
        if '--post' in sys.argv:
            exec(open(sys.argv[sys.argv.index('--post') + 1], encoding='utf-8').read(), ns)
    else:
        nb = construir()
        nbformat.write(nb, os.path.join(R, '04_contexto.ipynb'))
        print('escrito', len(nb.cells), 'celdas')
