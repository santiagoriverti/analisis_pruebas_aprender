# datos_consolidados/

Salida del notebook [`00_consolidacion.ipynb`](../00_consolidacion.ipynb). **Regenerable**: se reconstruye
por completo corriendo el notebook, por eso los datos pesados (`ra/`, `aprender_long/`, `*.parquet`) están
en `.gitignore`. Se versionan solo las referencias livianas (`diccionario_maestro.xlsx`, `catalogo_archivos.csv`).

## Contenido

| Ruta | Formato | Descripción |
|---|---|---|
| `diccionario_maestro.xlsx` | Excel | Diccionario unificado + catálogo + notas de unidades (6 hojas) |
| `catalogo_archivos.csv` | CSV | Un registro por archivo fuente con atributos parseados |
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
