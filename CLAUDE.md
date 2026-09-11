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
`02_brechas.ipynb` brechas) de las Pruebas APRENDER 2016–2025 y el Relevamiento Anual (RA) 2011–2025 de la
Secretaría de Educación de la Nación (Argentina). El usuario corre los notebooks en **Google Colab**: el 00 guarda en
*Mi unidad/`pruebas_aprender`* y el 01/02 leen de ahí.

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

## Trampas de datos que ya mordieron (detalle en ESTADO.md §6)
- Cargos Bis: `total` mezcla cargos, horas y módulos → filtrar por `tipo`.
- Base Trayectoria del año *t* = ciclo lectivo *t−1*.
- APRENDER 2016–2018: nivel/grado se completan en el 00 (verificado por edad modal).
- Desempeño × NSE no se puede cruzar en los agregados (solo microdatos).
- Nombres de provincia inconsistentes entre años → normalizar.
- Matemática Secundaria 2022 sin nivel Avanzado; Chubut sin Secundaria 2019; sin diccionario 2025.

## Al terminar una sesión
Actualizar `ESTADO.md` (estado, próximos pasos, bitácora) y `.claude/memory/project.md`; commitear y pushear si el
usuario lo pide.
