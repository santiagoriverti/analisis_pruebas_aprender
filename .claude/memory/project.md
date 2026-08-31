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

## Estado actual (2026-08-31)

> **Para retomar en otra PC/sesión: leer `ESTADO.md`** (handoff completo: instalación, ejecución,
> dónde quedan los resultados, métricas de referencia, gotchas y próximos pasos).
> **Firma de referencia de la consolidación: `c9740263478b`** (validada en local y en Colab).

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
- Trabajo sesión 5 (notebook 01 análisis):
  - `01_analisis.ipynb` (16 celdas, corre en Colab/local, 0 errores, 4 gráficos).
  - Marco de **comparabilidad**: RA = series de tiempo (2011-2025); APRENDER = solo dentro de la
    misma `(nivel, grado, cobertura)`. Cohortes comparables: Primaria 6° Censal (2021/23/25),
    Secundaria 5-6° Censal (2019/22/24). Escala 4 niveles salvo Primaria 3° 2024 (Lector/Nivel I-V).
  - Funciones: `cargar_ra/aprender/desempeno`, `harmonizar_nivel`+`ORDEN4`, `desempeno_pct(df,group)`,
    `serie_cohorte`, `norm_geo`+`CROSSWALK_PROV` (CABA y TdF difieren de nombre entre RA y APRENDER).
  - 4 tracks: (A) series RA, (B) cohortes APRENDER, (C) brechas sector/ámbito, (D) cruce RA↔APRENDER
    por depto (271 matcheados, corr % privado vs % Satisf+Avanz ≈ 0,55).
  - Gotcha pandas: `str.split(pat, n=1)` requiere `n=` keyword.

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

- `.xlsx` → `pandas.read_excel`. `.sav` → `pyreadstat.read_sav`.
- Outputs grandes → `ctx_execute` (context-mode) en vez de consola.
- Commits: usuario Santiago Riverti, sin `Co-Authored-By`.

## Pendiente / próximos pasos

- [x] Notebook 00 de consolidación (hecho, corre end-to-end y validado en Colab).
- [x] Diccionario maestro con significado/unidades de cada variable.
- [x] Colab + guardado en Drive + verificación (firma) + auditoría de datos.
- [x] Documentación de traspaso (`ESTADO.md`) y commits/push.
- [ ] Definir objetivo analítico y armar **notebook 01 de análisis** (leer desde `pruebas_aprender/parquet/`).
- [ ] Evaluar series comparables donde el universo lo permita (cuidado: operativo cambia por año).
- [ ] Opcional: afinar clasificación de variables `tipo_variable == 'otro'` (~2,1M filas).
- [ ] Opcional: integrar microdatos `.sav` 2024 (requiere `pyreadstat`, no instalado).
