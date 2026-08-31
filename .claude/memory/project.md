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

- Repo con documentación + **notebook 00 de consolidación funcionando end-to-end**.
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

- [x] Notebook 00 de consolidación (hecho, corre end-to-end).
- [x] Diccionario maestro con significado/unidades de cada variable.
- [ ] Commit + push de notebook 00, requirements, docs y referencias livianas.
- [ ] Definir objetivo analítico y armar notebook 01 de análisis.
- [ ] Evaluar series comparables donde el universo lo permita (cuidado: operativo cambia por año).
- [ ] Opcional: integrar microdatos `.sav` 2024 (requiere `pyreadstat`, no instalado).
