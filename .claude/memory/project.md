# Memoria de proyecto — análisis_pruebas_aprender

> Archivo de memoria para sesiones de Claude Code. Resume estado, decisiones y pendientes.
> Autor/usuario: Santiago Riverti. Los commits van solo con su usuario (sin atribución de Claude).

---

## Qué es

Repositorio de consolidación y análisis de las **Pruebas APRENDER** y la **estadística
educativa** de la Secretaría de Educación de la Nación (Argentina), 2011–2025.

- Local: `C:\Users\sriverti\Desktop\INECO\Repositorios\analisis_pruebas_aprender`
- Remoto: https://github.com/santiagoriverti/analisis_pruebas_aprender
- Rama principal: `main`

## Estado actual (2026-09-11)

> **Para retomar en otra PC/sesión: leer `ESTADO.md`** (handoff completo: instalación, ejecución,
> dónde quedan los resultados, métricas de referencia, gotchas y próximos pasos).
> **Firma de referencia de la consolidación: `bdedd07f319c`** (2026-09-11, incluye operativos con grado
> corregido; la anterior `c9740263478b` era con grado "No especificado" en 2016–2018).

- Repo con documentación + **notebook 00 de consolidación funcionando end-to-end y validado**.
- Trabajo sesión 1 (setup):
  - `.gitignore`, `README.md`, `CONTEXTO.md`, `.claude/memory/project.md`.
  - `.sav` de 117 MB excluido de git.
- Trabajo sesión 2 (consolidación):
  - `00_consolidacion.ipynb` (18 celdas): cataloga 156 xlsx, arma diccionario maestro y
    consolida en `datos_consolidados/`. Corre en ~4 min con motor `calamine`.
  - `requirements.txt` (pandas, pyarrow, openpyxl, python-calamine, jupyter).
  - Salida pesada regenerable en `.gitignore`; se versionan `diccionario_maestro.xlsx` y
    `catalogo_archivos.csv` + `datos_consolidados/README.md`.
- Trabajo sesión 3 (Colab + Drive):
  - Badge "Open in Colab" en README; celda 0 de bootstrap (clona repo en Colab).
  - Celda 9 de verificación con firma reproducible. **Firma de referencia: `c9740263478b`**
    (coincidió en Colab con Python/pandas/pyarrow distintos → consolidación determinística).
  - Celda 10: al correr en Colab, monta Drive y guarda en **Mi unidad/pruebas_aprender**:
    `parquet/` (para notebook 01) + `excel/` (legible). Función `exportar_resultados(origen, destino)`.
    Umbral xlsx/csv = 200k filas (Cargos Bis y Matricula por edad → CSV; resto xlsx;
    APRENDER completo solo en parquet, su parte legible = `aprender_desempenos.xlsx`, 109.473 filas).
- Trabajo sesión 4 (auditoría + traspaso):
  - Auditados los parquet descargados del Drive → íntegros; firma recomputada = `c9740263478b`.
  - Chequeos: RA shapes OK; APRENDER 18.721.597 filas, `valor` sin nulos ni negativos;
    departamento nulo 240.946 (esperado); Cargos Bis 7 filas con ambito nulo (del origen).
  - Creado `ESTADO.md` (handoff). README/memoria actualizados. Todo commiteado y pusheado.
- Trabajo sesión 5 (notebook 01 = TRAYECTORIAS):
  - **El usuario pidió trayectorias descriptivas, NO econometría.** Se reenfocó el notebook (se sacó
    el cruce RA↔APRENDER con correlación/scatter). `01_analisis.ipynb` = 22 celdas, 0 errores, 6 gráficos.
  - Marco de **comparabilidad**: RA = series de tiempo (2011-2025); APRENDER = solo dentro de la
    misma `(nivel, grado, cobertura)`. Cohortes: Primaria 6° Censal (2021/23/25), Secundaria 5-6°
    Censal (2019/22/24). Escala 4 niveles salvo Primaria 3° 2024 (Lector/Nivel I-V).
  - Trayectorias RA (desde base *Trayectoria*): matrícula inicial por nivel (`inicial_X`), tasa de
    repitencia (`nopromo_X/inicial_X`), abandono (`ssp_X/inicial_X`), cargos (*Cargos Bis* `total`).
    Rangos año de estudio: PRIM=1-6, SEC=7-12. Datos: repitencia sec 18,3%(2011)→10,2%(2025);
    matrícula sec 3,6M→4,2M; cargos 8,2M→11,2M.
  - Trayectorias APRENDER: `serie_cohorte()` + `desempeno_pct()`; % por nivel y por sector.
  - Funciones: `cargar_ra/aprender/desempeno`, `suma_anios`+`tasa`, `harmonizar_nivel`+`ORDEN4`,
    `desempeno_pct(df,group)`, `serie_cohorte`.
  - Gotcha pandas: `str.split(pat, n=1)` requiere `n=` keyword. (El cruce geográfico quedó probado
    aparte: norm_geo + CROSSWALK_PROV {CABA, TdF}; ~271 deptos matchean — guardado para más adelante.)
  - Agregado: trayectoria **Total** (línea negra punteada) en gráficos RA; `guardar(fig, nombre)` que
    exporta cada gráfico a **300 dpi** en `graficos_trayectorias/`; celda final que zippea y (en Colab)
    descarga con `google.colab.files.download`. Badges de Colab de ambos notebooks en README.
    `graficos_trayectorias/` y `.zip` en `.gitignore`.

