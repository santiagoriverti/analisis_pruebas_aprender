# scripts/ — herramientas de mantenimiento

Scripts auxiliares (no hacen falta para **usar** los notebooks en Colab). Se corren desde la **raíz del repo**.

| Script | Para qué |
|---|---|
| `generar_04_contexto.py` · `generar_05_asociaciones.py` · `generar_06_microdatos.py` · `generar_07_explorador_microdatos.py` | Generan los notebooks 04 a 07 (celdas con `nbformat`). `--debug` ejecuta las celdas como script para probar rápido sin escribir el notebook. Regenerar **reemplaza** el notebook: luego ejecutarlo con `nbconvert` y revisar salidas. |
| `comparar_excel.py` | Valida una corrida de Colab: compara hoja por hoja el Excel descargado contra el local (`assert_frame_equal` exacto). |
| `listar_cuestionario.py` | Lista las preguntas del cuestionario por cohorte y año con texto y % por opción → `cuestionario_por_anio.txt`. Para ubicar códigos de una pregunta que cambia de número entre años (04 y 05). |

Los notebooks 00 a 03 no tienen generador versionado: se editan directamente con `nbformat` (ver `CLAUDE.md`).

Flujo para cambiar un notebook generado:
```bash
python scripts/generar_04_contexto.py --debug          # probar cambios
python scripts/generar_04_contexto.py                  # escribir el notebook
python -m jupyter nbconvert --to notebook --execute --inplace 04_contexto.ipynb --ExecutePreprocessor.timeout=1800
```
