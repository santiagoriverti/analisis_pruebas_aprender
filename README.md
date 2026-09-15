# análisis_pruebas_aprender

Consolidación y procesamiento de las bases de datos de las **Pruebas Aprender** y de la
información estadística educativa de la Secretaría de Educación de la Nación (Argentina).

**▶ Ejecutá los notebooks en la nube (sin instalar nada):**

| Notebook | Abrir en Colab |
|---|---|
| **00 · Consolidación** (arma el dataset) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/santiagoriverti/analisis_pruebas_aprender/blob/main/00_consolidacion.ipynb) |
| **01 · Trayectorias** (grafica la evolución) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/santiagoriverti/analisis_pruebas_aprender/blob/main/01_analisis.ipynb) |
| **02 · Brechas** (sector, ámbito y provincia) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/santiagoriverti/analisis_pruebas_aprender/blob/main/02_brechas.ipynb) |
| **03 · Provincias** (evolución reciente y contexto) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/santiagoriverti/analisis_pruebas_aprender/blob/main/03_provincias.ipynb) |

En Colab: abrí el badge y elegí **Entorno de ejecución → Ejecutar todo**.
- El **00** clona el repo, consolida, imprime la **verificación** (`firma`) y guarda en tu Google Drive
  (*Mi unidad/`pruebas_aprender`*), en Parquet (para el 01) y en Excel/CSV (para leer).
- El **01** grafica las trayectorias y, al terminar, **descarga los gráficos en 300 dpi** (zip).
  Requiere haber corrido antes el **00** (lee de tu Drive).
- El **02** analiza las **brechas de desempeño** (estatal/privado, urbano/rural y entre provincias) y descarga
  gráficos + `brechas_aprender.xlsx` (zip). También lee de tu Drive; no necesita el 01.
- El **03** compara la **evolución de cada provincia** en los dos últimos operativos (también frente a provincias de
  nivel inicial similar) y qué cambió en su **contexto**; descarga gráficos + `provincias_contexto.xlsx` (zip). Lee de tu Drive.

**Fuente oficial:**
https://www.argentina.gob.ar/educacion/evaluacion-e-informacion-educativa/datos-abiertos-de-la-secretaria-de-educacion

> **¿Retomás el proyecto en otra PC o sesión?** Empezá por **[ESTADO.md](ESTADO.md)**: estado actual,
> cómo instalar y correr, dónde quedan los resultados, decisiones y próximos pasos.
> Estado: consolidación **completa y validada** (firma de referencia `bdedd07f319c`) , notebooks 01 (trayectorias), 02 (brechas) y 03 (provincias y contexto) funcionando.

---

## Objetivo

Reunir en un único repositorio las bases públicas de evaluación (APRENDER) y las series
estadísticas educativas (matrícula, cargos, población, trayectoria) para su consolidación,
limpieza y análisis a lo largo del tiempo (2011–2025).

## Consolidación (notebook 00)

El notebook [`00_consolidacion.ipynb`](00_consolidacion.ipynb) lee los 156 `.xlsx` de
`resultados_aprender/`, los cataloga, construye un **diccionario maestro** (qué significa y cómo se
expresa cada variable) y los consolida en `datos_consolidados/`:

- **Familia RA** (estadística educativa, 7 bases × 15 años) → 7 Parquet **anchos**, conteos absolutos.
- **Familia APRENDER** (evaluación, 48 archivos) → Parquet **largo/tidy** particionado por año;
  valores = conteos ponderados de estudiantes (factor de expansión).

Se usa Parquet porque varias tablas superan el límite de Excel (1.048.576 filas). El diccionario
maestro sí se entrega en Excel. Instalar dependencias con `pip install -r requirements.txt`.

