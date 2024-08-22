# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 18:29:27 2024

@author: Saulo
"""
import numpy as np
import matplotlib.pyplot as plt


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
    plt.xlabel('n')
    plt.ylabel('alpha')
    plt.title('Graph of Alpha vs. N for Different Methods')
    plt.legend(title='Method')
    plt.grid(True)

    # Show the plot
    plt.show()
    
    
data = [{'method': 'P', 'n': 2, 'alpha': 3}, {'method': 'P', 'n': 2, 'alpha': 3}]
print_dataset(data)
    
    
    