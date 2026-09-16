"""Compara hoja por hoja un Excel descargado de Colab contra el generado en local (validación de corridas).

Uso (desde la raíz del repo):
  python scripts/comparar_excel.py <excel_de_colab.xlsx> <excel_local.xlsx>
Ejemplo:
  python scripts/comparar_excel.py ~/Downloads/contexto_estudiantes.xlsx graficos_contexto/contexto_estudiantes.xlsx

Excel por notebook: 02 graficos_brechas/brechas_aprender.xlsx · 03 graficos_provincias/provincias_contexto.xlsx ·
04 graficos_contexto/contexto_estudiantes.xlsx · 05 graficos_asociaciones/asociaciones_desempeno.xlsx ·
06 graficos_microdatos/microdatos_2024.xlsx. (El 07 no genera Excel: comparar el texto de las salidas.)
"""
import sys
import pandas as pd

def comparar(colab, local):
    a, b = pd.read_excel(colab, sheet_name=None), pd.read_excel(local, sheet_name=None)
    ok = list(a) == list(b)
    if not ok:
        print('Hojas distintas:\n  colab:', list(a), '\n  local:', list(b))
    for hoja in b:
        if hoja not in a:
            print(f'FALTA en Colab: {hoja}'); ok = False; continue
        x, y = a[hoja], b[hoja]
        try:
            pd.testing.assert_frame_equal(x, y, check_exact=True)
            print(f'{hoja:35s} {x.shape}  IDÉNTICA')
        except AssertionError:
            try:
                pd.testing.assert_frame_equal(x, y, check_exact=False, rtol=1e-9, atol=1e-9)
                print(f'{hoja:35s} {x.shape}  igual salvo redondeo (< 1e-9)')
            except AssertionError as e:
                ok = False
                print(f'{hoja:35s} colab {x.shape} local {y.shape}  DIFIERE:\n{str(e)[:800]}')
    print('RESULTADO:', 'TODO OK' if ok else 'HAY DIFERENCIAS')
    return ok

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(0 if comparar(sys.argv[1], sys.argv[2]) else 1)
