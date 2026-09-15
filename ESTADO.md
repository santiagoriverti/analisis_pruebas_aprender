# ESTADO DEL PROYECTO — análisis_pruebas_aprender

> Documento de traspaso (handoff). Sirve para **retomar el proyecto en otra sesión o en otra PC**
> sin perder contexto. Última actualización: **2026-09-15** (sesión 14).
> Para Claude Code: ver también [`CLAUDE.md`](CLAUDE.md) y [`.claude/memory/project.md`](.claude/memory/project.md).

---

## 1. Resumen

Consolidación y análisis **descriptivo** de las **Pruebas APRENDER** (evaluación, 2016–2025) y la **estadística
educativa RA** (Relevamiento Anual, 2011–2025) de la Secretaría de Educación de la Nación (Argentina).
Cuatro notebooks, todos ejecutables en Google Colab (00–02 **validados en Colab**; 03 validado en local):

| Notebook | Qué hace | Salida |
|---|---|---|
| `00_consolidacion.ipynb` | Cataloga 156 `.xlsx`, arma el diccionario maestro y consolida RA (ancho) + APRENDER (largo) | `datos_consolidados/` y, en Colab, *Mi unidad/`pruebas_aprender`* |
| `01_analisis.ipynb` | Trayectorias RA (matrícula, repitencia, abandono, cargos) + desempeño APRENDER por cohorte + catálogo de variables | `graficos_trayectorias.zip` (7 gráficos + `variables_disponibles.xlsx/.txt`) |
| `02_brechas.ipynb` | Brechas de desempeño APRENDER por sector, ámbito y provincia | `graficos_brechas.zip` (8 gráficos + `brechas_aprender.xlsx`) |
| `03_provincias.ipynb` | Evolución provincial en los dos últimos operativos, comparación con provincias de nivel inicial similar y cambios de contexto asociados | `graficos_provincias.zip` (5 gráficos + `provincias_contexto.xlsx`) |

- **Remoto:** https://github.com/santiagoriverti/analisis_pruebas_aprender (rama `main`)
- **Local (PC INECO):** `C:\Users\sriverti\Desktop\INECO\Repositorios\analisis_pruebas_aprender`
- **Datos consolidados en Drive:** *Mi unidad/`pruebas_aprender`* (`parquet/` + `excel/` + `catalogo_archivos.csv`)
- **Enfoque acordado con el usuario:** descriptivo, **sin econometría**.

## 2. Estado actual

| Componente | Estado |
|---|---|
| `00_consolidacion.ipynb` — consolidación + diccionario maestro + verificación (firma) + guardado en Drive | ✅ local y Colab |
| Nivel/grado de archivos 2016–2018 completados (control por edad modal con assert) | ✅ |
| **Datos del Drive** re-consolidados en Colab y **auditados**: 57 parquet, 14 tablas de `excel/` y catálogo idénticos al local | ✅ 2026-09-14 |
| `01_analisis.ipynb` — trayectorias RA + cohortes APRENDER + catálogo de variables (sin truncar) | ✅ local y Colab (re-validado 2026-09-14 con orden de opciones determinístico: `variables_disponibles` idéntico) |
| `02_brechas.ipynb` — brechas por sector, ámbito, sector × ámbito y provincia | ✅ local y Colab (8 hojas de `brechas_aprender.xlsx` idénticas, 2026-09-14) |
| `03_provincias.ipynb` — evolución provincial reciente (Prim 2023→2025, Sec 2022→2024) + contexto | ✅ local (2026-09-15; pendiente correrlo en Colab) |
| Documentación: README, CONTEXTO, ESTADO, CLAUDE.md, memoria | ✅ |
| Notebook 04 (contexto del estudiante en el tiempo) · brechas por NSE con microdatos 2024 · más RA · informe | ⏳ próximos pasos (§8) |

