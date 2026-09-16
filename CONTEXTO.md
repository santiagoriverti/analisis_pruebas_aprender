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
> - 2016–2017 no traen el **grado** y 2018 no trae **ni nivel ni grado**; 2016 escribe `3grado` sin espacio.
>   El notebook 00 completa: 2016/2017 Primaria = `6 grado`, Secundaria = `5-6 año`; 2018 = Primaria `6 grado`
>   (verificado por edad modal declarada: 11 años / 17 años). Columna `nivel_grado_inferido` del catálogo.
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

- `.xlsx` → `pandas.read_excel(..., engine='calamine')` (5-10x más rápido que openpyxl; necesario
  para los APRENDER de 1000+ columnas).
- `.sav` → `pyreadstat.read_sav` (datos + metadatos con etiquetas) o `pandas.read_spss`.
- Para outputs grandes, usar `ctx_execute` (context-mode) en vez de imprimir en consola.

## 7. Consolidación (notebook 00)

El notebook `00_consolidacion.ipynb` deja todo en `datos_consolidados/`:

- **RA → ancho** (7 parquet, un base por archivo, años apilados). Conteos absolutos.
- **APRENDER → largo/tidy** (particionado por año). Conteos ponderados; columna `tipo_variable`
  distingue `desempeño` / `contexto` / `nse` / `nivel_educativo_hogar` / `otro`.
- **`diccionario_maestro.xlsx`** — significado y unidad de cada variable (join por `variable`/`campo`).
- **Nivel/grado 2016–2018:** se completan cuando el nombre del archivo no los trae (verificado por edad modal;
  columna `nivel_grado_inferido` del catálogo). Firma de verificación de referencia: `bdedd07f319c`.

Detalle de esquemas y ejemplos de uso en `datos_consolidados/README.md`.

## 8. Análisis (notebooks 01 a 06)

- **`01_analisis.ipynb` — trayectorias:** series RA (matrícula, repitencia y abandono por **ciclo lectivo**,
  cargos docentes, horas y módulos) y desempeño APRENDER en las cohortes comparables (Primaria 6° Censal
  2016/2018/2021/2023/2025; Secundaria 5-6° Censal 2016/2017/2019/2022/2024). Genera el catálogo
  `variables_disponibles.xlsx` con todas las variables y su significado.
- **`02_brechas.ipynb` — brechas:** % Satisfactorio+Avanzado por sector, ámbito y provincia en esas cohortes.
- **`03_provincias.ipynb` — evolución provincial y contexto:** cambio por provincia en los dos últimos operativos
  (Prim 2023→2025, Sec 2022→2024), comparación con provincias de nivel inicial similar y cambios de contexto asociados
  (cuestionario CC emparejado entre años + Relevamiento Anual). Usa parte de la selección de §10 para ese período.
- **`04_contexto.ipynb` — contexto del estudiante en el tiempo:** implementa §10.A1–A6 (+ sobreedad) en las cohortes
  completas y §10.C1–C4 del RA. Especificación por año en `IND` (código, opciones, etiqueta de redacción); tabla
  `preguntas_por_anio`. Primaria 2025: acceso digital y trabajo **no identificables** (varias preguntas candidatas con
  perfil provincial parecido; no se imputan).
- **`05_asociaciones.ipynb` — asociaciones:** ρ de Spearman entre provincias del cambio de indicadores (cuestionario + RA:
  docentes por alumno, horas, vacantes, titulares) y del cambio de desempeño en ventanas comparables; frente a pares y nivel
  vs nivel; permutaciones + Benjamini-Hochberg. Descriptivo: asociación, no causa.
- **`06_microdatos.ipynb` — microdatos 2024:** implementa §10.D (desempeño × contexto por estudiante), sector a igual
  contexto y provincias estandarizadas (educación de la madre × libros en Secundaria; NSE de escuela en Primaria 3°).
- **Advertencias de interpretación clave:**
  - *Cargos Bis*: `total` mezcla cargos, horas cátedra y módulos → separar por `tipo`.
  - Base *Trayectoria* del año *t* = ciclo lectivo *t−1*.
  - El nivel socioeconómico **no** se puede cruzar con el desempeño en las bases agregadas (solo con microdatos).
  - Matemática Secundaria 2022 sin nivel Avanzado; Chubut sin datos en Secundaria 2019; no hay diccionario 2025.
