# Memoria de proyecto — análisis_pruebas_aprender

> Memoria de trabajo para sesiones de Claude Code (viaja con el repo: sirve en cualquier PC).
> Usuario: Santiago Riverti. Última actualización: **2026-09-14** (sesión 12).
> Handoff completo y bitácora: **`ESTADO.md`**. Reglas de trabajo: **`CLAUDE.md`**.

---

## 1. Identidad del proyecto
- Consolidación + análisis **descriptivo** (sin econometría, pedido explícito) de **APRENDER 2016–2025** y
  **Relevamiento Anual (RA) 2011–2025**, Secretaría de Educación de la Nación (Argentina).
- Remoto: https://github.com/santiagoriverti/analisis_pruebas_aprender (`main`).
- Local PC INECO: `C:\Users\sriverti\Desktop\INECO\Repositorios\analisis_pruebas_aprender`.
- El usuario ejecuta en **Google Colab** (badges en README). Drive: *Mi unidad/`pruebas_aprender`* (`parquet/`, `excel/`).

## 2. Estado al cierre (2026-09-14)
- `00_consolidacion.ipynb` (24 celdas) ✅ — firma **`bdedd07f319c`** (local y Colab). Drive re-consolidado y
  **auditado**: catálogo idéntico, 57 parquet, 18 tablas con contenido idéntico al local.
- `01_analisis.ipynb` (38 celdas) ✅ — corrido por el usuario en Colab con resultados = local. Sesión 12: orden de
  `opciones` del catálogo hecho determinístico (celda 25: archivos ordenados + `group_by(use_threads=False)` + sort estable);
  **falta re-correrlo en Colab tras el push** y confirmar `variables_disponibles` idéntico al local.
- `02_brechas.ipynb` (21 celdas) ✅ local y Colab — `brechas_aprender.xlsx` (8 hojas) idéntico al local.
- Auditoría del Drive 2026-09-14 (re-corrida del 00 en Colab): 57 parquet, 14 tablas de `excel/` (incl.
  `aprender_desempenos.xlsx` 109.473 filas y los CSV de Cargos Bis / Matrícula por edad) y `catalogo_archivos.csv` idénticos.
- Último commit relevante antes del traspaso: `272a149` (02 de brechas); luego commit de documentación (sesión 11).
- Próximo paso sugerido (a elegir por el usuario): brecha por NSE con microdatos 2024, más trayectorias RA,
  contexto del estudiante en el tiempo, o informe. Ver `ESTADO.md` §8.

## 3. Decisiones tomadas (y por qué)
| Decisión | Motivo |
|---|---|
| RA en formato **ancho** (7 parquet), APRENDER **largo/tidy** particionado por año | Columnas RA estables; APRENDER tiene miles de columnas que cambian por año |
| Parquet + Excel legible (umbral 200k filas → CSV) | Cargos Bis 1,46 M y APRENDER 18,7 M filas superan Excel |
| Motor `calamine` | openpyxl no termina con los APRENDER de 1000+ columnas |
| `.sav` secundaria 2024 (117 MB) fuera de git | Límite de 100 MB de GitHub (sin LFS) |
| 00 se corre una vez; 01 y 02 solo leen del Drive | Evitar reconsolidar (~5 min) en cada sesión de Colab |
| Firma de verificación incluye operativos (año, cobertura, nivel, grado) | Detectar cambios de metadatos, no solo de filas |
| Nivel/grado 2016–2018 completados en el 00 con tabla explícita + assert por edad modal | Los nombres de archivo no los traen; evidencia en los datos |
| Trayectoria RA rotulada por **ciclo lectivo** (t−1) | Matrícula inicial de Trayectoria(t) ≈ Matrícula(t−1) todos los años |
| Cargos docentes = `tipo=='Cargos'` (horas y módulos aparte) | `total` de Cargos Bis mezcla unidades |
| Brechas solo por sector, ámbito y provincia | Desempeño × NSE no existe en los agregados (sin distribución conjunta) |
| Listado de variables impreso en 5 celdas + `variables_disponibles.xlsx/.txt` | Colab trunca cada celda a ~5.000 líneas |
| Notebooks nuevos en archivos separados (02) | Mantener el 01 manejable |

## 4. Números de control (para verificar corridas)
- Firma 00: `bdedd07f319c` (vieja `c9740263478b` = Drive desactualizado).
- APRENDER largo 18.721.597 filas; RA shapes en `ESTADO.md` §5; `dic_ra` 701×4, `dic_ap` 10.775×7.
- % Satisf+Avanz total país — Primaria 6° (2016/18/21/23/25): Lengua 66,8/75,3/70,9/66,4/76,9 · Mat 58,5/57,4/55,5/51,4/55,0.
  Secundaria 5-6° (2016/17/19/22/24): Lengua 53,6/62,5/61,8/56,9/56,9 · Mat 29,8/31,1/28,7/17,6/17,6.
  (Coinciden con valores publicados, p. ej. Lengua 6° 2018 = 75%; Secundaria 2016 Lengua 53,6% / Mat 30%.)