**Firma de referencia de la consolidación: `bdedd07f319c`**
Si al correr el 00 la `firma` da ese valor, los datos compilaron idénticos y sin errores. Incluye los operativos
APRENDER `(año, cobertura, nivel, grado)`. Verificada en local (Py 3.14 / pandas 2.3) y en Colab (Py 3.13 / pandas 2.2).
La firma histórica `c9740263478b` corresponde a la consolidación vieja (grado "No especificado" en 2016–2018): si
aparece, el Drive está desactualizado → re-correr el 00.

## 3. Cómo retomar

### 3.1 Uso normal (Google Colab, sin instalar nada)
Abrir el badge del notebook en el README → *Entorno de ejecución → Ejecutar todo* → autorizar Drive.
- **00:** se corre **una sola vez** (clona el repo, consolida ~5 min, imprime la verificación y guarda en Drive).
- **01, 02 y 03:** solo **montan el Drive y leen** (no reconsolidan). Son independientes entre sí.
- **Re-correr el 00 solo si:** (1) se borró/movió *Mi unidad/`pruebas_aprender`*; (2) se agregan datos a
  `resultados_aprender/`; (3) cambia la lógica de consolidación. El guardado reemplaza `parquet/ra` y
  `parquet/aprender_long` completos y sobrescribe el resto: **no hay que tocar nada a mano en el Drive**.
- Colab **corta la salida de una celda a ~5.000 líneas**: por eso el listado de variables del 01 se imprime por partes.

### 3.2 En una PC nueva (local)
```bash
git clone https://github.com/santiagoriverti/analisis_pruebas_aprender.git
cd analisis_pruebas_aprender
pip install -r requirements.txt          # pandas, pyarrow, openpyxl, python-calamine, matplotlib, jupyter, pyreadstat
python -m jupyter nbconvert --to notebook --execute --inplace 00_consolidacion.ipynb --ExecutePreprocessor.timeout=1800
python -m jupyter nbconvert --to notebook --execute --inplace 01_analisis.ipynb --ExecutePreprocessor.timeout=1800
python -m jupyter nbconvert --to notebook --execute --inplace 02_brechas.ipynb --ExecutePreprocessor.timeout=1800
python -m jupyter nbconvert --to notebook --execute --inplace 03_provincias.ipynb --ExecutePreprocessor.timeout=1800
```
- Los datos crudos (`resultados_aprender/`, 156 `.xlsx`) **están versionados**: el clone los trae.
- **No** se versionan `Base_publica_Ap2024.sav` (117 MB, supera el límite de GitHub) ni la salida pesada
  (`datos_consolidados/ra/`, `aprender_long/`, `*.parquet`) ni las carpetas/zips de gráficos.
- **Motor de lectura obligatorio:** `python-calamine` (openpyxl no termina de leer los APRENDER de 1000+ columnas).
- Tiempos locales: 00 ≈ 5 min · 01 ≈ 2,5 min · 02 ≈ 20 s · 03 ≈ 40 s. En local, 01, 02 y 03 leen de `datos_consolidados/`.

## 4. Dónde quedan los resultados

- **Local:** `datos_consolidados/` (regenerable) · `graficos_trayectorias/` + `.zip` (01) · `graficos_brechas/` + `.zip` (02) · `graficos_provincias/` + `.zip` (03).
- **Drive** (*Mi unidad/`pruebas_aprender`*, lo escribe el 00 en Colab):
  - `parquet/` → `ra/ra_<base>.parquet` (7), `aprender_long/anio=YYYY/` (48 archivos), `diccionario_ra/aprender.parquet`.
    **Es lo que leen el 01, el 02 y el 03.**
  - `excel/` → `diccionario_maestro.xlsx`, `ra_<base>.xlsx` (≤200k filas), `ra_cargos_bis.csv`,
    `ra_matricula_por_edad.csv`, `aprender_desempenos.xlsx` (109.473 filas).
  - `catalogo_archivos.csv`.
- **Descargas de Colab:** `graficos_trayectorias.zip` (01), `graficos_brechas.zip` (02) y `graficos_provincias.zip` (03).

