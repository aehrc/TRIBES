# library(R.cache)

#
# rmap.GRCh37.plink <- read.table(gzfile('../../data/ref/plink.chrALL.GRCh37.map.gz'), header = FALSE , col.names = c('Chr', 'Snp', 'Pos.cM', 'Pos.bp'), stringsAsFactors = TRUE)
# save(rmap.GRCh37.plink, file='data/rmap.GRCh37.plin.rda', compress = TRUE)
#

RMAP_GRCh37_PLINK <- 'rmap.GRCh37.plink'

gm_load_plink <-function(filename) {

    PLINK_MAP_COL_NAMES <- c('Chr','Reserved', 'Pos.cM', 'Pos.bp')
    mapfile <-gzfile(filename)
    r_map <- read.table(mapfile, header = FALSE , col.names = PLINK_MAP_COL_NAMES, stringsAsFactors = TRUE)
    r_map$Chr <- paste0('CHR', r_map$Chr)
    r_map
}

gm_bpToCM<-function(position.bp, chr, genetic_map) {
    chr_pos.bp <- genetic_map$Pos.bp[genetic_map$Chr == chr]
    chr_pos.cM <- genetic_map$Pos.cM[genetic_map$Chr == chr]
    approx(chr_pos.bp, chr_pos.cM,
           position.bp,
           yleft = 0.0, yright = max(chr_pos.cM))$y
}

GeneticMap <- setRefClass("GeneticMap",
                          fields = list(map = "data.frame"),
                          methods = list(
                              bpToCM = function(position.bp, chr) {
                                  gm_bpToCM(position.bp, chr, map)
                              }
                          )
)

GeneticMap.fromPlink <- function(name = RMAP_GRCh37_PLINK) {
    GeneticMap$new(map=get(name))
}

GeneticMap.default <- function() {
    GeneticMap.fromPlink()
}

#Deprecated
GeneticMap.load <- function() {
    GeneticMap.fromPlink()
}

#gm_load_plink_cached <- addMemoization(gm_load_plink)

#GeneticMap.load <- function(filename = DEF_GENETIC_MAP_FILE) {
#    GeneticMap$new(map=gm_load_plink_cached(filename))
#}







