import pandas as pd

df = pd.read_csv(r'C:\Users\Gerar\Desktop\2021-01-01.csv')
print(df.head())
print(df[df.NombreDePagador == 'NUEVA WAL MART DE MEXICO'])