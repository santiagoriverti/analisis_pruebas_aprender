# ESTADO DEL PROYECTO — análisis_pruebas_aprender

> Documento de traspaso (handoff). Sirve para **retomar el proyecto en otra sesión o en otra PC**
> sin perder contexto. Última actualización: **2026-08-31**.

---

## 1. Resumen en una línea

Consolidación documentada de las **Pruebas APRENDER** (evaluación, 2016–2025) y la **estadística
educativa RA** (Relevamiento Anual, 2011–2025) de la Secretaría de Educación de la Nación (Argentina).
El notebook `00_consolidacion.ipynb` deja todo listo para analizar; **está completo, probado y validado**.

- **Remoto:** https://github.com/santiagoriverti/analisis_pruebas_aprender (rama `main`)
- **Local (esta PC):** `C:\Users\sriverti\Desktop\INECO\Repositorios\analisis_pruebas_aprender`
- **Salida en Drive:** *Mi unidad/`pruebas_aprender`* (`parquet/` + `excel/`)

## 2. Estado actual (qué está hecho)

| Componente | Estado |
|---|---|
| Setup del repo (README, .gitignore, CONTEXTO, memoria) | ✅ |
| `00_consolidacion.ipynb` — consolidación completa | ✅ corre end-to-end, 0 errores |
| Diccionario maestro (significado + unidades de cada variable) | ✅ |
| Ejecución en Colab (badge + bootstrap que clona el repo) | ✅ verificado |
| Guardado automático en Google Drive (parquet + excel) | ✅ verificado |
| Celda de verificación con firma reproducible | ✅ |
| **Auditoría de los datos entregados** (parquet descargado del Drive) | ✅ íntegro |
| `01_analisis.ipynb` — arquitectura + análisis (comparabilidad, series, brechas, cruces) | ✅ corre, 0 errores, 4 gráficos |
| Profundizar un foco analítico específico | ⏳ pendiente (elegir track) |

**Firma de referencia de la consolidación: `c9740263478b`**
Si al correr el notebook la `firma` da ese valor, los datos compilaron idénticos y sin errores.
(Verificado: coincide en local (Py 3.14 / pandas 2.3) y en Colab (Py 3.13 / pandas 2.2) → determinístico.)

## 3. Cómo retomar en una PC nueva

```bash
git clone https://github.com/santiagoriverti/analisis_pruebas_aprender.git
cd analisis_pruebas_aprender
pip install -r requirements.txt          # pandas, pyarrow, openpyxl, python-calamine, jupyter
jupyter notebook 00_consolidacion.ipynb  # Ejecutar todo
```

- Los datos crudos (`resultados_aprender/`, 156 `.xlsx`) **están versionados**, así que el clone los trae.
- **No** se versiona `Base_publica_Ap2024.sav` (117 MB, supera el límite de GitHub) ni la salida pesada
  regenerable de `datos_consolidados/` (`ra/`, `aprender_long/`, `*.parquet`).
- **Motor de lectura obligatorio:** `python-calamine`. Sin él, openpyxl no termina de leer los
  archivos APRENDER de 1000+ columnas. La celda 1 del notebook lo instala solo si falta.

### Alternativa sin instalar nada (Google Colab)
Abrir el badge del README → *Entorno de ejecución → Ejecutar todo*. Clona el repo, procesa,
imprime la verificación y guarda en tu Drive.

## 4. Dónde quedan los resultados

- **Al correr en local:** `datos_consolidados/` (dentro del repo; regenerable, casi todo en `.gitignore`).
- **Al correr en Colab:** además, en *Mi unidad/`pruebas_aprender`*:
  - `parquet/` → formato eficiente, **es lo que consume el notebook 01**.
  - `excel/` → legible por humanos (xlsx ≤200k filas; CSV para Cargos Bis y Matrícula por edad;
    `aprender_desempenos.xlsx` con los niveles de desempeño).
  - `catalogo_archivos.csv`.

Leer desde Drive en el notebook 01:
```python
from google.colab import drive; drive.mount('/content/drive')
BASE = '/content/drive/MyDrive/pruebas_aprender/parquet'
mat     = pd.read_parquet(f'{BASE}/ra/ra_matricula.parquet')
ap_2024 = pd.read_parquet(f'{BASE}/aprender_long', filters=[('anio','==',2024)])
```

## 5. Modelo de datos (lo esencial)

- **RA → ancho.** 7 parquet (uno por base), años 2011–2025 apilados en `anio`.
  Claves: `provincia, departamento, sector, ambito` (+ `nivel/tipo/categoria/cargo/planta_tipo` en
  Cargos Bis; `grado` en Matrícula por edad). Valores = **conteos absolutos**.
- **APRENDER → largo/tidy.** Particionado por `anio`. Columnas: `cobertura, nivel, grado, area,
  jurisdiccion, departamento, sector, ambito, variable, tipo_variable, valor`.
  Valores = **conteos ponderados de estudiantes** (factor de expansión).
  `tipo_variable ∈ {desempeño, contexto, nse, nivel_educativo_hogar, otro}`.
