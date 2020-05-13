#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:23:50 2020

@author: charlotteb
"""


list = [5,8,6,9,1,7,3,2,4]



#run a loop that runs for each position in the list
#find the maximum and end position

def find_max(list):
    max = list[0]
    i = 0
    max_pos = i
    for number in list[1:]:
        i +=1
        if number > max:
            max = number
            max_pos = i
    tup1 = (max, max_pos)
    return tup1

print(find_max(list))


position = len(list)-1

for number in list:
    max,max_pos = find_max(list[0:position+1])
    
    # Take the number at <position> in <list> and assign it to <max_pos> in <list>
    list[max_pos] = list[position]  
    list[position] = max
    position = position - 1
    
    print(list)

    
