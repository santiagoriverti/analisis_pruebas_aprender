# datos_consolidados/

Salida del notebook [`00_consolidacion.ipynb`](../00_consolidacion.ipynb). **Regenerable**: se reconstruye
por completo corriendo el notebook, por eso los datos pesados (`ra/`, `aprender_long/`, `*.parquet`) están
en `.gitignore`. Se versionan solo las referencias livianas (`diccionario_maestro.xlsx`, `catalogo_archivos.csv`).

## Contenido

| Ruta | Formato | Descripción |
|---|---|---|
| `diccionario_maestro.xlsx` | Excel | Diccionario unificado + catálogo + notas de unidades (6 hojas) |
| `catalogo_archivos.csv` | CSV | Un registro por archivo fuente con atributos parseados (`nivel_grado_inferido` = nivel/grado completados porque el nombre no los trae) |
| `diccionario_ra.parquet` | Parquet | Diccionario RA: `base, campo, tipo_campo, contenido` |
| `diccionario_aprender.parquet` | Parquet | Diccionario APRENDER: `variable → pregunta_texto, opcion_texto` (por año/nivel) |
| `ra/ra_<base>.parquet` (7) | Parquet | Familia RA en formato **ancho**, años 2011–2025 apilados (`anio`) |
| `aprender_long/anio=YYYY/*.parquet` | Parquet (particionado) | Familia APRENDER en formato **largo/tidy** |

## Esquemas

**RA ancho** (`ra/ra_*.parquet`): `anio` + claves (`provincia, departamento, sector, ambito`;
Cargos Bis suma `nivel, tipo, categoria, cargo, planta_tipo`; Matrícula por edad suma `grado`) + columnas
de medida (conteos absolutos). Ver significado en la hoja `Diccionario_RA`.

**APRENDER largo** (`aprender_long/`): `cobertura, nivel, grado, area, jurisdiccion, departamento, sector,
ambito, variable, tipo_variable, valor` (+ `anio` como partición). `valor` = **conteo ponderado de
estudiantes**. `tipo_variable` ∈ {`desempeño`, `contexto`, `nse`, `nivel_educativo_hogar`, `otro`}.
Ver significado de cada `variable` en la hoja `Diccionario_APRENDER`.

## Uso

```python
import pandas as pd
mat     = pd.read_parquet('datos_consolidados/ra/ra_matricula.parquet')
ap_2024 = pd.read_parquet('datos_consolidados/aprender_long', filters=[('anio','==',2024)])
desemp  = pd.read_parquet('datos_consolidados/aprender_long')
desemp  = desemp[desemp.tipo_variable == 'desempeño']
```

> **Unidades:** APRENDER = conteos ponderados (factor de expansión), no porcentajes. RA = conteos absolutos.
> No todas las series son comparables entre años (el operativo cambia de nivel/grado/cobertura).

**Verificación:** la sección 9 del notebook imprime una `firma`; la de referencia es **`bdedd07f319c`**.

**Antes de usar los datos, tener en cuenta** (detalle en [`../ESTADO.md`](../ESTADO.md) §6):
- *Cargos Bis*: `total` mezcla cargos, horas y módulos según `tipo` → filtrar por `tipo` antes de sumar.
- *Trayectoria*: el relevamiento del año *t* informa el ciclo lectivo *t−1*.
- *Características* / *Población*: muchas columnas numéricas vienen como texto → `pd.to_numeric(..., errors='coerce')`.
- APRENDER 2016–2018: `nivel`/`grado` completados por la consolidación (ver `nivel_grado_inferido` en el catálogo).
- APRENDER: desempeño y nivel socioeconómico son conteos separados por celda → no se pueden cruzar entre sí.
- Los nombres de `jurisdiccion` cambian entre años (p. ej. "Buenos aires", "Ciudad de Buenos Aires") → normalizar.

## Guardado en Google Drive (al correr en Colab)

La última celda del notebook (sección 10) guarda una copia en **Mi unidad/`pruebas_aprender`** con dos formatos:

```
pruebas_aprender/
├── parquet/                 # eficiente/tipado — lo leen los notebooks 01 a 04
│   ├── ra/ra_<base>.parquet
│   ├── aprender_long/anio=YYYY/*.parquet
│   └── diccionario_*.parquet
├── excel/                   # legible por humanos
│   ├── diccionario_maestro.xlsx
│   ├── ra_<base>.xlsx        # tablas ≤ 200k filas
│   ├── ra_cargos_bis.csv     # > límite práctico de Excel → CSV
│   ├── ra_matricula_por_edad.csv
│   └── aprender_desempenos.xlsx   # niveles de desempeño por año/área/jurisdicción
└── catalogo_archivos.csv
```

Las tablas que superan las 200.000 filas (Cargos Bis, Matrícula por edad) se exportan a **CSV** (abre en
Excel, sin límite de filas); el resto va a `.xlsx`. El dataset completo de APRENDER (~19 M filas) vive
solo en Parquet; su parte legible es `aprender_desempenos.xlsx`.
