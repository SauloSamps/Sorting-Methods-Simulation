# -*- coding: utf-8 -*-
import random
import time
import numpy as np
import matplotlib.pyplot as plt
from externalSort import ExternalSort

def generate_random_data(n):
    return [random.randint(1, 1000000) for _ in range(n)]


def run_experiment(sorter, input_data, method):
    start_time = time.time()
    initial_runs = sorter.generate_initial_runs(input_data)
    

    print(f"\n{method}:")
    print("Sequências iniciais:", len(initial_runs))
    print("β(m,0):", sorter.calculate_beta(initial_runs))

    if method == "Ordenação balanceada multi-caminhos":
        result = sorter.balanced_multiway_merge(initial_runs)
    elif method == "Ordenação polifásica":
        result = sorter.polyphase_merge(initial_runs)
    else:  # Ordenação em cascata
        result = sorter.cascade_merge(initial_runs)

    end_time = time.time()

    print("Resultado final (primeiros 10 elementos):", result[:10])
    print("α(r):", sorter.calculate_alpha(len(input_data)))
    print("Tempo de execução:", end_time - start_time, "segundos")

    return len(initial_runs), sorter.calculate_alpha(len(input_data))

def main(n=10000,m=1000,k=4):
    input_data = generate_random_data(n)

    data = []
    methods = [
        "Ordenação balanceada multi-caminhos", "Ordenação polifásica",
        "Ordenação em cascata"
    ]
    
    for method in methods:
        sorter = ExternalSort(m, k)
        sequences, alpha = run_experiment(sorter, input_data, method)
        data.append({'method': method, 'n': sequences, 'alpha': alpha})
        
    return data


def print_dataset(data):
    # Create a dictionary to store x and y values for each method
    methods_data = {}

    # Organize data by method
    for entry in data:
        method = entry['method']
        n = entry['n']
        alpha = entry['alpha']
        
        if method not in methods_data:
            methods_data[method] = {'n': [], 'alpha': []}
        
        methods_data[method]['n'].append(n)
        methods_data[method]['alpha'].append(alpha)

    # Plot data for each method
    plt.figure(figsize=(10, 6))
    for method, values in methods_data.items():
        plt.plot(values['n'], values['alpha'], label=method)
    
    # Add labels and title
    plt.xlabel('Number of Starting Sequences')
    plt.ylabel('alpha')
    plt.title('Alpha per Number of Starting Sequences')
    plt.legend(title='Method')
    plt.grid(True)
    
    plt.savefig('plot.png', dpi=300, bbox_inches='tight')  # Save as PNG with high resolution

    # Show the plot
    plt.show()
    
    

data = []
#powers_of_10 = [10 ** i for i in range(5 + 1)]

for i in range (1,100000,100):
    data += main(i)

#for i in powers_of_10:
#    data += main(i)

print_dataset(data)
    
    
    
    
    
    
    
    
    
