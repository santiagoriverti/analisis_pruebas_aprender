# análisis_pruebas_aprender

Consolidación y procesamiento de las bases de datos de las **Pruebas Aprender** y de la
información estadística educativa de la Secretaría de Educación de la Nación (Argentina).

**▶ Ejecutá el notebook de consolidación en la nube (sin instalar nada):**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/santiagoriverti/analisis_pruebas_aprender/blob/main/00_consolidacion.ipynb)

En Colab: abrí el badge y elegí **Entorno de ejecución → Ejecutar todo**. El notebook clona este
repositorio, procesa todo, imprime un bloque de **verificación** (con una `firma`) para confirmar que
compiló sin errores, y **guarda los resultados en tu Google Drive** (*Mi unidad/`pruebas_aprender`*),
en Parquet (para el notebook 01) y en Excel/CSV (para leer).

**Fuente oficial:**
https://www.argentina.gob.ar/educacion/evaluacion-e-informacion-educativa/datos-abiertos-de-la-secretaria-de-educacion

> **¿Retomás el proyecto en otra PC o sesión?** Empezá por **[ESTADO.md](ESTADO.md)**: estado actual,
> cómo instalar y correr, dónde quedan los resultados, decisiones y próximos pasos.
> Estado: consolidación **completa y validada** (firma de referencia `c9740263478b`). Sigue: notebook 01 de análisis.

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
  matrícula inicial por nivel, tasa de repitencia, tasa de abandono, cargos docentes.
- **APRENDER** cambia de grado/nivel/cobertura cada año → **solo se compara dentro de la misma cohorte**:
  Primaria 6° Censal (2021/2023/2025) y Secundaria 5-6° Censal (2019/2022/2024). Trayectorias de desempeño
  (% por nivel) en Lengua y Matemática, y por sector (Estatal vs Privado).

[Abrir en Colab](https://colab.research.google.com/github/santiagoriverti/analisis_pruebas_aprender/blob/main/01_analisis.ipynb).

---

## Estructura del repositorio

```
analisis_pruebas_aprender/
├── README.md                  # este archivo
├── ESTADO.md                  # traspaso: estado, cómo retomar, próximos pasos
├── CONTEXTO.md                # contexto de datos: familias, convenciones, diccionarios
├── requirements.txt           # dependencias Python
├── .gitignore                 # excluye la base .sav de 117 MB y la salida pesada regenerable
├── 00_consolidacion.ipynb     # notebook que consolida todo el dataset
├── 01_analisis.ipynb          # notebook de trayectorias (evolución temporal descriptiva)
├── .claude/
│   └── memory/
│       └── project.md         # memoria de proyecto para sesiones de trabajo
├── datos_consolidados/        # SALIDA del notebook 00 (regenerable; datos pesados en .gitignore)
│   ├── README.md              # esquemas y uso de la salida
│   ├── diccionario_maestro.xlsx
│   ├── catalogo_archivos.csv
│   ├── ra/ra_<base>.parquet            # familia RA (ancho)
│   └── aprender_long/anio=YYYY/*.parquet  # familia APRENDER (largo)
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
| 2016 | Primaria y Secundaria (censal + muestral) |
| 2017 | Primaria y Secundaria |
| 2018 | Primaria (Lengua/Matemática) |
| 2019 | Secundaria 5-6 año (censal + muestral) |
| 2021 | Primaria 6 grado (censal) |
| 2022 | Secundaria 5-6 (censal) + Primaria 6 (muestral) |
| 2023 | Primaria 6 grado (censal) |
| 2024 | Secundaria 5-6 (censal) + Primaria 3 (muestral) + microdato `.sav` |
| 2025 | Primaria 6 grado (censal) |

> Nota: 2020 no tuvo operativo APRENDER (pandemia); solo hay estadística agregada.

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
