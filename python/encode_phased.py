#!/usr/bin/env python
'''
Created on 2 Jan 2019

@author: szu004
'''

import sys
import os



def encode_genotype(genotypes):
    def encode(s1,s2):
        return int(s1) + 2*int(s2)
    return [encode(*g.split(':')[0].split('|')) for g in genotypes]


def encode_line(line):
    items = line.split()
    return items[0:2] + encode_genotype(items[9:])


def encode_header(line):
    items = line.split()
    return ['CHR', 'POS'] + items[9:]
    

def main():
    for line in sys.stdin:
        if not line.startswith('##'):
            if line.startswith('#'):
                print(",".join(encode_header(line)))
            else:
                print(",".join(map(str,encode_line(line))))

if __name__ == "__main__":
    main()
