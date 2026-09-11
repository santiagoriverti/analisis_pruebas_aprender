# ESTADO DEL PROYECTO — análisis_pruebas_aprender

> Documento de traspaso (handoff). Sirve para **retomar el proyecto en otra sesión o en otra PC**
> sin perder contexto. Última actualización: **2026-09-11**.

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
| `01_analisis.ipynb` — trayectorias descriptivas (RA + cohortes APRENDER) | ✅ corre, 0 errores, 7 gráficos (revisado 2026-09-11) |
| Listado de variables disponibles + significado (secciones C–E del 01 + `variables_disponibles.xlsx`) | ✅ |
| Datos del Drive re-consolidados en Colab y auditados (firma `bdedd07f319c`, 18 tablas idénticas al local) | ✅ |
| Más trayectorias / cortes geográficos | ⏳ opcional |

**Firma de referencia de la consolidación: `bdedd07f319c`** (desde 2026-09-11)
Si al correr el notebook la `firma` da ese valor, los datos compilaron idénticos y sin errores.
La firma incluye los operativos APRENDER `(año, cobertura, nivel, grado)`, por eso cambió al corregir el
grado de 2016–2018 (la anterior, `c9740263478b`, corresponde a la consolidación con grado "No especificado").
Las métricas de filas/columnas no cambiaron. (La consolidación es determinística: la firma anterior coincidió
en local (Py 3.14 / pandas 2.3) y en Colab (Py 3.13 / pandas 2.2).)

> ⚠ **Los datos del Drive quedaron con la consolidación anterior** (grado "No especificado" en 2016–2018).
> Hay que **re-correr el 00 en Colab una vez** (verificar `firma=bdedd07f319c`) y después el 01.

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

### Flujo de trabajo día a día (importante)
El **00 se corre una sola vez**: guarda en Google Drive, que **es persistente** (sobrevive al cierre
de la VM de Colab). El **01 solo monta el Drive y lee** — no re-consolida. En el uso normal se abre el
**01**, *Ejecutar todo*, se autoriza Drive, se ven las trayectorias y se descargan los gráficos.
**Re-correr el 00 solo si:** (1) se borró/movió la carpeta `pruebas_aprender` del Drive; (2) se agregan
datos nuevos a `resultados_aprender/`; (3) se cambió la lógica de consolidación. Cada apertura en Colab
pide autorizar Drive (es por sesión; no reconsolida).

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
- **Cargos Bis: `total` mezcla unidades según `tipo`** (Cargos, Cargos Suplentes, Cargos No Docentes, Horas,
  Horas Suplentes, Módulos, Módulos Suplentes). Sumar sin filtrar da ~11,2 M (2024) cuando los cargos docentes
  son **882.824**. Filtrar SIEMPRE por `tipo`. (`tipo == 'Cargos'` no tiene filas de subtotal.)
- **Base Trayectoria: el relevamiento del año *t* informa el ciclo lectivo *t−1*.** Evidencia: la matrícula inicial
  de Trayectoria(*t*) se parece más a Matrícula(*t−1*) que a Matrícula(*t*) en todos los años (2021: −0,6% vs −2,5%).
  Por eso la caída de repitencia de "RA 2021" es el **ciclo 2020** (pandemia). El 01 usa `a_ciclo_lectivo()`.
- **APRENDER Secundaria Matemática 2022:** `mdesemp_Avanzado` viene vacía (`' '`) en la fuente → no hay Avanzado ese año.
- **Secundaria 5-6° 2022 vs 2024** dan % Satisf+Avanz casi idénticos (Lengua 56,94/56,89; Mat 17,64/17,63). No es
  duplicación: los archivos y las distribuciones son distintos.
- **Nivel/grado ausentes en el nombre (2016–2018)** — corregido en el 00 (sesión 8): 2016/2017 Primaria = `6 grado`,
  Secundaria = `5-6 año`; 2018 (sin nivel ni grado) = Primaria `6 grado`; `3grado` → `3 grado`. Evidencia: edad
  modal declarada (pregunta 1): 11 años → 6°, 17 → 5-6°, 8 → 3°, 14 → 2-3°. La sección 8 del 00 lo **controla con
  un assert** y el catálogo marca `nivel_grado_inferido`. Archivos 2016-2018 sin "Censal/Muestral" = Censal
  (el diccionario los llama "Estudiantes", no "Muestra").
- **RA Características/Población:** muchas columnas numéricas quedaron como texto (celdas vacías `''`) →
  `pd.to_numeric(..., errors='coerce')` antes de sumar.
- **Diccionario APRENDER:** no hay diccionario 2025; 102 variables 2025 toman el texto del año más cercano.
- **Matrícula (RA):** `s2` = sala de 2 años y `s_2` = sobreedad en 2° año → no normalizar nombres quitando `_`.

## 7. Trayectorias (notebook 01) — descriptivo

Enfoque elegido por el usuario: **trayectorias descriptivas** (evolución temporal), **sin econometría**.
`01_analisis.ipynb` (corre en Colab/local, 0 errores, 7 gráficos) trae funciones reutilizables y:
- **A — Estadística educativa (RA, 2011–2025):** A1 matrícula inicial por nivel; A2 tasa de repitencia y de
  abandono (salidos sin pase) — ambas **por ciclo lectivo** (t−1); A3 **cargos docentes por nivel** (`tipo=='Cargos'`,
  632 mil en 2011 → 890 mil en 2025) + tabla de todos los tipos; A4 horas cátedra y módulos (millones).
