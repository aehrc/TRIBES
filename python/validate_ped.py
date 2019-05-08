#!/usr/bin/env python
'''
Created on 30 Aug 2018

@author: szu004
'''
# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function)
# from builtins import *

import sys


VALID_ALLELES = set(['A', 'G', 'T', 'C'])


class MessageSink(object):
    
    def __init__(self):
        self.warning_count = 0
        
    def error(self, msg):
        print("ERROR: %s" % msg,  file = sys.stderr)
        exit(1)

    def warning(self, msg):
        self.warning_count+= 1
        print("WARN: %s" %  msg, file = sys.stderr)
        
    def fail_on_warnings(self):
        if self.warning_count:
            self.error("Validation failed. There were %s warnings reported" % self.warning_count)

class VariantIndex(object):
    
    def __init__(self):
        self.variants_by_allele = dict()
        
    def add_allele(self, a, v_index):
        index_set = self.variants_by_allele.get(a)
        if index_set is None:
            index_set = set()
            self.variants_by_allele[a] = index_set
        index_set.add(v_index)
        
    def get_alleles(self, v_index):
        return [a for a, v_indexes in  self.variants_by_allele.iteritems() if v_index in v_indexes]


def validate_ped_file(ped_f, no_variants = None):
    logger = MessageSink()
    v_indexer = VariantIndex()
    for line_no, line in enumerate(ped_f):
        row = line.strip().split()
        if len(row) < 6:
            logger.error("Lets than 6 columns in line: %s", line_no)
        #meta = row[0:6]
        #TODO: maybe some checking on alleles
        alleles = row[6:]    
        if no_variants is None and line_no == 0: 
            no_variants = int(len(alleles)/2)
            print("Inferred no of variants to: %s" % no_variants)
        if len(alleles) != no_variants * 2:
            logger.error("Wrong no of  %s alleles found (expected %s) in line: %s" % (len(alleles), no_variants * 2, line_no))
        # check that all alleles are single line base ones
        for ai, a in enumerate(alleles):
            v_indexer.add_allele(a, int(ai/2))
        if (line_no % 10 == 0):
            print("Processed line: %s" % line_no)
     
    for vi in range(0, no_variants):
        v_alleles = v_indexer.get_alleles(vi)
        for a in v_alleles:
            if (len(a)!=1):
                logger.warning("Non SNP allele `%s` at: %s" % (a, vi))
            elif not a in VALID_ALLELES:
                logger.warning("Non SNP GATC allele `%s` at: %s" % (a, vi))
        if len(v_alleles) > 2:
            logger.warning("Non biallelic variant `%s` at: %s" % (v_alleles, vi))
                
    logger.fail_on_warnings()
        
        
        
def main():
    if len(sys.argv) < 2:
        print("Usage: %s <ped_filename>" %  sys.argv[0])
        sys.exit(1)
    ped_filename = sys.argv[1]
    print("Validating ped file: %s" % ped_filename)
    with open(ped_filename, 'r') as ped_f:
        validate_ped_file(ped_f)
    
if __name__ == "__main__":
    main()