- Cargos docentes (`tipo=='Cargos'`): 632.494 (2011) → 882.824 (2024) → 889.843 (2025).
- Repitencia secundaria por ciclo lectivo: 18,3% (2010) → 5,4% (2020, pandemia) → 10,2% (2024).
- Brecha privado−estatal (% Satisf+Avanz): ~20–27 pp estable. Urbano−rural Secundaria 2024: Lengua 15,6 pp, Mat 8,3 pp.
- Catálogo de variables: RA 744 columnas; APRENDER 5.571 variables / 1.591 preguntas; 102 variables 2025 sin diccionario propio.

## 5. Gotchas técnicos (además de los de datos en `ESTADO.md` §6)
- **Editar notebooks:** script Python en archivo + `nbformat` con asserts; nunca heredoc sin comillas por bash
  (rompe backticks y `\n`). En PowerShell los here-strings multilínea pueden disparar un hook que bloquea el comando.
- **Ejecutar:** `python -m jupyter nbconvert --to notebook --execute --inplace <nb> --ExecutePreprocessor.timeout=1800`
  (`jupyter` no está en el PATH de bash; usar `python -m jupyter`). Tiempos: 00 ~5 min, 01 ~2,5 min, 02 ~20 s.
- **Commits:** mensaje en archivo + `git commit -F`; sin atribución a Claude.
- pandas `plot(style=dict, color=dict)` → ValueError si los nombres de columna contienen letras de color: usar `ax.plot`.
- Distintos rápidos sobre APRENDER: `pyarrow.dataset(...).to_table(columns=...).group_by(cols).aggregate([])`.
- Filtrar APRENDER por partición: `pads.dataset(OUT/aprender_long/anio=YYYY).to_table(filter=...)`.
- Excel con textos del diccionario: limpiar con `openpyxl.cell.cell.ILLEGAL_CHARACTERS_RE`.
- Hojas Excel con MultiIndex de columnas: aplanar antes de `to_excel`.
- **pyarrow `group_by` con hilos devuelve filas en orden arbitrario** (4 órdenes distintos en 4 corridas): si el orden
  se usa (p. ej. `dict.fromkeys` para listar opciones), pasar `use_threads=False` y archivos en orden fijo.
- Validar corridas de Colab: pedir al usuario los zips (`graficos_*.zip`, y del Drive `parquet/` y `excel/`) y comparar
  archivo por archivo con scripts (parquet con `assert_frame_equal`; Excel regenerando la receta de `exportar_resultados`).

## 6. Arquitectura del 00 (referencia)
- `clasificar(f)` → familia (RA/APRENDER/DICCIONARIO/OTRO). `parse_nombre_aprender(f)` = lo que dice el nombre;
  `parse_aprender(f)` completa con `NIVEL_SIN_NOMBRE` / `GRADO_SIN_NOMBRE`.
- `tipo_variable(col)`: prefijos `(l|m|cn|cs|c)desemp` → desempeño; `ap\d+` → contexto; `NSE` → nse;
  `Nivel_Ed` → nivel_educativo_hogar; resto → otro.
- `_norm_keys` (provincia/departamento/sector/ambito, `cod_provincia`→`jurisdiccion`), `ra_base_wide`,
  `coerce_for_parquet`, `aprender_to_long` (melt, descarta vacíos), `exportar_resultados(origen, destino)` (Drive).
- Secciones: 1 imports · 2 funciones · 3 catálogo · 4 diccionario · 5 RA · 6 APRENDER · 7 Excel/catálogos ·
  8 validaciones + control de grado · 9 verificación (firma) · 10 Drive.

## 7. Historial resumido
- 2026-08-31 (s1–s6): setup, 00, Colab + Drive + firma, auditoría, 01 de trayectorias.
- 2026-09-11 (s7): revisión del 01 → Cargos Bis corregido, ciclo lectivo, listado de variables.
- 2026-09-11 (s8): grado 2016–2018 en el 00, firma nueva, cohortes ampliadas.
- 2026-09-11 (s9): usuario corrió 00/01 en Colab, Drive auditado, listado sin truncar.
- 2026-09-11 (s10): notebook 02 de brechas.
- 2026-09-11 (s11): traspaso — ESTADO reescrito, CLAUDE.md, memoria reorganizada, requirements con matplotlib.
- 2026-09-14 (s12): usuario corrió 00/01/02 en Colab; validación completa (Drive y salidas idénticos); arreglo de orden
  determinístico en el catálogo del 01 y re-ejecución local.