- Lista completa de trampas y números de control: `ESTADO.md` (§5 y §6).

---

## 9. Microdatos APRENDER 2024 (`.sav`)

Son los **únicos microdatos a nivel estudiante** del repo (la advertencia metodológica los presenta como un "nuevo
producto"; no hay equivalentes descargables de otros años: los microdatos completos de todos los años solo se consultan
en el escritorio virtual de la Subsecretaría). Leer con `pyreadstat.read_sav` (está en `requirements.txt`).

| Archivo | Operativo | Tamaño | Filas × columnas | En git |
|---|---|---|---|---|
| `Base_publica_Ap2024.sav` | Secundaria 5-6° año, censal | 117 MB | 386.882 × 22 | **No** (límite de GitHub) |
| `Base_publica_prim_Ap2024.sav` | Primaria 3° grado (alfabetización), muestral | 5,6 MB | 91.264 × 24 | Sí |

**Secundaria** (sin etiquetas SPSS; los valores ya vienen como texto):
`jurisdiccion` (24) · `sector` · `ambito` · `ID_colegio` (11.947) · `ID_seccion` · `ID_alumno` · `lpuntaje` · `mpuntaje` ·
`ldesemp` / `mdesemp` (4 niveles) · `Edad` (17 o menos / 18 / 19 o más) · `Sexo` · `Nivel_Ed_MadreX` (hasta secundaria
incompleta / hasta terciario-universitario incompleto / terciario-universitario-posgrado completo) · `ap16g` computadora ·
`ap15` espacio tranquilo para estudiar · `ap17` cantidad de baños · `ap19X` libros (<6 / 6–50 / >50) · `ap25aX` repitencia
en primaria · `ap31X` horas de estudio fuera de la escuela · `ponder` (contexto) · `ponderL` · `ponderM`.
**No trae nivel socioeconómico.**

**Primaria 3°** (con etiquetas): `jurisdiccion` · `sector` (sin ámbito) · IDs · `lpuntaje` · `ldesemp` (Lector incipiente,
Nivel I–V) · `Edad` · `Sexo` · `NSE_escuela` (Bajo, Medio Bajo, Medio, Medio Alto, Alto) · `Jardin` (sala de 3 / sala de 4 /
sala de 5 o no asistió) · `Repitencia` · `Libros` (≤20 / >20) · `ap08` celular propio · `ap11` la familia pregunta qué hizo
en la escuela · `ap12` la familia ayuda con la tarea · `ap13` le gusta la escuela · `ap15a–d` relación con la maestra ·
`ap17` alguien le lee en casa · `ponder` · `ponderL` (llegan a ~390: **usar siempre los ponderadores**).

**Control (2026-09-14)** — % ponderado igual a las bases agregadas: Secundaria Lengua Satisf+Avanz 57,0 (agregado 56,9),
Por debajo del básico 22,4; Matemática Satisf+Avanz 17,6, Por debajo 54,3. Primaria 3° lectura: Lector incipiente 3,4 ·
Nivel I 8,3 · II 18,8 · III 24,5 · IV 26,3 · V 18,7.

**Anonimización (control de divulgación estadística):** ruido aleatorio de media cero en puntajes y ponderadores (no cambia
medias ni niveles de desempeño); recategorización de variables; sexo "X" repartido al azar entre las otras dos categorías;
a <10 % de los alumnos se les reasignó el código de colegio → **evitar análisis por escuela individual**.

**Para qué sirven:** cruzar desempeño × contexto **por estudiante** (imposible con los agregados), pero solo en 2024 y con
pocas variables. Primaria 3° trae `NSE_escuela`; en Secundaria hay que usar proxies (educación de la madre, libros,
computadora, baños). Para evolución en el tiempo se usan los agregados (notebooks 01 a 04). Análisis: `06_microdatos.ipynb`
(en Colab lee los zip oficiales `2024 Base de microdatos Aprender primaria.zip` y `2024 Base de microdatos Aprender secundaria.zip` desde *Mi unidad/`pruebas_aprender`*).

