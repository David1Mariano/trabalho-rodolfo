import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mode

# ======================
# DADOS SIMULADOS
# ======================

np.random.seed(42)

temperatura = np.random.normal(24, 3, 100)
energia = np.random.normal(80, 10, 100)

dados = pd.DataFrame({
    "Temperatura": temperatura,
    "Energia": energia
})

# ======================
# FUNÇÃO ESTATÍSTICA
# ======================

def analise_univariada(coluna):

    print(f"\nANÁLISE DE {coluna.name.upper()}")
    print("-" * 40)

    media = coluna.mean()
    mediana = coluna.median()
    moda = coluna.mode()[0]

    minimo = coluna.min()
    maximo = coluna.max()
    amplitude = maximo - minimo

    variancia = coluna.var()
    desvio = coluna.std()

    cv = (desvio / media) * 100

    quartis = coluna.quantile([0.25,0.50,0.75])

    print(f"Média: {media:.2f}")
    print(f"Mediana: {mediana:.2f}")
    print(f"Moda: {moda:.2f}")

    print(f"Máximo: {maximo:.2f}")
    print(f"Mínimo: {minimo:.2f}")
    print(f"Amplitude: {amplitude:.2f}")

    print(f"Variância: {variancia:.2f}")
    print(f"Desvio Padrão: {desvio:.2f}")
    print(f"Coeficiente de Variação: {cv:.2f}%")

    print("\nQuartis:")
    print(quartis)

# ======================
# ANÁLISES
# ======================

analise_univariada(dados["Temperatura"])
analise_univariada(dados["Energia"])

# ======================
# TABELAS DE FREQUÊNCIA
# ======================

print("\nTabela de Frequência - Temperatura")

faixas_temp = pd.cut(
    dados["Temperatura"],
    bins=5
)

print(faixas_temp.value_counts().sort_index())

print("\nTabela de Frequência - Energia")

faixas_energia = pd.cut(
    dados["Energia"],
    bins=5
)

print(faixas_energia.value_counts().sort_index())

# ======================
# ALERTAS INTELIGENTES
# ======================

for i in range(len(dados)):

    if dados["Temperatura"][i] > 30:
        print(f"ALERTA: Temperatura crítica na leitura {i}")

    if dados["Energia"][i] < 60:
        print(f"ALERTA: Energia baixa na leitura {i}")

# ======================
# GRÁFICO 1
# ======================

plt.figure(figsize=(10,5))

plt.plot(
    dados["Temperatura"],
    color="red"
)

plt.title("Monitoramento da Temperatura da Missão")
plt.xlabel("Leitura")
plt.ylabel("Temperatura (°C)")
plt.grid(True)

plt.show()

# ======================
# GRÁFICO 2
# ======================

plt.figure(figsize=(10,5))

plt.hist(
    dados["Energia"],
    bins=10,
    color="blue"
)

plt.title("Distribuição dos Níveis de Energia")
plt.xlabel("Energia (%)")
plt.ylabel("Frequência")

plt.show()