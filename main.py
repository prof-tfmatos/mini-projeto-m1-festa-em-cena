import pandas as pd

df = pd.read_csv("halloween_vendas.csv", dtype=str, keep_default_na=False, encoding="utf-8")
print(df.shape)
print(df.head(3))