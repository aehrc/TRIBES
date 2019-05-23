REL_DEGREE_LEVELS = c(0, 'PO', 1:15, 'UR')
as.relDegree <- function(x, naAsUnrelated = TRUE) {
    if (naAsUnrelated) {
        x[is.na(x)]<-'UR'
    }
    factor(x, levels=REL_DEGREE_LEVELS, ordered = TRUE )
}

REL_DEGREES = as.relDegree(REL_DEGREE_LEVELS)


KING_COEFFS <- data.frame(
    Degree = REL_DEGREES,
    K0.LowerBound = c(0, 0, 0.1, 0.366, sapply(2:15, FUN=function(d){ 1-1/(2^((2*d-1)/2))})),
    K0.UpperBound = c(0.1,0.1, 0.366, sapply(2:16, FUN=function(d){ 1-1/(2^((2*d-1)/2))}))
)

KING_COEFFS.UR.K0 <- mean(KING_COEFFS$K0.LowerBound[KING_COEFFS$Degree =='UR'], KING_COEFFS$K0.UpperBound[KING_COEFFS$Degree =='UR'])

normalizeRelations <- function(rel) {
        rel %>% mutate(Id1.org = Id1, Id2.org = Id2) %>%
        mutate(Id1 = case_when(Id1.org <= Id2.org ~ Id1.org, TRUE ~ Id2.org),
               Id2 = case_when(Id2.org > Id1.org ~ Id2.org, TRUE ~ Id1.org)) %>%
        select(-Id1.org, -Id2.org)
}

readRelations <- function(filename, normalize = TRUE, ...) {
    relations <- read.table(filename, header = TRUE, stringsAsFactors = FALSE)
    result <- data.frame(Id1 = relations$ID1, Id2 = relations$ID2,
               Degree=as.relDegree(relations$Degree, ...),
               stringsAsFactors = FALSE)
    if (normalize) normalizeRelations(result) else result
}

estimateDegreeFromIBD0<-function(ibd0) {
    # there is no difference between 0 and PO (cannot be estimated)
    dl <- length(REL_DEGREES)
    REL_DEGREES[approx(KING_COEFFS$K0.LowerBound[2:dl], KING_COEFFS$Degree[2:dl], ibd0, yleft=2, yright = dl)$y]
}

estimateNumDegreeFromIBD0<-function(ibd0) {
    # there is no difference between 0 and PO (cannot be estimated)
    dl <- length(REL_DEGREES)
    approx(KING_COEFFS$K0.LowerBound[2:dl], KING_COEFFS$Degree[2:dl], ibd0, yleft=2, yright = dl)$y -1
}
