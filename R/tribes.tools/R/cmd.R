##
##
## Highe level interface functions (specific for transformations)
##

germline2ibdEstimate <-function(inputFile, outputFile, minSegLength.cM = 3.0, verbose = FALSE, segmentsFile = NULL, ...) {

    germlineMatches <- read.germline(inputFile)
    if (verbose) {
        print("Germline matches")
        print(head(germlineMatches))
    }
    normalizedSegments <- normalizeSegmentsWithGU(germlineMatches, GeneticMap.default())
    if (verbose) {
        print("Normalized segments")
        print(head(as.data.frame(normalizedSegments)))
    }
    filteredSegments <- filterSegments(normalizedSegments, minLength.cM = minSegLength.cM)
    if (!is.null(segmentsFile)) {
        if (verbose) {
            print(sprintf("Writting segments to: %s", segmentsFile))
        }
        write.germline(segments2germline(filteredSegments), segmentsFile)
    }
    sharedIBDPerPair  <-estimateIBDSharing(filteredSegments)
    if (verbose) {
        print("Estimated IBD")
        print(head(sharedIBDPerPair))
    }
    sharedIBDPerPairWithDegree <- sharedIBDPerPair %>% mutate(EstDegree = estimateDegreeFromIBD0(IBD0.cM))
    if (verbose) {
        print("Estimated IBD With Degree")
        print(head(sharedIBDPerPairWithDegree))
    }
    write.csv(sharedIBDPerPairWithDegree, outputFile, row.names = FALSE, quote = FALSE)
}

maskSegments <- function(inputFile, outputFile, ersaMask, verbose = FALSE, ...) {
    germlineSegments <- read.germline(inputFile)
    if (verbose) {
        print("Germline segments")
        print(head(germlineSegments))
    }

    ersaMask <- readErsaMask(ersaMask)
    if (verbose) {
        print("ERSA mask")
        print(head(ersaMask))
    }

    adjustedSegments <- adjustGermlineSegments(germlineSegments, ersaMask)
    if (verbose) {
        print("Adjusted segments")
        print(head(adjustedSegments))
    }

    write.germline(adjustedSegments, outputFile)
}