- **Diccionario maestro** (`diccionario_maestro.xlsx`): significado y unidad de cada variable.
  APRENDER mapea cada columna `pregunta_opción` → `pregunta_texto` + `opcion_texto`.

### Métricas de referencia (para chequeo rápido)
- RA: Matrícula por edad 300.333×44 · Matrícula 18.020×105 · Cargos Bis 1.464.119×11 ·
  Cargos 18.426×61 · Características 18.021×74 · Población 18.017×170 · Trayectoria 17.912×317.
- APRENDER largo: **18.721.597 filas** (2016:3.788.601 · 2017:2.971.268 · 2018:1.079.294 ·
  2019:2.333.376 · 2021:1.740.100 · 2022:2.175.201 · 2023:1.776.906 · 2024:1.711.855 · 2025:1.144.996).
- Diccionarios: `dic_ra` 701×4 · `dic_ap` 10.775×7.
- Chequeo: `cargos_bis_total_2024 = 11.208.635,0`. Sin valores negativos ni nulos en `valor`.

## 6. Trampas conocidas (gotchas)

- **`Departamento` capitalizado en archivos 2024** → normalizado en `_norm_keys()`.
- **APRENDER sin columna `departamento`** en varios archivos (agregación a nivel provincia):
  ~240.946 filas con `departamento` nulo. Es esperado, no es error.
- **Cargos Bis:** 7 filas con `ambito` nulo (vienen así del origen).
- **`tipo_variable = 'otro'`** (~2,1 M filas, 11%): columnas APRENDER que no matchean los prefijos
  conocidos. Catch-all correcto; se puede afinar en el notebook 01 con el diccionario.
- **Irregularidades de nombrado de la fuente:** dobles espacios (`Muestral  -`), sufijo `.csv.xlsx`
  (2024 Prim 3° Solo CC), ausencia de `Censal/Muestral` en 2016–2018 (= operativo principal, Censal).
- **Comparabilidad temporal limitada:** el operativo cambia de nivel/grado/cobertura por año.
- **2020:** sin operativo APRENDER (pandemia); solo estadística RA.

## 7. Análisis (notebook 01) — comparabilidad

`01_analisis.ipynb` ya establece el marco y trae funciones reutilizables + 4 tracks de ejemplo:
- **Track A — RA series** (matrícula, trayectoria, etc.): comparables 2011–2025.
- **Track B — cohortes APRENDER** comparables: Primaria 6° Censal (2021/23/25), Secundaria 5-6° Censal (2019/22/24).
- **Track C — brechas** (sector, ámbito) dentro de un año.
- **Track D — cruce RA↔APRENDER** por geografía (ej: % gestión privada vs % Satisf+Avanz; corr≈0,55).

Funciones clave: `cargar_ra/cargar_aprender/cargar_desempeno`, `harmonizar_nivel` + `ORDEN4`,
`desempeno_pct(df, group_cols)`, `serie_cohorte(...)`, `norm_geo` + `CROSSWALK_PROV`.

**Regla de comparabilidad:** RA = series de tiempo válidas; APRENDER = solo dentro de la misma
`(nivel, grado, cobertura)`. Escala de desempeño homogénea (4 niveles) salvo Primaria 3° 2024.

## 8. Próximos pasos

1. **Elegir un foco** para profundizar en el notebook 01 (o crear un 02): evolución de desempeños,
   brechas por NSE / nivel educativo del hogar, o modelar el cruce RA↔APRENDER con más variables/crosswalk.
2. (Opcional) Mejorar el crosswalk de departamentos RA↔APRENDER (hoy matchean ~271; se puede ampliar).
3. (Opcional) Afinar la clasificación de las variables `tipo_variable == 'otro'` (~2,1 M filas).
4. (Opcional) Integrar los microdatos `.sav` 2024 (requiere `pyreadstat`, no instalado aún).

## 9. Convenciones del proyecto

- Commits: **solo** con el usuario Santiago Riverti, **sin** `Co-Authored-By` ni atribución de Claude.
- Datos crudos versionados; salida pesada regenerable en `.gitignore`.
- Idioma de trabajo: español.

## 10. Bitácora de sesiones

| Sesión | Fecha | Qué se hizo |
|---|---|---|
| 1 | 2026-08-31 | Setup: README, .gitignore (excluye .sav 117 MB), CONTEXTO, memoria. |
| 2 | 2026-08-31 | `00_consolidacion.ipynb`: catálogo + diccionario maestro + consolidación (calamine). |
| 3 | 2026-08-31 | Colab (badge + bootstrap), celda de verificación (firma), guardado en Drive (parquet + excel). |
| 4 | 2026-08-31 | Auditoría de los datos descargados del Drive (íntegros, firma `c9740263478b`); documentación de traspaso. |
| 5 | 2026-08-31 | `01_analisis.ipynb`: marco de comparabilidad + funciones + 4 tracks (series RA, cohortes APRENDER, brechas, cruce RA↔APRENDER). |
