"""Lista las preguntas del cuestionario del estudiante (Solo CC, censal) de cada cohorte comparable y año, con el texto
del diccionario y el % de cada opción. Sirve para ubicar los códigos de una misma pregunta en distintos años (cambian).

Uso (desde la raíz del repo, con datos_consolidados/ generado por el 00):
  python scripts/listar_cuestionario.py            # escribe cuestionario_por_anio.txt (y .parquet) en la raíz
  grep -n -i "########\\|libros" cuestionario_por_anio.txt

Diccionario usado: el del mismo año y nivel (2018/2021/2023 Primaria y 2019/2022 Secundaria están como "General");
Primaria 2025 no tiene diccionario (se muestra "?").
"""
import os, glob
import pandas as pd, pyarrow.dataset as pads

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(R, 'datos_consolidados')
COH = {'Prim': ('Primaria', '6 grado', [2016, 2018, 2021, 2023, 2025]),
       'Sec': ('Secundaria', '5-6 año', [2016, 2017, 2019, 2022, 2024])}
DIC = {('Prim', 2016): (2016, 'Primaria'), ('Prim', 2018): (2018, 'General'), ('Prim', 2021): (2021, 'General'),
       ('Prim', 2023): (2023, 'General'), ('Prim', 2025): (2023, 'General'), ('Sec', 2016): (2016, 'Secundaria'),
       ('Sec', 2017): (2017, 'Secundaria'), ('Sec', 2019): (2019, 'General'), ('Sec', 2022): (2022, 'General'),
       ('Sec', 2024): (2024, 'Secundaria')}
dic = pd.read_parquet(os.path.join(OUT, 'diccionario_aprender.parquet'))
dic['cod'] = dic.variable.str.split('_').str[0].str.lower()

partes = []
for coh, (nivel, grado, anios) in COH.items():
    for a in anios:
        f = ((pads.field('cobertura') == 'Censal') & (pads.field('nivel') == nivel) & (pads.field('grado') == grado)
             & (pads.field('area') == 'Solo CC'))
        t = pads.dataset(sorted(glob.glob(os.path.join(OUT, 'aprender_long', f'anio={a}', '*.parquet'))), format='parquet') \
                .to_table(filter=f, columns=['variable', 'valor']).to_pandas()
        g = t.groupby('variable').valor.sum().reset_index()
        sp = g.variable.str.split('_', n=1)
        g['codigo'], g['opcion'], g['coh'], g['anio'] = sp.str[0], sp.str[1], coh, a
        partes.append(g)
L = pd.concat(partes)
L.to_parquet(os.path.join(R, 'cuestionario_por_anio.parquet'))
with open(os.path.join(R, 'cuestionario_por_anio.txt'), 'w', encoding='utf-8') as fh:
    for (coh, a), g in L.groupby(['coh', 'anio'], sort=False):
        ya, nv = DIC[(coh, a)]
        textos = dic[(dic.anio_dic == ya) & (dic.nivel_dic == nv)].drop_duplicates('cod').set_index('cod').pregunta_texto
        fh.write(f'\n######## {coh} {a} (diccionario {ya} {nv})\n')
        for cod, h in g.groupby('codigo', sort=False):
            tot = h.valor.sum()
            ops = ' | '.join(f'{o}={100 * v / tot:.1f}' for o, v in zip(h.opcion, h.valor))
            fh.write(f'{cod} :: {textos.get(cod.lower(), "?")} :: {ops}\n')
print('Escrito cuestionario_por_anio.txt:', len(L), 'opciones')
