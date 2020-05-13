#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 11:20:55 2020

@author: eduardo
"""

import argparse
import sys
parser = argparse.ArgumentParser(description='comparing 2 bed files')
parser.add_argument('-a', '--bed_a', type=str, help='input a file (BED file)')
parser.add_argument('-b', '--bed_b', type=str, help='input b file (BED file)')

args = parser.parse_args()
print(args)

import pysam
import logging as L
L.basicConfig(level=L.DEBUG)
L.basicConfig(filename='example.log', level=L.DEBUG)
count_overlap = 0
with open(args.bed_a, "r") as bed_a:
    for line in bed_a:
        a_split = line.split('\t')
        a_chrom = a_split[0]
        a_start = int(a_split[1])
        a_end = int(a_split[2])
        
        with open(args.bed_b, "r") as bed_b:
            for line in bed_b:
                b_split = line.split('\t')
                b_chrom = b_split[0]
                b_start = int(b_split[1])
                b_end = int(b_split[2])
                
                if a_chrom == b_chrom:
                    if a_end >= b_start and not a_end >= b_end:
                        count_overlap +=1
                        print(f'a:{b_chrom} {b_start} {b_end}')
                    elif b_end >= a_start and not b_end >= a_end:
                        count_overlap +=1
                        print(f'a:{b_chrom} {b_start} {b_end}')
print(count_overlap)                
               
