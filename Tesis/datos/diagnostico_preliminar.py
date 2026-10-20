"""Diagnostico preliminar del extracto SIPCOP-M (no ejecuta agrupamiento ni contrastes)."""
import pandas as pd, numpy as np
from scipy import stats
from sklearn.neighbors import NearestNeighbors

MESES = {'enero':1,'febrero':2,'marzo':3,'abril':4,'mayo':5,'junio':6,'julio':7,'agosto':8}
df = pd.read_csv('sipcop_san_sebastian_2025.csv', sep=';', encoding='utf-8-sig', dtype=str)
df['x'], df['y'] = pd.to_numeric(df.x), pd.to_numeric(df.y)
def parse(s):
    m, r = s.split(' ', 1); d, y = r.replace(',', '').split(' ')
    return pd.Timestamp(int(y), MESES[m.lower()], int(d))
df['fecha'] = df.fechaalerta.map(parse)

print('registros:', len(df), '| duplicados exactos:', df.drop(columns='fecha').duplicated().sum())
print('ubicaciones distintas:', df.groupby(['x', 'y']).ngroups)
print('misma fecha+turno+xy (adicionales):', df.duplicated(['fechaalerta', 'turno', 'x', 'y']).sum())
print('origen:\n', df.origen.value_counts().to_string())
print('modalidad exposicion a peligro:', df.modalidad.str.contains('EXPOSICIÓN A PELIGRO').sum())

dias = {m: pd.Period(f'2025-{m:02d}').days_in_month for m in range(1, 9)}; dias[8] = 29
mes = df.fecha.dt.month.value_counts().sort_index()
print('tasa diaria por mes:', (mes / pd.Series(dias)).round(2).to_dict())
exp = np.array([dias[m] for m in range(1, 9)], float); exp = exp / exp.sum() * len(df)
print('chi2 mes vs dias calendario:', stats.chisquare(mes.values, exp))
alld = pd.date_range('2025-01-01', '2025-08-29')
wd = pd.Series(alld.dayofweek).value_counts().sort_index()
ob = df.fecha.dt.dayofweek.value_counts().sort_index()
print('chi2 dia de semana:', stats.chisquare(ob.values, (wd / wd.sum() * len(df)).values))

lat0 = np.deg2rad(-13.533)
X = np.c_[(df.x - df.x.mean()) * 111320 * np.cos(lat0), (df.y - df.y.mean()) * 110574]
for k in (10, 20, 30):
    d, _ = NearestNeighbors(n_neighbors=k + 1).fit(X).kneighbors(X)
    print(f'k={k}: percentiles 10/25/50/75/90 de la k-distancia (m):', np.percentile(d[:, k], [10, 25, 50, 75, 90]).round(0))