## 5. Modelo de datos

- **RA → ancho.** 7 parquet (uno por base), años 2011–2025 apilados en `anio`.
  Claves: `provincia, departamento, sector, ambito` (+ `nivel/tipo/categoria/cargo/planta_tipo` en Cargos Bis;
  `grado` en Matrícula por edad). Valores = **conteos absolutos**.
- **APRENDER → largo/tidy.** Particionado por `anio`. Columnas: `cobertura, nivel, grado, area, jurisdiccion,
  departamento, sector, ambito, variable, tipo_variable, valor`. Valores = **conteos ponderados de estudiantes**.
  `tipo_variable ∈ {desempeño, contexto, nse, nivel_educativo_hogar, otro}`. `variable` = `código_opción`.
- **Diccionario maestro** (`diccionario_maestro.xlsx`, hojas Notas, Catalogo, Diccionario_RA, Diccionario_APRENDER,
  Indice_RA, Indice_APRENDER). El catálogo tiene la columna `nivel_grado_inferido`.
- **Catálogo legible de variables:** `variables_disponibles.xlsx` (lo genera el 01): RA 744 columnas, APRENDER
  5.571 variables / 1.591 preguntas, con años de disponibilidad y significado.

### Operativos APRENDER (tras la corrección de grado)
| Año | Censal | Muestral |
|---|---|---|
| 2016 | Primaria 6 grado (Lengua, Mat) · Secundaria 5-6 año (Lengua, Mat, Cs. Nat., Cs. Soc.) | Primaria 3 grado · Secundaria 2-3 año |
| 2017 | Primaria 6 grado (Cs. Nat., Cs. Soc.) · Secundaria 5-6 año (Lengua, Mat) | — |
| 2018 | Primaria 6 grado (Lengua, Mat) | — |
| 2019 | Secundaria 5-6 año (Lengua, Mat) | Secundaria 5-6 año (Cs. Nat., Ciudadanía) |
| 2021 | Primaria 6 grado | — |
| 2022 | Secundaria 5-6 año | Primaria 6 grado |
| 2023 | Primaria 6 grado | — |
| 2024 | Secundaria 5-6 año | Primaria 3 grado (Lengua) |
| 2025 | Primaria 6 grado | — |

**Cohortes comparables** (misma nivel/grado/cobertura, escala de 4 niveles):
**Primaria 6° Censal 2016 · 2018 · 2021 · 2023 · 2025** y **Secundaria 5-6° Censal 2016 · 2017 · 2019 · 2022 · 2024**.

### Métricas de referencia (chequeo rápido)
- RA: Matrícula por edad 300.333×44 · Matrícula 18.020×105 · Cargos Bis 1.464.119×11 · Cargos 18.426×61 ·
  Características 18.021×74 · Población 18.017×170 · Trayectoria 17.912×317.
- APRENDER largo: **18.721.597 filas** (2016:3.788.601 · 2017:2.971.268 · 2018:1.079.294 · 2019:2.333.376 ·
  2021:1.740.100 · 2022:2.175.201 · 2023:1.776.906 · 2024:1.711.855 · 2025:1.144.996).
- Diccionarios: `dic_ra` 701×4 · `dic_ap` 10.775×7. `cargos_bis_total_2024 = 11.208.635,0` (suma de TODOS los tipos).
- % Satisf+Avanz total país (01 y 02 deben coincidir):
  - Primaria 6° Lengua 66,8 / 75,3 / 70,9 / 66,4 / 76,9 · Matemática 58,5 / 57,4 / 55,5 / 51,4 / 55,0
  - Secundaria 5-6° Lengua 53,6 / 62,5 / 61,8 / 56,9 / 56,9 · Matemática 29,8 / 31,1 / 28,7 / 17,6 / 17,6

## 6. Trampas conocidas (gotchas)