### Riqueza de datos por año (bases agregadas APRENDER)

| Año | Operativos | Filas | Variables | Áreas con desempeño |
|---|---|---|---|---|
| 2016 | 4 (Prim 6° y 3°, Sec 5-6° y 2-3°) | 3,79 M | 1.225 | Lengua, Matemática, Cs. Naturales, Cs. Sociales |
| 2017 | 2 | 2,97 M | 943 | Lengua, Matemática, Cs. Naturales, Cs. Sociales |
| 2018 | 1 | 1,08 M | 370 | Lengua, Matemática |
| 2019 | 2 | 2,33 M | 779 | Lengua, Matemática, Cs. Naturales, Ciudadanía |
| 2021 | 1 | 1,74 M | 588 | Lengua, Matemática |
| 2022 | 2 | 2,18 M | 888 | Lengua, Matemática |
| 2023 | 1 | 1,78 M | 544 | Lengua, Matemática |
| 2024 | 2 (Sec 5-6° censal, Prim 3° muestral) | 1,71 M | 657 | Lengua, Matemática |
| 2025 | 1 | 1,14 M | 354 | Lengua, Matemática |

2024 **no** tiene más datos agregados que otros años (el año más rico es 2016). Todos llegan a departamento (~430). Lo
único propio de 2024 son los microdatos por estudiante. El NSE existe como tipo `nse` desde 2019 y como índice
`isocioa`/`ICSE` en 2016–2018, pero en los agregados nunca es cruzable con desempeño.

---

## 10. Variables de interés para desarrollar (selección 2026-09-14)

Criterio: análisis **descriptivo**, priorizando lo que se puede seguir en el tiempo dentro de las cohortes comparables
**Primaria 6° (2016·18·21·23·25)** y **Secundaria 5-6° (2016·17·19·22·24)**. Los códigos cambian por año: buscarlos con
`buscar_variable("…")` o en `variables_disponibles.xlsx` (hoja `APRENDER_preguntas`).

**Reglas generales:** (1) en los agregados estas variables **no se cruzan con desempeño por estudiante**, solo se comparan a
nivel provincia/departamento; (2) usar `area == 'Solo CC'` como cuestionario canónico (las preguntas se repiten en las
áreas); (3) en 2016–2018 excluir "Blanco / Dato faltante / Multimarca"; (4) 2025 no tiene diccionario: validar el
significado de los códigos; (5) armonizar categorías antes de comparar años.

### A. Contexto del estudiante con serie en el tiempo (APRENDER) — prioridad alta

| # | Variable (búsqueda) | Años | Qué mostraría | Cuidado |
|---|---|---|---|---|
| A1 | **Repitencia** ("repetiste") | Prim 6°: los 5 · Sec: los 5 (repitencia en primaria) | Evolución de la repitencia declarada; contraste con RA | Categorías Nunca/Una vez… vs Sí/No |
| A2 | **Asistencia al jardín** ("jardín", "nivel inicial") | Prim 6°: los 5 (2025 sin diccionario) · Sec: los 5 | Expansión del nivel inicial por generación | Armonizar sala 3 / 4 / 5 / no asistió |
| A3 | **Nivel educativo de madre y padre** ("nivel educativo") | Los 5 en ambas cohortes | Clima educativo del hogar | Redacción distinta 2016–19 vs 2021+ (tipo `nivel_educativo_hogar`) |
| A4 | **Libros en el hogar** ("libros") | Prim 2018·21·23·25 · Sec 2017·19·22·24 | Capital cultural | Rangos distintos: agrupar grueso |
| A5 | **Internet / computadora / celular en el hogar** ("internet", "computadora", "celular") | Sec: los 5 · Prim 2016·18·21·23 | Brecha digital pre/post pandemia | Sí/No vs cantidad |
| A6 | **Trabajo y tareas de cuidado** ("trabaj", "cuid", "tareas del hogar") | Sec: los 5 · Prim 2016·18·21·23 | Trabajo infantil/adolescente y carga de cuidados | Escalas de frecuencia muy distintas |
| A7 | **Inasistencias y motivos** ("faltaste", "inasistencias") | Sec: los 5 · Prim 2016·21·23 | Ausentismo y causas (período menstrual desde 2022) | Tramos cambian |
| A8 | **¿Te gusta ir a la escuela?** | Prim 6° 2018·21·23·25 | Vínculo con la escuela | Pregunta estable |
| A9 | **Autopercepción** ("cómo leés", "escribís", "resolvés") | Prim 2016·18·21·23·25 · Sec 2024 | Percepción vs desempeño provincial | Solo comparación agregada |
| A10 | **Convivencia, bullying, discriminación** ("discrimin", "burlan", "agred") | Prim 2018·21·23 · Sec: los 5 | Clima escolar | Redacción muy variable: indicativo |
| A11 | **Proyectos al terminar la secundaria** ("termines el secundario", "proyectos inmediatos") | Sec 2017·19·22·24 | Estudiar / trabajar / nuevas expectativas (contenidos, videojuegos) | — |
| A12 | **Hijos / embarazo adolescente** ("hijos", "embarazada") | Sec: los 5 | Maternidad y paternidad en secundaria | — |
| A13 | **Sobreedad** (tipo `otro`) y **migración** ("migra") | 2019–2025 · 2017–2025 | Complemento del RA; composición migrante | Migración cambia de definición en 2021 |

