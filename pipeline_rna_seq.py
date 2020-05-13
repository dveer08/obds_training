#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 10:16:38 2020

@author: sumeet
"""


from ruffus import *
from cgatcore import pipeline as P
import sys



#Import parameters
Params = P.get_parameters ("pipeline_rna_seq.yml")

#This part is the fastq to generate fastqc html files
@transform('*.fastq.gz', suffix('.fastq.gz'),'_fastqc.html')
def fastqc (infile , outfile):
    statement = '''fastqc %(infile)s > %(outfile)s.log'''
    P.run(statement)                
    
    
#Next want to do multiqc to make a nice report containing all the fastqc from each fastq file
#We want to merge the input from fastqc files into multiqc report
#First use decorator @follows to make a directory for output
#use the input from fastqc in the merge function, output will be multiqc.html report
#define multiqc function, need multiple infiles
#run this like  . - to look in cd
#Name the output file usin -n and specify output directory using -o 
@follows(mkdir('multiqc_reports'))
@merge(fastqc, 'multiqc_reports/multiqc.html')
def multiqc (infiles , outfile):
    statement = ''' export LC_ALL=en_US.UTF-8 && export LANG=en_US.UTF-8 
    && multiqc . -f -n %(outfile)s '''
    P.run(statement)  

#Next function is mapping - Hisat
#Use a regex to allow input for two sets of file, ie for paired end sequence mapping
#\1 takes matched group between () as same, reuses it for name of the bam
#tuple here
#stdout pipe to same tools
@follows(mkdir('bamfiles'))
@collate('*.fastq.gz', regex(r'(.+)_[12].fastq.gz$'),r'bamfiles/\1.bam')
def hisat (infiles , outfile):
    fastq1,fastq2 = infiles
    statement = '''hisat2 %(hisat_options)s --threads %(hisat_threads)s -x %(hisat_genome)s 
    -1 %(fastq1)s -2 %(fastq2)s --summary-file %(outfile)s.txt | 
    samtools sort - -o %(outfile)s 
    && samtools index %(outfile)s '''
    P.run(statement, job_threads = Params["hisat_threads"], job_queue = 'all.q')    
    
@transform(hisat, suffix('.bam'),'.idxstats')
def idxstats(infile , outfile):
    statement = '''samtools idxstats %(infile)s > %(outfile)s'''
    P.run(statement)

@transform(hisat, suffix('.bam'),'.flagstat')
def flagstat(infile , outfile):
    statement = '''samtools flagstat %(infile)s > %(outfile)s'''
    P.run(statement)
    
@merge(hisat, 'count.table')
def featureCounts(infiles, outfile):
    input_list = " ".join(infiles)
    #the input_list is to join lists from various infiles to a space separarted string file.
    statement = '''featureCounts %(featureCounts_options)s -T %(featureCounts_threads)s
    -a %(featureCounts_annotation)s -o %(outfile)s %(input_list)s '''
    P.run(statement, job_threads = Params["featureCounts_threads"], job_queue = 'all.q')
           # this line helps with running the statement on 12 cores and also specifies all.q if it were on a different cluster
    


#The main bit to let it run from cgat core
if __name__ == "__main__":
    sys.exit( P.main (sys.argv))