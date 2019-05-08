#!/usr/bin/env python

#Natalie Twine edited python script November 2017. original from https://github.com/joepickrell/1000-genomes-genetic-maps
#Script interpolates a genetic map (ie one provided on Beagle 4.1 website) in plink format, with a .map file in plink format - which contains physical location but no genetic (in cM)

import sys, os, gzip

#infile = gzip.open(sys.argv[1]) #.bed
infile = open(sys.argv[1]) #.bed
#mapfile = gzip.open(sys.argv[2]) #input map file, either the HapMap map or the 1000 Genomes OMNI map
mapfile = gzip.open(sys.argv[2], 'r') if sys.argv[2].endswith(".gz") else open(sys.argv[2], 'r')
#input map file, either the HapMap map or the 1000 Genomes OMNI map
outfile = open(sys.argv[3], "w") #output style: [chr] [rs] [pos] [genetic pos]

posin = list()
rsin = list()
mappos = list()
mapgpos = list()
chrom = None

line = infile.readline()
while line:
	line = line.strip().split()
#	pos = int(line[2]) original code. NAT edit to read in plink format .map file from ALS cohort
        pos = int(line[3])
#	rs = line[3] original code. NAT edit to reead in plink format .map file from ALS cohort
	rs = line[1]
#grab the chromosome number to output later in script (NAT)	
	this_chrom = line[0]
	if chrom is None:
		chrom = this_chrom
	elif chrom != this_chrom:
		print >> sys.stderr, "Expected chromosomes: %s only but found %s" % (chrom, this_chrom)
		exit(1)
	posin.append(pos)
	rsin.append(rs)
	line = infile.readline()

#PS: Why do we need to skip the first line?
#line = mapfile.readline()
line = mapfile.readline()
while line:
	line = line.strip().split()
	map_chrom = line[0]
	if map_chrom == chrom:
	# Only load the enrties for this chromosme
	#	pos = int(line[0])   #original code. NAT edit to read in plink format genetic recomb .map file from BEAGLE 4.1 website
		pos = int(line[3])
		#pos = int(line[1]) #uncomment for hapmap input
		gpos = float(line[2])
		#gpos = float(line[3]) #uncomment for hapmap  input
		mappos.append(pos)
		mapgpos.append(gpos)
	line = mapfile.readline()

index1 = 0
index2 = 0
while index1 < len(posin):
	pos = posin[index1]
	rs = rsin[index1]
	if pos == mappos[index2]:
		#the 1000 Genomes site was genotyped as part of the map
		print >> outfile, chrom, rs, mapgpos[index2], pos
		##print chrom, rs, pos, mapgpos[index2]
		index1 = index1+1
	elif pos < mappos[index2]:
		#current position in interpolation before marker
		if index2 ==0:
			#before the first site in the map (genetic position = 0)
			print >> outfile, chrom, rs, mapgpos[index2], pos
			index1 = index1+1
		else:
			#interpolate
			prevg = mapgpos[index2-1]
			prevpos = mappos[index2]
			frac = (float(pos)-float(mappos[index2-1]))/ (float(mappos[index2]) - float(mappos[index2-1]))
			tmpg = prevg + frac* (mapgpos[index2]-prevg)
			print >> outfile, chrom, rs, tmpg, pos
			##print chrom, rs, pos, tmpg
			index1 = index1+1
	elif pos > mappos[index2]:
		#current position in interpolation after marker
		if index2 == len(mappos)-1:
			#after the last site in the map (genetic position = maximum in map, note could try to extrapolate based on rate instead)
			print >> outfile, chrom, rs, mapgpos[index2], pos
			##print chrom, rs, pos, mapgpos[index2]
			index1 = index1+1
		else:
			#increment the marker
			index2 = index2+1