**Datos RA**
- **Cargos Bis: `total` mezcla unidades según `tipo`** (Cargos, Cargos Suplentes, Cargos No Docentes, Horas, Horas
  Suplentes, Módulos, Módulos Suplentes). Sumar todo da ~11,2 M (2024); los **cargos docentes son 882.824**.
  Filtrar SIEMPRE por `tipo` (y `strip()` a `tipo`/`nivel`). `tipo == 'Cargos'` no tiene subtotales.
- **Base Trayectoria: el relevamiento del año *t* informa el ciclo lectivo *t−1*** (inicial de Trayectoria(*t*) ≈
  Matrícula(*t−1*) en todos los años; 2021: −0,6% vs −2,5%). La caída de repitencia de "RA 2021" es el **ciclo 2020**.
- **Matrícula:** `s2` = sala de 2 años y `s_2` = sobreedad en 2° año → no normalizar nombres quitando `_`.
- **Características / Población:** muchas columnas numéricas quedaron como texto (vacíos `''`) → `pd.to_numeric(errors='coerce')`.
- `Departamento` capitalizado en 2024 → normalizado en `_norm_keys()`. Cargos Bis: 7 filas con `ambito` nulo (origen).
- **Jornada completa/extendida (Población) por provincia: inconsistente entre años** (saltos de decenas de pp, Santa Fe
  113 % en 2025, Santa Cruz 97 %→1 %) → no usar como indicador (03, sección G).

**Datos APRENDER**
- **Nivel/grado ausentes en el nombre (2016–2018):** el 00 los completa (2016/2017 Primaria `6 grado`, Secundaria
  `5-6 año`; 2018 Primaria `6 grado`; `3grado`→`3 grado`). Evidencia: edad modal (pregunta 1): 11→6°, 17→5-6°, 8→3°,
  14→2-3°; assert en la sección 8 del 00. Sin "Censal/Muestral" en 2016–2018 = Censal (diccionario: "Estudiantes").
- **Nivel socioeconómico NO se puede cruzar con desempeño** en las bases agregadas: vienen como conteos separados por
  celda (jurisdicción × departamento × sector × ámbito), sin distribución conjunta. Solo con microdatos.
- **Microdatos solo en 2024** (`.sav`, detalle en `CONTEXTO.md` §9): Secundaria 5-6° censal (386.882 alumnos × 22 var.,
  sin etiquetas SPSS, **sin NSE**) y Primaria 3° muestral (91.264 × 24, con `NSE_escuela`). Puntajes y ponderadores con
  ruido (SDC) y <10 % de códigos de colegio reasignados. % ponderados verificados = agregados. Leer con `pyreadstat`.
- **Matemática Secundaria 2022:** `mdesemp_Avanzado` viene vacía en la fuente (no hay Avanzado ese año).
- **Secundaria 2022 vs 2024:** % Satisf+Avanz casi idénticos (56,94/56,89; 17,64/17,63) — coincidencia real, no duplicado.
- **Chubut sin datos en Secundaria 2019** (23 provincias).
- **Nombres de provincia cambian entre años** (" Buenos Aires", "Buenos aires", "Ciudad de Buenos Aires",
  "Tierra del Fuego, Antártida…") → `norm_prov()` en el 02 y el 03.
- **Sin diccionario 2025:** 102 variables 2025 toman el texto del diccionario del año más cercano (los códigos pueden
  cambiar de pregunta entre años).
- **Cuestionario Primaria 2025 renumerado:** jardín `ap06`, repitencia `ap07`, tiempo de viaje `ap09`, libros `ap24` y
  autopercepción `ap40a–c` se identificaron por opciones y distribución; **no hay preguntas de clima identificables**.
  En Secundaria 2022→2024 varias preguntas cambian período o escala ("te molestaron": 3 meses → año; formas de
  resolver conflictos): comparar provincias entre sí, no niveles (03, sección D).
- Sin columna `departamento` en algunos archivos (~240.946 filas nulas, esperado). `tipo_variable='otro'` ~11% (catch-all).
- Irregularidades de nombres: dobles espacios (`Muestral  -`), `.csv.xlsx` (2024 Prim 3° Solo CC). 2020 sin APRENDER.