- Trabajo sesión 7 (2026-09-11, revisión de resultados del 01):
  - **Bug corregido A3:** sumaba `total` de Cargos Bis sin filtrar `tipo` (mezcla cargos/horas/módulos/suplentes/
    no docentes → 11,2 M). Ahora cargos docentes por nivel (`tipo=='Cargos'`, 882.824 en 2024) + A4 horas/módulos.
  - **Trayectoria RA(t) = ciclo lectivo t−1** (verificado: inicial de Trayectoria(t) ≈ Matrícula(t−1)). A1/A2
    rotulados por ciclo lectivo con `a_ciclo_lectivo()`; la caída de repitencia es el ciclo 2020 (pandemia).
  - Sec. 5-6° 2022≈2024 en % Satisf+Avanz es coincidencia real (no duplicado). Mat. 2022 sin Avanzado en la fuente.
  - Nueva **sección D**: listado completo de variables (RA 744 cols; APRENDER 5.571 vars / 1.591 preguntas) +
    `buscar_variable()`. Distintos desde pyarrow `group_by().aggregate([])` para velocidad.
  - Gotchas: pandas `plot(style=dict, color=...)` falla si los NOMBRES de columnas contienen letras de color
    (itera las claves del dict) → usar `ax.plot` por serie. Matrícula `s2` (sala) vs `s_2` (sobreedad): no
    normalizar quitando `_`. RA Características/Población tienen números como texto.
  - Notebook editado con `nbformat` y ejecutado con `python -m jupyter nbconvert --execute --inplace` (~2,5 min).

- Trabajo sesión 8 (2026-09-11, grado 2016–2018):
  - 00: `parse_nombre_aprender` (lo que dice el nombre) + `parse_aprender` completa con `NIVEL_SIN_NOMBRE` /
    `GRADO_SIN_NOMBRE` (2016/17 Prim 6 grado, Sec 5-6 año; 2018 Prim 6 grado); `3grado`→`3 grado`.
  - Evidencia = edad modal de la pregunta 1 (ap1/Ap1): 11→6°, 17→5-6°, 8→3°, 14→2-3°. Assert en sección 8.
  - Firma ahora incluye `operativos` → **`bdedd07f319c`**. Filas/columnas iguales.
  - 01: cohortes `ANIOS_PRIM6=[2016,2018,2021,2023,2025]`, `ANIOS_SEC56=[2016,2017,2019,2022,2024]`.
    % Satisf+Avanz: Prim 6° Lengua 66.8/75.3/70.9/66.4/76.9, Mat 58.5/57.4/55.5/51.4/55.0;
    Sec 5-6° Lengua 53.65/62.53/61.76/56.94/56.89, Mat 29.81/31.13/28.66/17.64/17.63.

- Trabajo sesión 9 (2026-09-11): Drive auditado tras re-correr el 00 en Colab (0 diferencias). **Gotcha Colab:
  la salida de una celda se trunca a ~5.000 líneas** → el listado de variables se imprime en 5 celdas (E.1–E.5)
  y se guarda completo en `variables_disponibles.xlsx/.txt` dentro del zip. Editar notebooks con scripts en
  archivo (no heredoc sin comillas: bash come los backticks y los `\n`).

## Arquitectura de consolidación (clave)

- **Motor de lectura:** `pandas.read_excel(..., engine='calamine')` — 5-10x más rápido que openpyxl.
  openpyxl no terminaba de leer los APRENDER de 1000+ columnas; calamine lee el mayor en ~2.4s.
