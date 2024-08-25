import numpy as np
import matplotlib.pyplot as plt
from externalSort import ExternalSort
    
def calculate_beta_m_0(m_values, k, r, input_data):
    beta_values = []
    for (i, m) in enumerate(m_values):
        sorter = ExternalSort(m, k)
        initial_runs = sorter.generate_initial_runs(input_data)
        beta = sorter.calculate_beta(initial_runs)
        beta_values.append(beta)
        print(f'm = {i + 1}/{m_values.size}')
    return beta_values

k = 4  # número de arquivos
r = 10  # número de sequências iniciais
n = 1000000  # tamanho do conjunto de dados

# Gerar dados de entrada aleatórios
input_data = np.random.randint(1, 1000001, n)

# Valores de m para testar
m_values = np.arange(3, 61, 1)  # [3, 6, 9, ..., 60]

# Calcular β(m, 0) para cada valor de m
beta_values = calculate_beta_m_0(m_values, k, r, input_data)

plt.figure(figsize=(10, 6))
plt.plot(m_values, beta_values, marker='o')
plt.title('β(m, 0) em função de m')
plt.xlabel('m (tamanho da memória interna)')
plt.ylabel('β(m, 0)')
plt.grid(True)
plt.savefig('Figura-beta-3-m-61-1.png', dpi=300, bbox_inches='tight')
plt.show()

