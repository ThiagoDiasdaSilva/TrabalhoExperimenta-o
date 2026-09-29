import numpy as np 
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
import os



#Apresentar estatística descritiva – média, desvio padrão, boxplots – para
#cada variável dependente.
#◆ Apresentar os testes estatísticos e seus resultados
#● Fazer o teste de normalidade para as amostras (mesmo que a
#equipe de autoria do artigo não tenha feito).
#● Fazer o teste de hipóteses adequado para as amostras, segundo o
#design experimental e a normalidade das amostras
#● Salvar telas mostrando o passo a passo.

pasta_saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras")
os.makedirs(pasta_saida, exist_ok=True)


def estatistica_media(dados, rotulo):
    media = np.mean(dados)
    return print(f"Media relativa a {rotulo}: {media:.3f}")

def estatistica_devio(dados, rotulo):
    desvio = np.std(dados, ddof=1)
    return print(f"Desvio relativa a {rotulo}: {desvio:.3f}")


def boxplot(dados ,rotulo, nome_arquivo):
    plt.figure(figsize=(8, 6))
    plt.boxplot(dados, vert=False, patch_artist=True, 
                boxprops=dict(facecolor='lightblue'),
                medianprops=dict(color='red'))
    plt.title(f'Boxplot referente a {rotulo}')
    plt.xlabel('Valores')
    caminho = f"{pasta_saida}/{nome_arquivo}.png"
    plt.savefig(caminho, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Figura salva em {caminho}")

def Shapiro_Wilk(dados, rotulo):
    stat, p_value = stats.shapiro(dados)
    print(f"--- Shapiro-Wilk: {rotulo} (n={len(dados)}) ---")
    print(F"Statistic: {stat:.4f}, p-value: {p_value:.4f}")

def teste_hipotese(dados1, dados2, rotulo1, rotulo2, alfa=0.05):

    
    print(f"\n=== Teste de hipóteses: {rotulo1} (n={len(dados1)}) vs "
          f"{rotulo2} (n={len(dados2)}) — amostras independentes ===")
    print("H0: as duas populações têm a mesma média/distribuição.")
    print("H1: as duas populações diferem.\n")

    normal1 = Shapiro_Wilk(dados1, rotulo1, alfa)
    normal2 = Shapiro_Wilk(dados2, rotulo2, alfa)
    print()

    if normal1 and normal2:
        stat_levene, p_levene = stats.levene(dados1, dados2)
        variancias_iguais = p_levene > alfa
        print(f"--- Levene (homogeneidade de variâncias) ---")
        print(f"Statistic: {stat_levene:.4f}, p-value: {p_levene:.4f}")
        print(f"=> Variâncias {'iguais' if variancias_iguais else 'diferentes'}.\n")

        stat, p_value = stats.ttest_ind(dados1, dados2, equal_var=variancias_iguais)
        nome_teste = "Teste t de Student" if variancias_iguais else "Teste t de Welch"
    else:
        stat, p_value = stats.mannwhitneyu(dados1, dados2, alternative='two-sided')
        nome_teste = "Teste de Mann-Whitney U"

    print(f"Teste escolhido: {nome_teste}")
    print(f"Statistic: {stat:.4f}, p-value: {p_value:.4f}")
    if p_value < alfa:
        print(f"=> p-valor < {alfa}: rejeitamos H0. Diferença estatisticamente significativa.")
    else:
        print(f"=> p-valor >= {alfa}: não rejeitamos H0. Sem diferença significativa.")

    return nome_teste, stat, p_value




#respectivo a inspeção do teste de usuabilidade



ROTULOS_inspection = [
    "Discrepancies",
    "False Positives",
    "Total Problems",
    "Time (min)",
    "Effectiveness (%)",
    "Efficiency (%)",
]

ROTULOS_testing = [
    "Total Problems", 
    "Time (min)",
    "Effectiveness (%)",
    "Efficiency (%)"
]

I1 = [21, 2, 19, 108, 15.0, 10.6]
I2 = [20, 2, 18 , 94, 14.2, 11.5]
I3 = [27, 2, 25, 101, 19.7, 14.9]
I4 = [26, 0, 26, 81, 20.5, 19.3]
I5 = [16, 1, 15, 98, 11.8, 9.2]
I7 = [27, 3, 34, 111, 26.3, 18.4]
I8 = [28, 1, 27, 96, 21.3, 16.9]
I9 = [23, 0, 23, 114, 18.1, 12.1]
I10 = [19, 3, 16, 92, 12.6, 10.4]

U1 = [11, 33, 8.7, 10.0]
U2 = [8, 25, 6.3, 9.6]
U3 = [13, 69, 10.2, 5.7]
U4 = [5, 15, 3.9, 10.0]
U5 = [8, 30, 6.3, 8.0]
U6 = [7, 20, 5.5, 10.5]
U7 = [14, 29, 11.0, 14.5]
U8 = [7, 27, 5.5, 7.8]
U9 = [9, 57, 7.1, 4.7]
U10 = [7, 39, 5.5, 5.4]


avaliadores_inspection = [I1, I2, I3, I4, I5, I7, I8, I9, I10]
participantes_testing = [U1, U2, U3, U4, U5, U6, U7, U8, U9, U10]


dados_inspection = {
    rotulo: [avaliador[i] for avaliador in avaliadores_inspection]
    for i, rotulo in enumerate(ROTULOS_inspection)
}

dados_testing = {
    rotulo: [participante[i] for participante in participantes_testing]
    for i, rotulo in enumerate(ROTULOS_testing)
}


print("=" * 60)
print("Estatistica descretiva por variavel dependente - Usuability inspection")
print("=" * 60)

for rotulo, valores in dados_inspection.items():
    label = f"{rotulo} (Inspection)"
    estatistica_media(valores, label)
    estatistica_devio(valores, label)

print("=" * 60)
print("Estatistica descretiva por variavel dependente - Usuability Testing")
print("=" * 60)

for rotulo, valores in dados_testing.items():
    label = f"{rotulo} (Testing)"
    estatistica_media(valores, label)
    estatistica_devio(valores, label)

print("=" * 60)
print("Boxplots")
print("=" * 60)

for rotulo, valores in dados_inspection.items():
    nome_arquivo = "boxplot_inspection_" + rotulo.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("%", "pct")
    boxplot(valores, f"{rotulo} - Usability Inspection", nome_arquivo)

for rotulo, valores in dados_testing.items():
    nome_arquivo = "boxplot_testing_" + rotulo.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("%", "pct")
    boxplot(valores, f"{rotulo} - Usability Testing", nome_arquivo)


print("=" * 60)
print("Teste de normalidade - Usuability inspection")
print("=" * 60)
for rotulo, valores in dados_inspection.items():
    Shapiro_Wilk(valores, f"{rotulo} (Inspection)")

print("=" * 60)
print("Teste de normalidade - Usuability Testing")
print("=" * 60)
for rotulo, valores in dados_testing.items():
    Shapiro_Wilk(valores, f"{rotulo} (Testing)")

print("=" * 60)
print("Teste de hipoteses - Inspection vs Testing (amostras independentes)")
print("=" * 60)
print("Discrepancies e False Positives só existem em Inspection,")
print("por isso não entram no teste de hipóteses (sem grupo para comparar).\n")

variaveis_comuns = ["Total Problems", "Time (min)", "Effectiveness (%)", "Efficiency (%)"]

resultados = {}
for rotulo in variaveis_comuns:
    resultados[rotulo] = teste_hipotese(
        dados_inspection[rotulo], dados_testing[rotulo],
        f"{rotulo} (Inspection)", f"{rotulo} (Testing)"
    )

print("\n" + "=" * 60)
print("Resumo dos testes de hipoteses")
print("=" * 60)
for rotulo, (nome_teste, stat, p) in resultados.items():
    conclusao = "DIFERENÇA SIGNIFICATIVA" if p < 0.05 else "sem diferença significativa"
    print(f"{rotulo:22s} | {nome_teste:20s} | p={p:.4f} | {conclusao}")



