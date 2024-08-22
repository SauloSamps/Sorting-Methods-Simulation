# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 12:43:33 2024

@author: Saulo
"""

import heapq
import random
import time
from minHeap import minHeap, lastof
import numpy as np
import matplotlib.pyplot as plt


class ExternalSort:

    def __init__(self, m, k):
        self.m = m  # tamanho da memória interna
        self.k = k  # número de arquivos
        self.write_count = 0  # contador para calcular α(r)
        
    def generate_initial_runs(self, input_data):
        runs = []
        heap = minHeap(self.m)
        current_run = []
        
        
        for value in input_data:
            if not heap.push(value, (value < lastof(current_run))):
                min_value = heap.pop()
                if min_value:
                    current_run.append(min_value)
                    heap.push(value, (value < lastof(current_run)))
                    #self.write_count += 1
                else:
                    runs.append(current_run)
                    current_run = []
                    heap.reset()
                    
                    current_run.append(heap.pop())
                    #self.write_count += 1
                    heap.push(value, (value < lastof(current_run)))
                    
        while(heap.heap):
            min_value = heap.pop()
            if min_value:
                current_run.append(min_value)
                #self.write_count += 1
            else:
                runs.append(current_run)
                current_run = []
                heap.reset()
                
                current_run.append(heap.pop())
                #self.write_count += 1
        runs.append(current_run)
        
        return runs                    

    def balanced_multiway_merge(self, runs):
        while len(runs) > 1:
            merged = []
            for i in range(0, len(runs), self.k // 2):
                chunk = runs[i:i + self.k // 2]
                merged.append(self.merge(chunk))
            runs = merged
        return runs[0] if runs else []

    def polyphase_merge(self, runs):
        if not runs:
            return []

        files = [[] for _ in range(self.k)]
        for i, run in enumerate(runs):
            files[i % self.k].append(run)

        while len(files) > 1:
            files.sort(key=lambda f: len(f))
            file1, file2 = files[:2]

            merged = []
            while file1 and file2:
                merged.append(self.merge([file1.pop(0), file2.pop(0)]))

            merged.extend(file1)
            merged.extend(file2)

            files = files[2:] + [merged]

        return self.merge(files[0]) if files and files[0] else []

    def cascade_merge(self, runs):
        levels = [runs]
        while len(levels[-1]) > 1:
            next_level = []
            for i in range(0, len(levels[-1]), self.k):
                chunk = levels[-1][i:i + self.k]
                next_level.append(self.merge(chunk))
            levels.append(next_level)
        return levels[-1][0] if levels[-1] else []

    def merge(self, lists):
        merged = []
        heap = []
        for i, lst in enumerate(lists):
            if lst:
                heapq.heappush(heap, (lst[0], i, 0))

        while heap:
            val, list_index, element_index = heapq.heappop(heap)
            merged.append(val)
            self.write_count += 1
            if element_index + 1 < len(lists[list_index]):
                next_val = lists[list_index][element_index + 1]
                heapq.heappush(heap, (next_val, list_index, element_index + 1))

        return merged

    def calculate_alpha(self, n):
        return self.write_count / n

    def calculate_beta(self, runs):
        return sum(len(run) for run in runs) / (self.m * len(runs))


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
    
    
    
    
    
    
    
    
    