**Herramientas**
- **Colab trunca la salida de una celda a ~5.000 líneas.**
- pandas `plot(style=dict, color=...)` falla si los **nombres de columnas** contienen letras de color → usar `ax.plot` por serie.
- `str.split(pat, n=1)` requiere `n=` como keyword.
- **pyarrow `Table.group_by` con hilos no garantiza el orden de salida** (cambia entre corridas y entornos). Si el orden
  importa, usar archivos en orden fijo + `group_by(..., use_threads=False)` y `sort_values(..., kind='stable')`
  (así se arregló el orden de `opciones` del catálogo del 01, que difería entre local y Colab).

## 7. Notebooks de análisis

### 7.1 `01_analisis.ipynb` — trayectorias (38 celdas)
- **Setup/funciones:** `cargar_ra`, `cargar_aprender`, `cargar_desempeno`, `suma_anios`+`tasa` (`PRIM=1-6`, `SEC=7-12`),
  `a_ciclo_lectivo` (Trayectoria t → ciclo t−1), `estilo_total`, `nota`, `harmonizar_nivel`+`ORDEN4`, `desempeno_pct`,
  `serie_cohorte`, `ANIOS_PRIM6=[2016,2018,2021,2023,2025]`, `ANIOS_SEC56=[2016,2017,2019,2022,2024]`.
- **Sección 2:** mapa de comparabilidad (nivel, grado, cobertura, área) × año.
- **A (RA):** A1 matrícula inicial por nivel · A2 repitencia y abandono (por ciclo lectivo, franja pandemia) ·
  A3 cargos docentes por nivel (`tipo=='Cargos'`, 632 mil 2011 → 890 mil 2025) + tabla por tipo · A4 horas y módulos.
- **B (APRENDER):** B1 Primaria 6° y B2 Secundaria 5-6° (% por nivel, Lengua/Mat) · B3 % Satisf+Avanz por sector (Prim 6° Mat).
- **C:** catálogo de variables → `variables_ra`, `variables_aprender`, `preguntas_aprender`, `buscar_variable(texto)`;
  guarda `variables_disponibles.xlsx/.txt`. **D:** zip + descarga. **E.1–E.5:** listado impreso por partes
  (500 / 134 / 2.284 / 2.216 / 785 líneas).

### 7.2 `02_brechas.ipynb` — brechas (21 celdas)
- **Funciones:** `COHORTES`, `cargar_cohorte` (filtro pyarrow por partición), `indicadores(df, por)`, `norm_prov`/`PROV_ALIAS`.
- **A** total país · **B** sector (B1 líneas, B2 brecha pp privado−estatal) · **C** ámbito (C1, C2 brecha urbano−rural)
  + tabla sector × ámbito · **D** provincias (D1/D2 heatmaps, D3 cambio primer→último año, D4 dispersión: rango y desvío)
  · **E** nota NSE · **F** `brechas_aprender.xlsx` (8 hojas) + zip.
- **Hallazgos:** brecha privado−estatal estable ~20–27 pp en las 4 series; Primaria rural ≈ urbano (Matemática estatal:
  rural > urbano todos los años); Secundaria urbano−rural ~16 pp en Lengua y ~8 pp en Matemática (2024); CABA primera
  siempre, Chaco/Catamarca últimas en Primaria; Matemática Secundaria cae en todas las provincias 2016→2024 (−1 a −23 pp)
  y la dispersión baja de 41 a 27 pp **por piso**, no por convergencia.

