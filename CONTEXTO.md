# CONTEXTO — análisis_pruebas_aprender

Documento de contexto de datos para orientar el trabajo de consolidación y análisis.
Complementa al `README.md` (visión general) con el detalle de convenciones y decisiones.

---

## 1. Qué son estos datos

Dos orígenes oficiales de la Secretaría de Educación de la Nación (Argentina):

1. **Pruebas APRENDER** — operativo nacional de evaluación de aprendizajes. Bases con
   resultados de desempeño (Lengua, Matemática, Ciencias) y cuestionarios complementarios (CC).
2. **Estadística educativa** — series anuales de matrícula, cargos docentes, población de
   referencia y trayectoria escolar.

Todas las bases `.xlsx` son **agregadas/anonimizadas**. Los `.sav` son **microdato individual**
anonimizado (formato SPSS).

---

## 2. Convención de nombres de las bases APRENDER

El nombre del archivo codifica las dimensiones del operativo:

```
<AÑO> Base APRENDER - <COBERTURA> - <NIVEL> <GRADO> - Agregada - <CONTENIDO>.xlsx
```

- **AÑO:** 2016–2025 (sin 2020).
- **COBERTURA:** `Censal` (todo el universo) | `Muestral` / `Muestra` (muestra representativa).
- **NIVEL:** `Primaria` | `Secundaria`.
- **GRADO:** `3 grado`, `6 grado`, `5-6 año`, `2-3 año`.
- **CONTENIDO:**
  - `Desempeños de Lengua`
  - `Desempeños de Matematica`
  - `Desempeños de Ciencias Naturales`
  - `Desempeños de Ciencias Sociales`
  - `Desempeños de Ciudadania`
  - `Solo CC` → cuestionarios complementarios (contexto socioeducativo, no desempeño)

> Ojo con las irregularidades de nombrado en la fuente:
> - 2016–2018 no siempre traen la palabra `Censal`/`Muestral`.
> - `2019 ... Muestral  - Secundaria` tiene doble espacio.
> - `2024 ... Primaria 3 grado - Agregada - Solo CC.csv.xlsx` arrastra `.csv` en el nombre.
> Estas variaciones hay que normalizarlas al parsear.

---

## 3. Convención de la estadística agregada

```
<AÑO> <CORTE> - agregada.xlsx
```

Cortes: `Caracteristicas`, `Cargos`, `Cargos Bis`, `Matricula`, `Matricula por edad`,
`Poblacion`, `Trayectoria`. Presentes de forma bastante regular en 2011–2025.

---

## 4. Escala de desempeño APRENDER

Los resultados suelen expresarse en **niveles de desempeño**:
`Por debajo del básico`, `Básico`, `Satisfactorio`, `Avanzado`
(verificar etiquetas exactas en el diccionario de cada año, pueden variar).

---

## 5. Decisiones y advertencias

- **`Base_publica_Ap2024.sav` (117 MB)** → excluido de git (`.gitignore`) por superar el
  límite de 100 MB de GitHub. Vive solo en local.
- **Comparabilidad temporal:** los operativos cambian de nivel/grado/cobertura año a año, por
  lo que **no todas las series son directamente comparables**. Verificar universo antes de
  comparar (ver notas metodológicas en los PDF).
- **2020 sin APRENDER** por la pandemia.
- Consultar siempre los diccionarios (`Diccionario ... .xlsx`) y las advertencias
  metodológicas antes de interpretar resultados.

---

## 6. Herramientas sugeridas

- `.xlsx` → `pandas.read_excel` (motor `openpyxl`).
- `.sav` → `pyreadstat.read_sav` (devuelve datos + metadatos con etiquetas) o `pandas.read_spss`.
- Para outputs grandes, usar `ctx_execute` (context-mode) en vez de imprimir en consola.
