#!/usr/bin/env python

import sys
import scipy as sc
import numpy as np
import pandas as pd
from collections import OrderedDict


# Germline treats entries with 0 at NA and thus does not map semnets
# starting at the end of the chromosome correctly (uses BP instead of CM)
DEF_MIN_POS_CM = 1e-6

class GeneticMap(object):
	
	@classmethod
	def load(cls, mapfile_name):
		genetic_map = pd.read_table(mapfile_name, header = None,
                            names=['chrom', 'rs', 'pos_CM', 'pos_bp'],
                            dtype=dict(chrom=np.str, rs=np.str, pos_CM = np.float32, pos_bp = np.int64))
		mapping = dict((chrom, (genetic_map.pos_bp.iloc[gindex].values, genetic_map.pos_CM.iloc[gindex].values)) for chrom, gindex in genetic_map.groupby('chrom').groups.items())
		return cls(mapping)

	def __init__(self, mapping):
		self.mapping = mapping
		
	def bpToCM(self, pos_bp, chrom):
		""" This is very generic but also very slow
		"""
		chr_pos_bp, chr_pos_CM = self.mapping[chrom]		
		return sc.interp(pos_bp, chr_pos_bp, chr_pos_CM, left = 0.0, right = max(chr_pos_CM))
	
def main():
	infile_name = sys.argv[1] #.bed
	mapfile_name = sys.argv[2] #input map file, either the HapMap map or the 1000 Genomes OMNI map
	outfile_name = sys.argv[3] #output style: [chr] [rs] [pos] [genetic pos]
	
	gm = GeneticMap.load(mapfile_name)
	
	plink_map = pd.read_table(infile_name,
                    names = ['chrom', 'rs', 'pos_CM', 'pos_bp'], header = None, 
                    dtype=dict(chrom=np.str, rs=np.str, pos_CM = np.float64, pos_bp = np.int32))
	
	chrom = plink_map.chrom[0]
	assert np.alltrue(plink_map.chrom == chrom)
	# assume all equals to the same done
	plink_map_interpolated  = pd.DataFrame.from_dict(OrderedDict([
		('chrom', plink_map.chrom), 
		('rs', plink_map.rs), 
		('pos_CM', np.maximum(DEF_MIN_POS_CM, gm.bpToCM(plink_map.pos_bp, chrom))), 
		('pos_bp', plink_map.pos_bp), 
	]))	
	plink_map_interpolated.to_csv(outfile_name, header=None, index=None, sep='\t', float_format='%.6f')			
	
				
if __name__ == "__main__":
	main()