- **Familia RA (7 bases × 15 años):** formato **ANCHO**, 1 parquet por base, años apilados (`anio`).
  Claves `provincia/departamento/sector/ambito` (+ extras Cargos Bis y Matricula por edad).
  Ojo: 2024 usa `Departamento` capitalizado → `_norm_keys()` lo normaliza. Columnas crecen en años
  recientes (union) → `pd.concat(sort=False)`. `coerce_for_parquet()` homogeneiza tipos.
- **Familia APRENDER (48 archivos):** formato **LARGO/tidy** particionado por año. Cada archivo se
  melt-ea; se descartan celdas vacías; se clasifica `tipo_variable` (desempeño/contexto/nse/
  nivel_educativo_hogar/otro). Claves: `cod_provincia`↔`jurisdiccion`; **algunos sin departamento**
  (nivel provincia). Total ~18,7 M filas.
- **Diccionario APRENDER:** cada columna `pregunta_opción` mapea a etiqueta `"pregunta - opción"`;
  se separa con `str.rsplit(' - ', n=1)`. 15 hojas por año/nivel, ~10.775 definiciones.
- **Unidades:** APRENDER = conteos PONDERADOS (factor de expansión). RA = conteos ABSOLUTOS.
- **Por qué Parquet:** Cargos Bis 1,46M filas y APRENDER largo ~19M superan el límite de Excel (1,05M).

## Datos (resumen)

- `resultados_aprender/`: 156 `.xlsx`, 2 `.sav`, 3 `.pdf`.
- Familia 1 — estadística agregada 2011–2025: Caracteristicas, Cargos, Cargos Bis,
  Matricula, Matricula por edad, Poblacion, Trayectoria.
- Familia 2 — Bases APRENDER 2016–2025 (sin 2020): Censal/Muestral × Primaria/Secundaria ×
  grado × área (Lengua, Matemática, Cs. Naturales, Cs. Sociales, Ciudadanía, Solo CC).
- Microdatos SPSS: `Base_publica_Ap2024.sav` (secundaria, 117 MB, NO versionado) y
  `Base_publica_prim_Ap2024.sav` (primaria, 5,5 MB, sí versionado).

## Decisiones clave

- **Archivo grande fuera de git:** `Base_publica_Ap2024.sav` va al `.gitignore`. No se usa
  Git LFS (por ahora). El resto de las bases sí se versionan.
- **Irregularidades de nombrado** en la fuente hay que normalizarlas al parsear (dobles
  espacios, sufijo `.csv.xlsx`, ausencia de `Censal/Muestral` en años viejos). Ver CONTEXTO.md.
- **Comparabilidad temporal limitada:** el operativo cambia de nivel/grado/cobertura por año.

## Flujo de trabajo

- `.xlsx` → `pandas.read_excel(engine='calamine')`. `.sav` → `pyreadstat.read_sav`.
- Outputs grandes → `ctx_execute` (context-mode) en vez de consola.
- Commits: usuario Santiago Riverti, sin `Co-Authored-By`.
- **Uso normal (Colab):** el 00 se corre **una vez** (guarda en Drive, persistente); el 01 solo
  **monta Drive y lee** (no reconsolida). Re-correr el 00 solo si se borra la carpeta del Drive,
  se agregan datos nuevos, o cambia la lógica de consolidación. Cada apertura pide autorizar Drive.

## Pendiente / próximos pasos

- [x] Notebook 00 de consolidación (hecho, corre end-to-end y validado en Colab).
- [x] Diccionario maestro con significado/unidades de cada variable.
- [x] Colab + guardado en Drive + verificación (firma) + auditoría de datos.
- [x] Documentación de traspaso (`ESTADO.md`) y commits/push.
- [x] Notebook 01 de trayectorias descriptivas (7 gráficos) + listado de variables (sección D).
- [x] Revisión de resultados del 01 contra los datos (A3 corregido, ciclo lectivo en A1/A2).
- [x] Corregir en el 00 grado "No especificado" (2016–2018) y `3grado` → cohortes ampliadas; firma `bdedd07f319c`.
- [x] Usuario re-corrió 00 y 01 en Colab (firma `bdedd07f319c`); Drive auditado = idéntico al local.
- [x] Listado de variables sin truncar: 01 secciones C (catálogo + xlsx/txt), D (zip), E (5 celdas de impresión).
- [ ] Opcional: afinar clasificación de variables `tipo_variable == 'otro'` (~2,1M filas).
- [ ] Opcional: integrar microdatos `.sav` 2024 (requiere `pyreadstat`, no instalado).
