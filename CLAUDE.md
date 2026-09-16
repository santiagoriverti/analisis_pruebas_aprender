# CLAUDE.md — análisis_pruebas_aprender

Instrucciones para Claude Code en este repositorio (se cargan solas al abrir el proyecto, en cualquier PC).

## Al empezar una sesión
1. Leer **[`ESTADO.md`](ESTADO.md)** (handoff: estado, cómo correr, gotchas, próximos pasos, bitácora) y
   **[`.claude/memory/project.md`](.claude/memory/project.md)** (memoria de trabajo: decisiones, números de control, forma de trabajar).
2. `git fetch && git status -sb` para confirmar que el local está al día con `origin/main`.
3. Contexto de datos (familias, nombres de archivo, diccionarios): [`CONTEXTO.md`](CONTEXTO.md) y
   [`datos_consolidados/README.md`](datos_consolidados/README.md).

## Qué es
Consolidación (`00_consolidacion.ipynb`) y análisis **descriptivo** (`01_analisis.ipynb` trayectorias,
`02_brechas.ipynb` brechas, `03_provincias.ipynb` provincias y contexto, `04_contexto.ipynb` contexto del estudiante en el tiempo, `05_asociaciones.ipynb` asociaciones entre cambios de contexto y desempeño) de las Pruebas APRENDER 2016–2025 y el Relevamiento Anual (RA) 2011–2025 de la
Secretaría de Educación de la Nación (Argentina). El usuario corre los notebooks en **Google Colab**: el 00 guarda en
*Mi unidad/`pruebas_aprender`* y el 01 a 05 leen de ahí.

## Reglas del usuario (obligatorias)
- Responder y documentar en **español**.
- **Sin econometría** (pidió análisis descriptivo).
- Commits **solo con su usuario (Santiago Riverti)**, **sin** `Co-Authored-By` ni ninguna atribución a Claude.
- Commitear/pushear cuando lo pide (lo pide para poder correr en Colab).
- **Verificar los resultados contra los datos** antes de darlos por buenos, y reportar con honestidad lo que no se puede
  calcular (p. ej. brecha por NSE con bases agregadas).

## Forma de trabajar (probada)
- **Editar notebooks con scripts Python guardados en archivo** que usan `nbformat` (leer → modificar `cell.source` con
  asserts de contenido → `nbformat.validate` → escribir). **No** pasar código con heredoc sin comillas por bash
  (se comen los backticks y los `\n`). Para notebooks nuevos, generar las celdas con `nbformat.v4`.
- **Ejecutar y validar localmente** antes de commitear, y versionar el notebook **ejecutado**:
  `python -m jupyter nbconvert --to notebook --execute --inplace <nb>.ipynb --ExecutePreprocessor.timeout=1800`
  Luego revisar salidas (errores, `stderr`, tablas clave) y mirar los PNG generados.
- Consolidación local válida = `firma=bdedd07f319c` en la sección 9 del 00. Números de control en `ESTADO.md` §5.
- Mensajes de commit largos: escribir a un archivo y `git commit -F archivo` (en PowerShell los here-strings pueden
  ser bloqueados por un hook; usar Bash).
- Colab trunca la salida de una celda a ~5.000 líneas: partir impresiones largas en varias celdas.
- **Validar corridas de Colab:** pedir al usuario los zips (`graficos_*.zip` y, del Drive, `parquet/` y `excel/`) y
  compararlos archivo por archivo contra lo local con scripts (parquet con `assert_frame_equal`; Excel regenerando la
  receta de `exportar_resultados` del 00). Última validación completa: 2026-09-14 (00–02); 03, 04 y 05 el 2026-09-16 (Excel idénticos).
- **pyarrow `group_by` con hilos no garantiza el orden de salida:** si el orden importa, archivos en orden fijo +
  `group_by(..., use_threads=False)` + `sort_values(..., kind='stable')`.

## Trampas de datos que ya mordieron (detalle en ESTADO.md §6)
- Cargos Bis: `total` mezcla cargos, horas y módulos → filtrar por `tipo`.
- Base Trayectoria del año *t* = ciclo lectivo *t−1*.
- APRENDER 2016–2018: nivel/grado se completan en el 00 (verificado por edad modal).
- Desempeño × NSE no se puede cruzar en los agregados (solo microdatos).
- Nombres de provincia inconsistentes entre años → normalizar.
- Matemática Secundaria 2022 sin nivel Avanzado; Chubut sin Secundaria 2019; sin diccionario 2025.
- Cuestionario Primaria 2025 renumerado (códigos deducidos por opciones); jornada extendida del RA por provincia no confiable.
- Cambios parejos en las 24 provincias entre dos operativos = probable cambio de cuestionario (Primaria 2023→2025: madre, libros).
- RA: egresados de primaria de los ciclos 2010–2012 incompletos (provincias con 0); sobreedad secundaria de Santa Cruz 2025 atípica;
  alumnos por maestro en Buenos Aires ≈ 26 hasta 2022 → 18,4 en 2025 (probable cambio de reporte).
- Correlaciones entre 24 provincias: con ~100 comparaciones, ~5 dan p < 0,05 por azar → permutaciones + Benjamini-Hochberg
  y control del punto de partida (frente a pares) antes de afirmar nada (05).

## Al terminar una sesión
Actualizar `ESTADO.md` (estado, próximos pasos, bitácora) y `.claude/memory/project.md`; commitear y pushear si el
usuario lo pide.
