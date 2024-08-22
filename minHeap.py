# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 14:48:57 2024

@author: Saulo
"""

class minHeap:
    def __init__(self, size):
        self.heap = []
        self.maxSize = size
        
    def push(self, value, valid=False):
        if len(self.heap) < self.maxSize:
            data = {"value": value, "marked": valid }
            self.heap.append(data)
            self.heap.sort(key=lambda x: x["value"])
            return True
        else:
            return False
        
    def pop(self):
        for item in self.heap:
            if not item["marked"]:
                value = item["value"]
                self.heap.remove(item)
                return value
        return False
    
    def reset(self):
        for item in self.heap:
            item["marked"] = False
    
    
    
    
def lastof(array):
    if len(array) > 0:
        return array[-1]
    else:
        return 0
    
        
    