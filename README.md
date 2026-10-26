# Festa em Cena — Mini-Projeto M1.1

## Problema e objetivo

A Festa em Cena é uma rede fictícia que comercializa fantasias e acessórios de Halloween pelos canais Mercado, Loja física e Web. A base de
dados da empresa apresenta ruídos de registro: categorias vazias ou com pontuações indevidas, diferenças de grafia e caixa nos nomes dos
canais, quantidades zeradas ou negativas, preços unitários ausentes ou negativos e datas de venda inválidas. Se a gestão contasse os pedidos
diretamente na base bruta, o mesmo canal de venda seria dividido em múltiplos grupos e registros com datas corrompidas distorceriam a análise
temporal. O objetivo deste programa é higienizar e validar os registros em Python, marcando inconsistências sem inventar valores, para
entregar um relatório confiável antes que a gestão compare os períodos de venda de 2024 e 2025.

## O que é uma linha

Cada linha do arquivo `halloween_vendas.csv` representa um pedido único referente a um único produto. Como um mesmo pedido pode conter
várias unidades compradas daquele item, a contagem de linhas reflete a quantidade de pedidos registrados, e não o volume total de unidades
físicas vendidas. Ao todo, a base reúne 1.500 pedidos distintos distribuídos entre os meses de agosto a novembro de 2024 e de 2025,
estruturados em 14 colunas.

## Colunas escolhidas

| coluna | o que guarda | exemplo |
|---|---|---|
| `categoria` | Tipo do item de Halloween vendido no pedido | `Fantasia` (pedido 844) |
| `canal_venda` | Canal pelo qual o pedido foi realizado (`Mercado`, `Loja física` ou `Web`) | `Loja física` (pedido 844) |
| `quantidade` | Número de unidades daquele produto compradas no pedido | `3` (pedido 844) |
| `data_venda` | Data e horário em que o pedido foi registrado no sistema | `2025-11-21 18:02:35` (pedido 844) |

## Regras de limpeza

### Textos

- **Categoria (`categoria`):** aplicação sequencial de `strip()` (remoção de espaços nas bordas), `lower()` (conversão para minúsculas) e
`re.sub(r"[^a-z ]", "", limpa)` para manter apenas letras de `a` a `z` e o espaço interno (essencial para preservar nomes compostos e o
próprio rótulo `"sem categoria"` sem colar as palavras).
- **Categorias vazias:** se o texto original era vazio ou ficou vazio após a remoção de símbolos pelo regex, recebe o valor padronizado
`"sem categoria"`.
- **Critério de categoria alterada:** só é contabilizada como alterada quando o conteúdo muda além da simples diferença de caixa (`limpa !=
original.lower()`), evitando inflar a contagem com registros que apenas começavam com letra maiúscula (por isso o total é 131 alteradas, e não
1.482).
- **Canal de venda (`canal_venda`):** remoção de espaços nas pontas e conversão para minúsculas (`strip().lower()`) para consulta em um
dicionário tradutor, convertendo as variações para os três nomes canônicos: `Mercado`, `Loja física` e `Web`.

### Valores

- **Quantidade válida (`quantidade`):** deve ser convertível para inteiro (`int`) e estritamente maior que zero (`> 0`).
- **Preço unitário válido (`preco_unitario`):** deve estar preenchido, ser convertível para ponto flutuante (`float`) e ser não negativo
(`>= 0`).
- **Tratamento de exceções (`try/except`):** a conversão numérica usa blocos `try/except ValueError` para que o programa capture falhas de
texto ou campos vazios e continue a execução sem interromper o processamento.
- **Marcação sem imputação:** valores inválidos são apenas contados e marcados; o valor original no registro é preservado intacto, sem
substituir por zero ou pela média.
- **Contagem de pedidos com problema:** uso de um conjunto (`set`) guardando o `pedido_id` para garantir que um pedido com erro simultâneo
em quantidade e preço seja contado apenas uma vez.

### Datas

- **Conversão (`data_venda`):** validação e parsing com `datetime.strptime(texto, "%Y-%m-%d %H:%M:%S")` dentro de um bloco `try/except
ValueError`.
- **Preservação e enriquecimento:** o texto original de `data_venda` é mantido intacto no dicionário do pedido; quando a data é válida
(`data_ok = True`), são extraídos ao lado os campos `ano`, `mes`, `dia`, `hora`, a data no formato brasileiro com `strftime("%d/%m/%Y")` e a
chave `ano_mes` (`strftime("%Y-%m")`).
- **Datas inválidas:** quando o parsing falha (`data_ok = False`), a data inválida é apenas marcada e contabilizada, nunca sendo substituída
pela data atual (`datetime.now()`).

## Como executar

1. Certifique-se de que os arquivos necessários (`main.py`, `halloween_vendas.csv` e `requirements.txt`) estejam todos **na mesma pasta**.
2. No terminal, dentro da pasta do projeto, crie e ative o ambiente virtual, instale as dependências listadas no `requirements.txt` e
execute o script principal:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
## Resultados