### B. Fotos puntuales (un año) muy relevantes
- **Pandemia:** Prim 2021 (asistencia presencial 2020/2021, clases virtuales, motivos de no conexión); Sec 2022 (impacto en
  aprendizajes, qué valoraron de la vuelta a la presencialidad).
- **Salud mental y entorno digital, Sec 2024:** estados de ánimo (ap42), redes sociales (ap40), control parental y
  **apuestas online** (ap41l).
- **Programa "Libros para Aprender":** Prim 2022 y 2023.
- **ESI:** Prim 2018·21·23; Sec 2019·22.
- **Espacio tranquilo y horas de estudio:** Prim 2021–23; Sec 2022·24.
- **Índices construidos:** clima escolar (2016–17, 2024), ICSE (2017–18), infraestructura (2019).

### C. Relevamiento Anual (serie 2011–2025, provincia/departamento)
- **C1** Sobreedad por año de estudio (`s_1…s_12` / `_1…_12` de Matrícula).
- **C2** Egresados de primaria y secundaria (y mujeres): aproximación a terminalidad.
- **C3** Abandono y repitencia por año de estudio y provincia (el 01 solo lo muestra por nivel).
- **C4** Brecha de género en trayectorias (columnas `m_*` de Trayectoria, `v_*` de Matrícula).
- **C5** Nivel inicial: salas de 3 y 4; "alumnos que nunca asistieron a sala de 5" (Población).
- **C6** Jornada completa / extendida en primaria (Población).
- **C7** Comedor escolar: beneficiarios de almuerzo, desayuno, merienda (nombres de columna cambian en 2019).
- **C8** Conectividad de escuelas: internet, tipo de conexión, **conexión en aulas** (2014–2025; columnas como texto).
- **C9** Estudiantes extranjeros por origen (Venezuela desde 2014), población indígena, discapacidad con/sin apoyo (2019–2025).
- **C10** Cargos no cubiertos (vacancia docente) y alumnos por cargo frente a alumnos.
- **C11** Plurigrado: secciones múltiples (clave rural).

### D. Microdatos 2024 — cruces con desempeño
- **Secundaria:** Lengua/Matemática × educación de la madre, libros, computadora, horas de estudio, repitencia en primaria.
- **Primaria 3°:** nivel de lectura × `NSE_escuela`, jardín, libros, lectura en el hogar, gusto por la escuela.

**Prioridad sugerida:** A1–A6 + C1–C4 → **implementado en `04_contexto.ipynb`** (2026-09-16; validado en Colab); D → capítulo
aparte de brechas por NSE/contexto con microdatos 2024 → **implementado en `06_microdatos.ipynb`** (2026-09-16). Quedan sin desarrollar A7–A13, B y C5–C11.