Para correrlo sin instalar nada, usá el badge de Colab de arriba
([abrir directo](https://colab.research.google.com/github/santiagoriverti/analisis_pruebas_aprender/blob/main/00_consolidacion.ipynb)).

## Trayectorias (notebook 01)

El notebook [`01_analisis.ipynb`](01_analisis.ipynb) muestra la **evolución en el tiempo** (descriptiva)
de las variables más relevantes, respetando la **comparabilidad**:

- **RA (2011–2025)** se releva igual todos los años → **series de tiempo válidas**. Trayectorias incluidas:
  matrícula inicial por nivel, tasa de repitencia, tasa de abandono (por **ciclo lectivo**: la base *Trayectoria*
  del año *t* informa el ciclo *t−1*), cargos docentes por nivel y horas cátedra/módulos (separados por `tipo`).
- **APRENDER** cambia de grado/nivel/cobertura cada año → **solo se compara dentro de la misma cohorte**:
  Primaria 6° Censal (2016/2018/2021/2023/2025) y Secundaria 5-6° Censal (2016/2017/2019/2022/2024). Trayectorias de desempeño
  (% por nivel) en Lengua y Matemática, y por sector (Estatal vs Privado).
- **Al final imprime el listado completo de variables disponibles y su significado** (RA y APRENDER, con años
  de disponibilidad), por partes para que Colab no lo corte, y lo incluye en el zip de descarga como
  `variables_disponibles.xlsx` (filtrable) y `.txt`. Deja `buscar_variable(texto)` para buscar por palabra.

[Abrir en Colab](https://colab.research.google.com/github/santiagoriverti/analisis_pruebas_aprender/blob/main/01_analisis.ipynb).

## Brechas de desempeño (notebook 02)

El notebook [`02_brechas.ipynb`](02_brechas.ipynb) sigue, dentro de las mismas cohortes comparables, cómo evolucionan
las **brechas** en el % Satisfactorio+Avanzado (Lengua y Matemática):

- **Sector:** estatal vs privado (brecha en puntos porcentuales).
- **Ámbito:** urbano vs rural, y cruce sector × ámbito.
- **Provincias:** mapas de calor provincia × año, cambio entre el primer y el último operativo, y dispersión territorial.
- **Límite:** la brecha por **nivel socioeconómico no se puede calcular** con las bases agregadas (traen desempeño y NSE
  por separado, sin su distribución conjunta); requiere microdatos.

[Abrir en Colab](https://colab.research.google.com/github/santiagoriverti/analisis_pruebas_aprender/blob/main/02_brechas.ipynb).

## Evolución provincial y contexto (notebook 03)

El notebook [`03_provincias.ipynb`](03_provincias.ipynb) analiza **cómo cambió cada provincia en los dos últimos
operativos** (Primaria 6° 2023→2025 y Secundaria 5-6° 2022→2024) y **qué cambió en su contexto**:

- Cambio del % Satisfactorio+Avanzado por provincia y cuántas mejoran en cada área.
- **Punto de partida:** las provincias que partían más abajo mejoraron más; por eso compara a cada una con las de
  **nivel inicial similar** y resume su consistencia en las cuatro series.
- **Contexto:** indicadores del cuestionario emparejados entre años (hogar, trayectoria, asistencia, estudio, trabajo,
  clima escolar) y del Relevamiento Anual; compara las provincias que más y menos mejoraron y arma fichas por provincia.
- **Límite:** son asociaciones entre 24 provincias, no causas; el cuestionario de Primaria 2025 no tiene diccionario.

[Abrir en Colab](https://colab.research.google.com/github/santiagoriverti/analisis_pruebas_aprender/blob/main/03_provincias.ipynb).

---

## Estructura del repositorio

```
analisis_pruebas_aprender/
├── README.md                  # este archivo
├── ESTADO.md                  # traspaso: estado, cómo retomar, gotchas, próximos pasos, bitácora
├── CLAUDE.md                  # instrucciones para Claude Code (se cargan solas al abrir el repo)
├── CONTEXTO.md                # contexto de datos: familias, convenciones, diccionarios
├── requirements.txt           # dependencias Python
├── .gitignore                 # excluye la base .sav de 117 MB y la salida pesada regenerable
├── 00_consolidacion.ipynb     # notebook que consolida todo el dataset
├── 01_analisis.ipynb          # notebook de trayectorias (evolución temporal descriptiva)
├── 02_brechas.ipynb           # notebook de brechas (sector, ámbito, provincia)
├── 03_provincias.ipynb        # notebook de evolución provincial reciente y contexto
├── .claude/
│   └── memory/
│       └── project.md         # memoria de proyecto para sesiones de trabajo
├── datos_consolidados/        # SALIDA del notebook 00 (regenerable; datos pesados en .gitignore)
│   ├── README.md              # esquemas y uso de la salida
│   ├── diccionario_maestro.xlsx
│   ├── catalogo_archivos.csv
│   ├── ra/ra_<base>.parquet            # familia RA (ancho)
│   └── aprender_long/anio=YYYY/*.parquet  # familia APRENDER (largo)
├── graficos_trayectorias/     # SALIDA del 01: gráficos + variables_disponibles.xlsx/.txt (no versionado)
├── graficos_brechas/          # SALIDA del 02: gráficos + brechas_aprender.xlsx (no versionado)
├── graficos_provincias/       # SALIDA del 03: gráficos + provincias_contexto.xlsx (no versionado)
└── resultados_aprender/       # datos crudos descargados de la fuente oficial
    ├── 20XX Base APRENDER ... .xlsx      # resultados de las pruebas (2016–2025)
    ├── 20XX Caracteristicas - agregada.xlsx
    ├── 20XX Cargos - agregada.xlsx
    ├── 20XX Cargos Bis - agregada.xlsx
    ├── 20XX Matricula - agregada.xlsx
    ├── 20XX Matricula por edad - agregada.xlsx
    ├── 20XX Poblacion - agregada.xlsx
    ├── 20XX Trayectoria - agregada.xlsx
    ├── Base_publica_Ap2024.sav           # microdato 2024 secundaria (NO versionado, 117 MB)
    ├── Base_publica_prim_Ap2024.sav      # microdato 2024 primaria (5,5 MB)
    ├── *.pdf                             # notas y advertencias metodológicas
    └── Diccionario ... .xlsx             # diccionarios de las bases
```

---

## Familias de datos

### 1. Estadística educativa agregada (2011–2025)
Series anuales por año con siete cortes recurrentes:

| Archivo                          | Contenido |
|----------------------------------|-----------|
| `Caracteristicas - agregada`     | Características de los establecimientos |
| `Cargos - agregada`              | Cargos docentes |
| `Cargos Bis - agregada`          | Cargos docentes (detalle ampliado) |
| `Matricula - agregada`           | Matrícula por nivel |
| `Matricula por edad - agregada`  | Matrícula desagregada por edad |
| `Poblacion - agregada`           | Población de referencia |
| `Trayectoria - agregada`         | Indicadores de trayectoria escolar |

### 2. Bases APRENDER — resultados de evaluación (2016–2025)
Resultados de las pruebas Aprender. El nombre de cada archivo codifica sus dimensiones:

- **Cobertura:** `Censal` / `Muestral` (o `Muestra`)
- **Nivel:** `Primaria` / `Secundaria`
- **Grado/año:** p. ej. `Primaria 6 grado`, `Secundaria 5-6 año`, `Primaria 3 grado`
- **Contenido:** `Desempeños de Lengua`, `Desempeños de Matematica`,
  `Desempeños de Ciencias Naturales`, `Desempeños de Ciencias Sociales`,
  `Desempeños de Ciudadania`, o `Solo CC` (cuestionarios complementarios)

Cobertura por año (resumen):

| Año  | Operativo principal |
|------|---------------------|
| 2016 | Primaria 6 grado y Secundaria 5-6 año (censal) + Primaria 3 grado y Secundaria 2-3 año (muestral) |
| 2017 | Primaria 6 grado (Cs. Naturales/Sociales) y Secundaria 5-6 año (Lengua/Matemática), censal |
| 2018 | Primaria 6 grado (Lengua/Matemática), censal |
| 2019 | Secundaria 5-6 año (censal + muestral) |
| 2021 | Primaria 6 grado (censal) |
| 2022 | Secundaria 5-6 (censal) + Primaria 6 (muestral) |
| 2023 | Primaria 6 grado (censal) |
| 2024 | Secundaria 5-6 (censal) + Primaria 3 (muestral) + microdato `.sav` |
| 2025 | Primaria 6 grado (censal) |

> Nota: 2020 no tuvo operativo APRENDER (pandemia); solo hay estadística agregada.
>
> En 2016–2018 varios nombres de archivo no traen nivel y/o grado. La consolidación los completa y lo verifica
> con la edad más frecuente declarada por los estudiantes (11 años → 6° grado; 17 años → 5-6° año).

### 3. Microdatos públicos y documentación
- `Base_publica_Ap2024.sav` — microdato individual secundaria 2024 (**117 MB, no versionado**).
- `Base_publica_prim_Ap2024.sav` — microdato individual primaria 2024 (5,5 MB).
- `Diccionario ... .xlsx` — diccionarios de variables de las bases.
- `Advertencia metodológica*.pdf`, `Notas metodologicas ... .pdf` — documentación oficial.

---

## Nota sobre el archivo grande (`Base_publica_Ap2024.sav`)

Pesa **117 MB**, por encima del **límite duro de 100 MB por archivo** de GitHub, por lo que
**no puede pushearse**. Está listado en `.gitignore` y se conserva únicamente en local. Para
trabajar con él se recomienda leerlo con `pyreadstat` o `pandas.read_spss`. Si se necesitara
versionar, la alternativa sería Git LFS (no configurado en este repo).

---

## Uso sugerido

Las bases `.xlsx` pueden leerse con `pandas`:

```python
import pandas as pd
df = pd.read_excel("resultados_aprender/2024 Base APRENDER - Censal - Secundaria 5-6 año - Agregada - Desempeños de Lengua.xlsx")
```

Los microdatos `.sav` (SPSS) con `pyreadstat`:

```python
import pyreadstat
df, meta = pyreadstat.read_sav("resultados_aprender/Base_publica_prim_Ap2024.sav")
```
