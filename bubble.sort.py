#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 14:03:15 2020

@author: vishal
"""

list = [1,4,2,5,6]
for j in range (len(list)-1):
    for i in range (len(list)-1):
        if list[i]>list[i+1]:
            list[i], list[i+1] = list[i+1], list [i]
            
print (list)

