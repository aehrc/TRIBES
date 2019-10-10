

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


write.germline <-function(germline_df, filename) {
    outf <- open.file(filename, 'w')
    write.table(germline_df, outf, sep = '\t', col.names = FALSE, row.names = FALSE, quote = FALSE)
    close(outf)
}


normalizeSegments.germline <-function(germline_df) {
    data.frame(
        Chr = germline_df$Chr,
        Fam1 = germline_df$Fam1,
        Id1 = germline_df$Id1,
        Fam2 = germline_df$Fam2,
        Id2 = germline_df$Id2,
        Pair = paste(germline_df$Id1, germline_df$Id2, sep='_'),
        Start.bp = germline_df$SegStart,
        End.bp = germline_df$SegEnd,
        SnpStart = germline_df$SnpStart,
        SnpEnd = germline_df$SnpEnd,
        Length.bp = germline_df$SegEnd - germline_df$SegStart,
        germline_Length.CM = germline_df$Length,
        stringsAsFactors = FALSE
    )
}

segments2germline <- function(segmengts) {
    segmengts %>% ungroup %>% transmute(
        Fam1 = Fam1,
        Id1 = Id1,
        Fam2 = Fam2,
        Id2 = Id1,
        Chr = Chr,
        SegStart = Start.bp,
        SegEnd = End.bp,
        SnpStart = SnpStart,
        SnpEnd = SnpEnd,
        NoSnp = 'NA',
        Length = Length.cM,
        Unit = 'cM',
        NoMismatch = 'NA',
        Res1 = 'NA',
        Res2 = 'NA'
    )
}