### 7.3 `03_provincias.ipynb` — evolución provincial y contexto (26 celdas)
- **Período:** dos últimos operativos (Primaria 6° 2023→2025, Secundaria 5-6° 2022→2024); % Satisf+Avanz.
- **Secciones:** A cambio por provincia (A1) · B convergencia: ρ con nivel inicial y terciles (B1) · C cambio frente a
  provincias del mismo tercil de nivel inicial + consistencia en las 4 series (C1) · D indicadores de contexto
  emparejados (`SPECS`: 11 Prim + 28 Sec del cuestionario CC, más 5 del RA por cohorte; `pct()` con asserts de opciones) ·
  E 8 que más vs 8 que menos mejoran + ρ (E1/E2) · F fichas frente al país · G control de calidad (jornada RA descartada) ·
  H lectura · I `provincias_contexto.xlsx` + zip.
- **Hallazgos:** Lengua Prim mejora 24/24 (+7,3 a +13,9), Mat Prim 22/24, Lengua Sec 10/24, Mat Sec 16/24 (no todas).
  Convergencia: ρ −0,59 Lengua Prim, −0,48 Mat Sec, −0,37 Lengua Sec, −0,21 Mat Prim. Frente a pares: Entre Ríos, La Pampa
  y Chubut por encima en 4/4; Neuquén (−4,0 pp), Tucumán y Santiago del Estero por debajo en 4/4; Córdoba en 3/4.
  Contexto: en Primaria no hay señal robusta (jardín desde sala de 3 como hipótesis); en Secundaria pesa la composición
  del hogar de quienes rinden (libros ρ +0,57 en Mat), la repitencia del RA sube donde mejoran (Neuquén, opuesto) y el
  clima escolar no acompaña. Asociaciones entre 24 provincias, **no causales**.

**Regla de comparabilidad:** RA = series de tiempo válidas; APRENDER = solo dentro de la misma
`(nivel, grado, cobertura)`. Escala de desempeño homogénea (4 niveles) salvo Primaria 3° 2024.

## 8. Próximos pasos

1. **Usuario:** correr `03_provincias.ipynb` en Colab y pasar `graficos_provincias.zip` para validarlo contra local
   (00–02 ya validados). Luego, **indagar con fuentes externas** las hipótesis del 03 (sección H): participación en
   APRENDER por provincia, régimen académico en secundaria, días de clase y conflictos docentes, sala de 3 y planes de
   alfabetización; y medir con los microdatos 2024 cuánto pesa la composición del hogar.
2. **Notebook 04 · contexto del estudiante en el tiempo** (prioridad sugerida, selección en `CONTEXTO.md` §10): APRENDER
   A1–A6 (repitencia, jardín, educación de madre/padre, libros, conectividad del hogar, trabajo y cuidados) dentro de cada
   cohorte por provincia/sector/ámbito + RA C1–C4 (sobreedad, egresados, abandono/repitencia por año de estudio, brecha de género).
3. **Brechas por NSE / contexto con microdatos 2024** (`CONTEXTO.md` §9 y §10.D): Primaria 3° × `NSE_escuela`, jardín,
   libros; Secundaria × educación de la madre, libros, computadora (sin NSE propio). `Base_publica_Ap2024.sav` (117 MB)
   está **solo en la PC local** (no en GitHub/Colab). Solo una foto 2024.
4. **Más RA** (`CONTEXTO.md` §10.C5–C11): nivel inicial, jornada extendida, comedor, conectividad escolar, migrantes,
   discapacidad, vacancia docente, plurigrado; y fotos puntuales de APRENDER (§10.B: pandemia, salud mental, apuestas online).
5. **Informe** (Word/presentación) con gráficos y tablas de 01, 02 y 03.
6. (Opcional) Cruce RA↔APRENDER por geografía (~271 deptos matchean; requiere crosswalk). **Sin econometría.**
7. (Opcional) Afinar la clasificación `tipo_variable == 'otro'`.

## 9. Convenciones del proyecto

- Idioma de trabajo: **español**.
- Commits: **solo** con el usuario Santiago Riverti, **sin** `Co-Authored-By` ni atribución de Claude.
- Datos crudos versionados; salida pesada y gráficos regenerables en `.gitignore`.
- Los notebooks versionados se guardan **ejecutados** (con salidas) tras correrlos localmente con `nbconvert`.
- Gráficos nuevos: paleta validada (fondo claro, grilla recesiva; azul/rojo para cambios, azul/naranja para Lengua/Matemática),
  PNG a 300 dpi con nota de fuente, y siempre una tabla con los valores al lado.
