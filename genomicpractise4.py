#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 11:52:46 2020

@author: eduardo
"""


import argparse
import sys
import gzip
parser = argparse.ArgumentParser(description='converting BAM to BED')
parser.add_argument('-i', '--bam', type=str, help='input file (BAM file)')
parser.add_argument('-o', '--bed', type=str, help='input file (BED file)')
parser.add_argument('-z', '--zip', action='store_true', help='output asgzip')
args = parser.parse_args()


import pysam
import logging as L
L.basicConfig(level=L.DEBUG)
L.basicConfig(filename='example.log', level=L.DEBUG)

if args.bam =="-":
    input_bam = sys.stdin
    infile = pysam.AlignmentFile(input_bam, "rb")
    iter = infile.fetch(until_eof = True)
else:
    input_bam = args.bam
    infile = pysam.AlignmentFile(input_bam, "rb")
    iter = infile.fetch()

if args.bed == "-":
    output_bed = sys.stdout
else:
    output_bed = open(args.bed, "w")

if args.zip == True:
    output_bed = gzip.open(args.bed, "wt")
else:
    output_bed = open(args.bed, "w")  
with output_bed as output:
    for aln in iter:
        if aln.is_proper_pair:
            chrom = aln.reference_name
            bed_start = aln.reference_start
            bed_end = aln.reference_end
            output.write(f'{chrom}\t{bed_start}\t{bed_end}\n')
            L.info(chrom)
            L.info(bed_start)
            L.info(bed_end)
        else:
            L.warn('not a proper pair)')
            continue        
    



