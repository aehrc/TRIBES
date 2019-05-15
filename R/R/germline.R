

#
# germline related functions
#

GERMLINE_COLUMN_NAMES <- c(
    "Fam1",
    "Id1",
    "Fam2",
    "Id2",
    "Chr",
    "SegStart",
    "SegEnd",
    "SnpStart",
    "SnpEnd",
    "NoSnp",
    "Length",
    "Unit",
    "NoMismatch",
    "Res1",
    "Res2"
)

read.germline <- function(filename) {
    infile <-gzfile(filename)
    germlineDF = read.table(infile, header = FALSE, col.names = GERMLINE_COLUMN_NAMES, stringsAsFactors = FALSE)
    class(germlineDF) <- append(class(germlineDF), "germline")
    germlineDF
}


normalizeSegments.germline <-function(germline_df) {
    data.frame(
        Chr = germline_df$Chr,
        Id1 = germline_df$Id1,
        Id2 = germline_df$Id2,
        Pair = paste(germline_df$Id1, germline_df$Id2, sep='_'),
        Start.bp = germline_df$SegStart,
        End.bp = germline_df$SegEnd,
        Length.bp = germline_df$SegEnd - germline_df$SegStart,
        germline_Length.CM = germline_df$Length,
        stringsAsFactors = FALSE
    )
}