- Antes de dar un resultado por bueno, **verificarlo contra los datos** (así se detectaron el error de Cargos Bis,
  el desfase del ciclo lectivo y el grado 2016–2018).

## 10. Bitácora de sesiones

| Sesión | Fecha | Qué se hizo |
|---|---|---|
| 1 | 2026-08-31 | Setup: README, .gitignore (excluye .sav 117 MB), CONTEXTO, memoria. |
| 2 | 2026-08-31 | `00_consolidacion.ipynb`: catálogo + diccionario maestro + consolidación (calamine). |
| 3 | 2026-08-31 | Colab (badge + bootstrap), celda de verificación (firma), guardado en Drive (parquet + excel). |
| 4 | 2026-08-31 | Auditoría de los datos descargados del Drive (firma `c9740263478b`); documentación de traspaso. |
| 5 | 2026-08-31 | `01_analisis.ipynb`: trayectorias descriptivas (sin econometría, por pedido del usuario). |
| 6 | 2026-08-31 | 01: línea Total, gráficos a 300 dpi + zip, badges de Colab. Flujo: 00 una vez → Drive; 01 solo lee. |
| 7 | 2026-09-11 | Revisión del 01 contra los datos: **A3 corregido** (Cargos Bis mezclaba unidades) + A4; A1/A2 por **ciclo lectivo**; nota Avanzado 2022; listado de variables. |
| 8 | 2026-09-11 | 00: **nivel/grado 2016–2018** completados (assert por edad modal), `nivel_grado_inferido`; firma con operativos → **`bdedd07f319c`**. 01: cohortes ampliadas. |
| 9 | 2026-09-11 | Usuario re-corrió 00 y 01 en Colab (firma OK); **Drive auditado** (0 diferencias). Colab truncó el listado → 01 secciones C/D/E + `variables_disponibles.xlsx/.txt`. |
| 10 | 2026-09-11 | Nuevo **`02_brechas.ipynb`**: sector, ámbito, sector × ámbito, provincias + `brechas_aprender.xlsx`. NSE no cruzable (documentado). |
| 11 | 2026-09-11 | Traspaso: ESTADO reescrito, `CLAUDE.md` creado, memoria de proyecto reorganizada, CONTEXTO y README de datos actualizados. |
| 12 | 2026-09-14 | Usuario corrió 00, 01 y 02 en Colab. **Validación completa** contra local: firma OK, 57 parquet + 14 tablas Excel/CSV del Drive y catálogo idénticos, tablas del 01/02 y `brechas_aprender.xlsx` idénticos. Única diferencia: orden de `opciones` en `variables_disponibles` (group_by de pyarrow con hilos) → **01 corregido** (orden determinístico) y re-ejecutado en local (27/30 celdas sin cambios; 3 del listado: mismo contenido). Re-corrido en Colab: `variables_disponibles` **idéntico** al local. |
| 13 | 2026-09-14 | Exploración de microdatos 2024 (`pyreadstat`): contenido, anonimización y control de % ponderados = agregados. Comparación de riqueza de datos por año (2024 no es el más rico; solo suma microdatos). Selección de **variables de interés** para desarrollar → `CONTEXTO.md` §9–§10; próximos pasos reordenados (notebook 03). |
| 14 | 2026-09-15 | Análisis provincial pedido por el usuario (4 afirmaciones): corresponden a los dos últimos operativos; la 4 no se cumple (Mat Sec 16/24). Convergencia, comparación con pares, contexto emparejado (Primaria 2025 sin diccionario: códigos deducidos), jornada RA descartada. Nuevo **`03_provincias.ipynb`** ejecutado y validado en local contra el análisis exploratorio (Δ vs 02 máx 0,009 pp; ρ máx 0,02). |