| item | valor |
|---|---|
| linhas lidas | 1.500 (14 colunas) |
| categorias vazias preenchidas | 18 |
| categorias alteradas no conteúdo | 131 |
| canais padronizados | 45 (0 desconhecidos) |
| quantidades inválidas | 7 |
| preços inválidos | 12 |
| pedidos com problema numérico | 19 |
| datas inválidas | 4 |
| pedidos sem data de entrega | 143 |
| cancelados entre os sem entrega | 109 |
| outros status entre os sem entrega | 34 |
| Web | 666 (44,4%) |
| Loja física | 551 (36,7%) |
| Mercado | 283 (18,9%) |
| excluídos da contagem por canal | 0 |
| ano-mês | 2024-08: 77 · 2024-09: 104 · 2024-10: 393 · 2024-11: 174 · 2025-08: 62 · 2025-09: 94 · 2025-10: 410 · 2025-11: 182 |
| excluídos da contagem por ano-mês | 4 (data inválida) |

## Pedidos sem data de entrega

Investigou-se a hipótese de que todos os registros com data_entrega vazia teriam status_pedido igual a Cancelado. Ao separar os 143 pedidos
sem data de entrega, foram encontrados 109 com status Cancelado e 34 com outros status.

A conclusão é que a hipótese é falsa na base, pois em uma afirmação universal ("todos") basta um único contraexemplo para refutá-la. O main.py
exibe o primeiro contraexemplo encontrado, o que já é suficiente para derrubar a hipótese: o pedido 1170, que está sem data de entrega, mas
possui status Concluído (venda em 2025-08-19 22:20:19).

## Descobertas

### Descoberta 1 — por canal

- Número: Dos 1.500 pedidos válidos analisados (0 excluídos), o canal Web lidera com 666 pedidos (44,4%), seguido por Loja física com 551
pedidos (36,7%) e Mercado com 283 pedidos (18,9%).
- Interpretação: A liderança do canal Web sugere que o comércio eletrônico é a principal porta de entrada de pedidos da Festa em Cena,
concentrando quase metade das transações registradas.
- Limitação: Essa contagem representa apenas pedidos registrados (incluindo cancelados e devolvidos), e não unidades físicas vendidas ou
receita financeira efetiva; além disso, trata-se de uma base fictícia que não reflete o mercado real.

### Descoberta 2 — por período

- Número: Dos 1.496 pedidos com data válida (4 excluídos por data inválida), há um pico acentuado em outubro nos dois anos: 393 pedidos em
2024-10 (~52,5% dos 748 pedidos válidos de 2024) e 410 pedidos em 2025-10 (~54,8% dos 748 pedidos válidos de 2025). Agrupar por ano-mês (e não
apenas pelo mês isolado) foi fundamental para não misturar 2024 e 2025 e permitir comparar a evolução entre os dois anos.
- Interpretação: A concentração de mais da metade dos pedidos em outubro é explicada pela sazonalidade direta do Halloween (celebrado em 31 de
outubro), mostrando que a demanda se intensifica nas semanas que antecedem a data comemorativa e recua em novembro.
- Limitação: O número de pedidos não equivale ao faturamento nem ao total de itens vendidos (pois um pedido pode ter várias unidades e
diferentes preços), e os dados cobrem apenas uma janela sazonal (agosto a novembro) de uma empresa fictícia.

## Reflexão: ML e qualidade de dados

Em projetos de ciência de dados e Machine Learning, vale o princípio de que "lixo entra, lixo sai" (garbage in, garbage out). Se um modelo ou
relatório fosse alimentado com esta base sem limpeza prévia, variações de grafia como 'web', 'Web' e ' web ' seriam tratadas como três canais
distintos, fragmentando as contagens e distorcendo os padrões aprendidos pelo algoritmo.

Por outro lado, limpar os dados é condição necessária, mas não garante, sozinha, que um modelo evite overfitting (sobreajuste ao ruído da
amostra) ou underfitting (incapacidade de capturar o padrão). A qualidade preditiva também depende da representatividade dos dados, da escolha
adequada do algoritmo e de uma avaliação correta. Por exemplo, como esta base contém apenas vendas de agosto a novembro voltadas para o
Halloween, ela não é representativa para prever vendas de março, independentemente do quão limpa esteja.

Por fim, erros de registro como preços ausentes, quantidades negativas ou datas corrompidas devem ser marcados e contabilizados de forma
transparente, e nunca substituídos silenciosamente. Trocar uma data inválida pela data de hoje (datetime.now()) ou inventar um preço faltante
fabricaria dados falsos no histórico, criando picos artificiais e enviesando tanto a decisão da gestão quanto o treinamento de futuros
modelos.

## Decisões sobre o enunciado

- "Dimensões físicas" (critério 3 da rubrica): como o CSV não possui colunas de peso, altura ou largura numérica dos pacotes, esse item foi
interpretado e implementado sobre as colunas numéricas de negócio da base: quantidade e preco_unitario.
- "Data de aprovação" (critério 4 da rubrica): como não existe coluna de aprovação no arquivo, a validação temporal foi realizada sobre a
coluna data_venda.
- "sem categoria" vs. "Sem Categoria": foi adotada a grafia em minúsculas ("sem categoria"), conforme descrito na especificação da tarefa e em
coerência direta com a regra de padronização que aplica .lower() a todas as categorias.
- Escopo de bibliotecas (Python nativo + pandas na leitura): o pandas foi utilizado exclusivamente na etapa inicial de leitura do CSV (pd.read_csv(..., dtype=str, keep_default_na=False)) e conversão para lista de dicionários; toda a limpeza, validação e agregação foi construída
em Python nativo, seguindo a versão padrão orientada pelo professor.