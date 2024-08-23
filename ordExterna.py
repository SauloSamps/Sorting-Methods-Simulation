# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 16:43:52 2024

@author: Saulo
"""

import heapq
import random
import time
from minHeap import minHeap, lastof
import numpy as np
import matplotlib.pyplot as plt


class ExternalSort:

    def __init__(self, m, k, r, n):
        self.m = m  # tamanho da memória interna
        self.k = k  # número de arquivos
        self.r = r
        self.n = n
        self.write_count = 0  # contador para calcular α(r)
        
    def generate_initial_runs(self, input_data):
        runs = []
        heap = minHeap(self.m)
        current_run = []
        
        
        for value in input_data:
            if len(runs)==r-1:
                break
            
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
                    
        while(heap.heap and len(runs)!=r):
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
        phase = 0
        while len(runs) > 1:
            merged = []
            for i in range(0, len(runs), self.k // 2):
                chunk = runs[i:i + self.k // 2]
                merged.append(self.merge(chunk))
                print("fase " + str(phase) + " " + str(self.calculate_beta(runs)))
                for index, sublist in enumerate(chunk):
                    print(f"{index+1} {{ {', '.join(map(str, sublist))} }}")
                phase += 1
            runs = merged
        return runs[0] if runs else []

    def polyphase_merge(self, runs):
        phase = 0
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
            print("fase " + str(phase) + " " + str(self.calculate_beta(runs)))
            for index, sublist in enumerate(files):
                print(f"{index+1} {{ {', '.join(map(str, sublist))} }}")
            phase += 1

        return self.merge(files[0]) if files and files[0] else []

    def cascade_merge(self, runs):
        phase = 0
        levels = [runs]
        while len(levels[-1]) > 1:
            next_level = []
            for i in range(0, len(levels[-1]), self.k):
                chunk = levels[-1][i:i + self.k]
                next_level.append(self.merge(chunk))
            levels.append(next_level)
            print("fase " + str(phase) + " " + str(self.calculate_beta(runs)))
            for index, sublist in enumerate(chunk):
                print(f"{index+1} {{ {', '.join(map(str, sublist))} }}")
            phase += 1
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
    #start_time = time.time()
    initial_runs = sorter.generate_initial_runs(input_data)
    

    #print(f"\n{method}:")
    #print("Sequências iniciais:", len(initial_runs))
    #print("β(m,0):", sorter.calculate_beta(initial_runs))

    if method == "Ordenação balanceada multi-caminhos":
        result = sorter.balanced_multiway_merge(initial_runs)
    elif method == "Ordenação polifásica":
        result = sorter.polyphase_merge(initial_runs)
    else:  # Ordenação em cascata
        result = sorter.cascade_merge(initial_runs)

    #end_time = time.time()
    
    print("final " + str(sorter.calculate_alpha(len(input_data))))

    #print("Resultado final (primeiros 10 elementos):", result[:10])
    #print("α(r):", sorter.calculate_alpha(len(input_data)))
    #print("Tempo de execução:", end_time - start_time, "segundos")
    
    return 0


def main(n=10000,m=1000,k=4, r=1, input_data=[], method='B'):
    
    if (method == 'B'):
        method = "Ordenação balanceada multi-caminhos"
    elif (method == 'P'):
        method = "Ordenação polifásica"
    else:
        method = "Ordenação em cascata"
    
    
    sorter = ExternalSort(m, k, r, n)
    run_experiment(sorter, input_data, method)
        

method = input()
parameters = input().split()
keys = input().split()

parameters = [int(x) for x in parameters]
keys = [int(x) for x in keys]

m, k, r, n = parameters[0], parameters[1], parameters[2],parameters[3]

if len(keys)>n:
    keys = keys[:n]
    
main(n, m, k, r, keys, method)



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    