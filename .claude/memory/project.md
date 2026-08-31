# Memoria de proyecto — análisis_pruebas_aprender

> Archivo de memoria para sesiones de Claude Code. Resume estado, decisiones y pendientes.
> Autor/usuario: Santiago Riverti. Los commits van solo con su usuario (sin atribución de Claude).

---

## Qué es

Repositorio de consolidación y análisis de las **Pruebas APRENDER** y la **estadística
educativa** de la Secretaría de Educación de la Nación (Argentina), 2011–2025.

- Local: `C:\Users\sriverti\Desktop\INECO\Repositorios\analisis_pruebas_aprender`
- Remoto: https://github.com/santiagoriverti/analisis_pruebas_aprender
- Rama principal: `main`

## Estado actual (2026-08-31)

- Repo recién inicializado. Solo contenía `README.md` mínimo + carpeta `resultados_aprender/`
  con los datos crudos (161 archivos, 520 MB).
- Trabajo de esta sesión:
  - `.gitignore` creado → excluye `Base_publica_Ap2024.sav` (117 MB, supera el límite de
    100 MB de GitHub) + artefactos Python/Jupyter/OS.
  - `README.md` reescrito con estructura, familias de datos y cobertura por año.
  - `CONTEXTO.md` creado con convenciones de nombrado y decisiones de datos.
  - `.claude/memory/project.md` (este archivo) creado.
- Todavía **no hay código de consolidación ni notebooks**. Los datos están en crudo.

## Datos (resumen)

- `resultados_aprender/`: 156 `.xlsx`, 2 `.sav`, 3 `.pdf`.
- Familia 1 — estadística agregada 2011–2025: Caracteristicas, Cargos, Cargos Bis,
  Matricula, Matricula por edad, Poblacion, Trayectoria.
- Familia 2 — Bases APRENDER 2016–2025 (sin 2020): Censal/Muestral × Primaria/Secundaria ×
  grado × área (Lengua, Matemática, Cs. Naturales, Cs. Sociales, Ciudadanía, Solo CC).
- Microdatos SPSS: `Base_publica_Ap2024.sav` (secundaria, 117 MB, NO versionado) y
  `Base_publica_prim_Ap2024.sav` (primaria, 5,5 MB, sí versionado).

## Decisiones clave

- **Archivo grande fuera de git:** `Base_publica_Ap2024.sav` va al `.gitignore`. No se usa
  Git LFS (por ahora). El resto de las bases sí se versionan.
- **Irregularidades de nombrado** en la fuente hay que normalizarlas al parsear (dobles
  espacios, sufijo `.csv.xlsx`, ausencia de `Censal/Muestral` en años viejos). Ver CONTEXTO.md.
- **Comparabilidad temporal limitada:** el operativo cambia de nivel/grado/cobertura por año.

## Flujo de trabajo

- `.xlsx` → `pandas.read_excel`. `.sav` → `pyreadstat.read_sav`.
- Outputs grandes → `ctx_execute` (context-mode) en vez de consola.
- Commits: usuario Santiago Riverti, sin `Co-Authored-By`.

## Pendiente / próximos pasos

- [ ] Confirmar con el usuario el objetivo analítico concreto (¿qué se quiere consolidar/medir?).
- [ ] Primer commit con README, .gitignore, CONTEXTO y memoria; push a `main`.
- [ ] Diseñar script/notebook de consolidación (parser de nombres → tabla larga tidy).
- [ ] Cargar y explorar diccionarios de variables para mapear columnas entre años.
- [ ] Evaluar armado de series comparables donde el universo lo permita.
