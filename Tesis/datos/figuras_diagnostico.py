"""Figuras descriptivas del diagnostico preliminar (blanco y negro). No ejecuta agrupamiento ni contrastes.
Uso: python figuras_diagnostico.py  (desde la carpeta datos/; escribe en ../figures/)"""
import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

MESES = {'enero':1,'febrero':2,'marzo':3,'abril':4,'mayo':5,'junio':6,'julio':7,'agosto':8}
ETQ = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago*']
df = pd.read_csv('sipcop_san_sebastian_2025.csv', sep=';', encoding='utf-8-sig', dtype=str)
df['x'], df['y'] = pd.to_numeric(df.x), pd.to_numeric(df.y)
def parse(s):
    m, r = s.split(' ', 1); d, y = r.replace(',', '').split(' ')
    return pd.Timestamp(int(y), MESES[m.lower()], int(d))
df['fecha'] = df.fechaalerta.map(parse); df['mes'] = df.fecha.dt.month
df['expo'] = df.modalidad.str.contains('EXPOSICIÓN A PELIGRO')
plt.rcParams.update({'font.family': 'serif', 'font.size': 9})

# Figura A: ubicaciones distintas, tamano proporcional al numero de registros
g = df.groupby(['x', 'y']).size().reset_index(name='n')
fig, ax = plt.subplots(figsize=(5.6, 4.4))
ax.scatter(g.x, g.y, s=8 + 14 * (g.n - 1) ** 0.85, facecolors='none', edgecolors='black', linewidths=0.6)
ax.set_xlabel('Longitud (°)'); ax.set_ylabel('Latitud (°)')
ax.set_aspect(1 / np.cos(np.deg2rad(-13.53)))
ax.grid(True, color='0.85', linewidth=0.4)
for n in (1, 5, 20):
    ax.scatter([], [], s=8 + 14 * (n - 1) ** 0.85, facecolors='none', edgecolors='black', linewidths=0.6, label=f'{n} registro' + ('s' if n > 1 else ''))
ax.legend(frameon=False, loc='upper left', title='Registros por ubicación', fontsize=8, title_fontsize=8)
fig.tight_layout(); fig.savefig('../figures/diag_ubicaciones.pdf'); plt.close(fig)

# Figura B: tasa diaria por mes y porcentaje de la modalidad de exposicion
dias = {m: pd.Period(f'2025-{m:02d}').days_in_month for m in range(1, 9)}; dias[8] = 29
cnt = df.mes.value_counts().sort_index()
tasa = cnt / pd.Series(dias)
pct = df.groupby('mes').expo.mean() * 100
fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.4, 3.0))
a1.bar(range(8), tasa.values, color='0.55', edgecolor='black', linewidth=0.5)
a1.set_xticks(range(8)); a1.set_xticklabels(ETQ); a1.set_ylabel('Registros por día'); a1.set_title('(a) Tasa diaria de registro')
a2.bar(range(8), pct.values, color='white', edgecolor='black', linewidth=0.7, hatch='///')
a2.set_xticks(range(8)); a2.set_xticklabels(ETQ); a2.set_ylabel('% de los registros del mes'); a2.set_title('(b) Exposición a peligro o abandono')
for a in (a1, a2):
    a.tick_params(axis='x', labelsize=8); a.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); fig.savefig('../figures/diag_mensual.pdf'); plt.close(fig)
print('listo', len(g), 'ubicaciones; tasas', tasa.round(1).tolist())