- **C — Catálogo de variables:** arma RA (744 columnas en 7 bases, series numeradas agrupadas, años con dato) y
  APRENDER (5.571 variables / 1.591 preguntas con años, códigos y opciones). Deja `variables_ra`,
  `variables_aprender`, `preguntas_aprender` y `buscar_variable(texto)`; guarda `variables_disponibles.xlsx`
  (hojas RA_columnas, APRENDER_preguntas, APRENDER_variables) y `.txt` en `graficos_trayectorias/`. ~30–60 s.
- **D — Descarga:** zip con los 7 gráficos + `variables_disponibles.xlsx/.txt`.
- **E — Listado impreso por partes** (E.1 RA 500 líneas · E.2 APRENDER general 134 · E.3 contexto ≤2019 2.284 ·
  E.4 contexto ≥2021 2.216 · E.5 otro + resumen 785). **Colab corta la salida de una celda a ~5.000 líneas**:
  por eso no se imprime en una sola celda.
- **B — Desempeño APRENDER (cohortes comparables):** Primaria 6° Censal (2016/18/21/23/25) y Secundaria
  5-6° Censal (2016/17/19/22/24), % por nivel en Lengua y Matemática; y % Satisf+Avanz por sector
  (Primaria 6° Matemática). Años de cada cohorte en `ANIOS_PRIM6` / `ANIOS_SEC56` (celda de funciones).
- Los gráficos RA incluyen la **trayectoria Total** (línea negra punteada). Al finalizar, el notebook
  guarda todos los gráficos a **300 dpi** en `graficos_trayectorias/` y (en Colab) descarga un `.zip`.
- Badges de Colab en el README para ambos notebooks (00 y 01).

Funciones clave: `cargar_ra/cargar_aprender/cargar_desempeno`, `suma_anios`+`tasa` (RA, rangos
`PRIM=1-6`, `SEC=7-12`), `a_ciclo_lectivo` (Trayectoria t → ciclo t−1), `estilo_total`, `nota(fig, texto)`,
`harmonizar_nivel`+`ORDEN4`, `desempeno_pct(df, group_cols)`, `serie_cohorte(...)`, `buscar_variable(texto)`.
Indicadores RA desde base *Trayectoria*: `inicial_X` (matrícula), `nopromo_X` (repitentes), `ssp_X` (abandono).

**Regla de comparabilidad:** RA = series de tiempo válidas; APRENDER = solo dentro de la misma
`(nivel, grado, cobertura)`. Escala de desempeño homogénea (4 niveles) salvo Primaria 3° 2024.

## 8. Próximos pasos

1. Sumar más trayectorias RA (promoción, sobreedad desde *Matrícula por edad*, infraestructura desde
   *Características*) o cortes por provincia.
2. (Opcional, más adelante) Cruce RA↔APRENDER por geografía (ya se probó: ~271 deptos matchean; requiere
   crosswalk de departamentos más completo). **El usuario pidió no hacer análisis econométrico por ahora.**
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
| 5 | 2026-08-31 | `01_analisis.ipynb`: **trayectorias descriptivas** (matrícula, repitencia, abandono, cargos; desempeño APRENDER por cohorte y sector). Sin econometría, por pedido del usuario. |
| 6 | 2026-08-31 | Notebook 01: línea **Total** en gráficos RA, export de gráficos a **300 dpi** + descarga zip en Colab, badges de Colab (00 y 01) en README. Aclarado el flujo (00 una vez → Drive persistente; 01 solo lee). |
| 7 | 2026-09-11 | Revisión de resultados del 01 contra los datos: **A3 estaba mal** (sumaba horas/módulos/suplentes → 11,2 M; corregido a cargos docentes por nivel, ~883 mil en 2024) + nuevo A4 horas y módulos; A1/A2 rotulados por **ciclo lectivo** (Trayectoria t = ciclo t−1); nota de Avanzado vacío en Mat. Sec. 2022; fix warning de pandas; **sección D: listado completo de variables y su significado**. 00 sin cambios (firma igual). |
| 8 | 2026-09-11 | **00: nivel/grado completados en 2016–2018** (2016/17 Primaria 6 grado y Secundaria 5-6 año; 2018 Primaria 6 grado; `3grado`→`3 grado`), verificado por edad modal con assert en la sección 8; catálogo con `nivel_grado_inferido`; firma incluye operativos → **nueva firma `bdedd07f319c`**. 01: cohortes ampliadas a Primaria 6° 2016/18/21/23/25 y Secundaria 5-6° 2016/17/19/22/24 (`ANIOS_PRIM6`/`ANIOS_SEC56`). Resultados 2016–2018 coinciden con los publicados (p. ej. Lengua 6° 2018 = 75,3%). Requiere re-correr el 00 en Colab. |
| 9 | 2026-09-11 | Usuario re-corrió 00 y 01 en Colab: firma `bdedd07f319c` y control de grado OK; **auditoría del Drive** (catálogo idéntico, 57 parquet sin restos viejos, 18 tablas con contenido idéntico al local, Excel con grados corregidos). Colab **truncó** el listado de variables (>5.000 líneas) → 01 reestructurado: C arma catálogo + `variables_disponibles.xlsx/.txt`, D zip, E imprime en 5 celdas. |
