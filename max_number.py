# -*- coding: utf-8 -*-
"""
Created on Tue May  5 10:36:24 2020

@author: ecalpena
"""


list = [5, 8, 6, 9, 1, 7, 3, 2, 4]
#Selecting the first as the max
max = list[0]
#for any additional number if bigger than the previous, replace it
for number in list[1:]:
    if number > max:
        max = number
print(max)