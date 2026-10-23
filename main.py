# peça 1: traz a biblioteca 
import pandas as pd
# traz o regex
import re

# peça 2: lê o CSV numa tabela (DataFrame), tudo como texto
df = pd.read_csv("halloween_vendas.csv", dtype=str, keep_default_na=False, encoding="utf-8")

# peça 3: confere: 1500 linhas x 14 colunas
print(df.shape)
print(df.head(3))

# peça 4: tabela vira lista de dicts (um dict por pedido)
registros = df.to_dict(orient="records")
print(len(registros))
print(registros[0])

# peça 5: limpar a categoria dos 1500 registros e contar
vazias = 0
alteradas = 0

for registro in registros:
    original = registro["categoria"]
    limpa = original.strip()
    limpa = limpa.lower()
    limpa = re.sub(r"[^a-z ]", "", limpa)

    if limpa == "":
        limpa = "sem categoria"
        vazias += 1
    elif limpa != original.lower():    # troca de caixa não conta
        alteradas += 1

    registro["categoria"] = limpa

print("vazias:", vazias)          # alvo: 18
print("alteradas:", alteradas)    # alvo: 131


# peça 6: padronizar o canal de venda com um dict tradutor
tradutor = {
    "mercado": "Mercado",
    "loja física": "Loja física",
    "web": "Web",
}
padronizados = 0
desconhecidos = 0

for registro in registros:
    original = registro["canal_venda"]
    chave = original.strip().lower()

    if chave in tradutor:
        novo = tradutor[chave]
        if novo != original:
            padronizados += 1
        registro["canal_venda"] = novo
    else:
        desconhecidos += 1

print("canais padronizados:", padronizados)    # alvo: 45
print("canais desconhecidos:", desconhecidos)  # alvo: 0

# peça 8: quantidade (inteiro > 0) e preço (preenchido, >= 0): marcar sem inventar
qtd_invalidas = 0
preco_invalidos = 0
pedidos_com_problema = set()    # {} vazio seria dict

for registro in registros:
    pedido = registro["pedido_id"]

    # quantidade: falha no int() OU converte mas não é > 0 ("-1" converte sem erro)
    try:
        qtd = int(registro["quantidade"])
        qtd_ok = qtd > 0
    except ValueError:
        qtd_ok = False
    if not qtd_ok:
        qtd_invalidas += 1
        pedidos_com_problema.add(pedido)

    # preço: float("") levanta ValueError; negativo converte mas não passa
    try:
        preco = float(registro["preco_unitario"])
        preco_ok = preco >= 0
    except ValueError:
        preco_ok = False
    if not preco_ok:
        preco_invalidos += 1
        pedidos_com_problema.add(pedido)

    # o valor original fica como está: nada de trocar por 0 ou média

print("quantidades inválidas:", qtd_invalidas)               # alvo: 7
print("preços inválidos:", preco_invalidos)                  # alvo: 12
print("pedidos com problema:", len(pedidos_com_problema))    # alvo: 19