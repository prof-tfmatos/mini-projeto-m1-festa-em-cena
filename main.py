# peça 1: traz a biblioteca
import pandas as pd

# peça 2: lê o CSV numa tabela (DataFrame), tudo como texto
df = pd.read_csv("halloween_vendas.csv", dtype=str, keep_default_na=False, encoding="utf-8")

# peça 3: confere: 1500 linhas x 14 colunas
print(df.shape)
print(df.head(3))

# peça 4: tabela vira lista de dicts (um dict por pedido)
registros = df.to_dict(orient="records")
print(len(registros))
print(registros[0])