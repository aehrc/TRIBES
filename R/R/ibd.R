
#
# IBD Segment related functions
#

normalizeSegments <- function(df) {
    UseMethod("normalizeSegments", df)
}


normalizeSegments.default <- function(df) {
    stop("not implemented")
}


appendGeneticUnits <- function(segments, gm) {

    segments %>% group_by(Chr) %>%
        mutate(Start.cM = gm$bpToCM(Start.bp, Chr[1]),End.cM=gm$bpToCM(End.bp, Chr[1])) %>%
        mutate(Length.cM = End.cM - Start.cM)
}

normalizeSegmentsWithGU <- function(df, gm) {
    appendGeneticUnits(normalizeSegments(df), gm)
}

filterSegments <-function(segments, chrs=ALL_AUTOSOMES, minLength.cM=0) {
    segments[is.element(segments$Chr, chrs) & segments$Length.cM >= minLength.cM, ]
}

estimateIBDSharing <-function(segments, chrs=ALL_AUTOSOMES, minLength.cM=0) {
    totalLenght.cM <- sum(CHROMOSOMES$Length.cM[is.element(CHROMOSOMES$Chr, chrs)])
    filteredSegments <- filterSegments(segments, chrs, minLength.cM)
    totalLengthById <- aggregate(filteredSegments$Length.cM, by=list(filteredSegments$Id1, filteredSegments$Id2), sum)
    data.frame(Id1 = totalLengthById$Group.1, Id2 = totalLengthById$Group.2,
               IBD0.cM= 1-totalLengthById$x/totalLenght.cM,
               IBD1.cM = NA,
               IBD2.cM = NA
    )
}


