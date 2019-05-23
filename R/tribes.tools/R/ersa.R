#' Adjust the bounds of a sement with a mask.
#' @param seg: segment to be adjusted : numeric vector c(start, end)
#' @param mask: masked region:  numeric vector c(start, end)
#' @param min_extension: the minimum distance the segment must extend beyond the masked region not be truncaced (in [bp])
#' @return the masked segment:  numeric vector c(start, end)

adjustSegmentWithMask <- function(seg, mask,  min_extension = 1e6) {
    mask_start = mask[1]
    mask_end = mask[2]
    seg_start = seg[1]
    seg_end = seg[2]
    # check for intersection
    if (seg_start <= mask_end && mask_start <= seg_end) {
        # adjust it if does not extend more than min_extension before the begining
        if ( seg_start > (mask_start - min_extension)) {
            seg_start = min(seg_end, mask_end)
        }
        # adjust it if does not extend more than min_extension after the end
        if ( seg_end < (mask_end + min_extension)) {
            seg_end = max(seg_start, mask_start)
        }
    }
    c(seg_start, seg_end)
}


#' Adjust the bounds of a sement with a multiple masks
#' @param seg: segment to be adjusted : numeric vector c(start, end)
#' @param masks: masked regions:  numeric matrix with dim(K,2) with masked regions in rows as c(start,end)
#' @param min_extension: the minimum distance the segment must extend beyond the masked region not be truncaced (in [bp])
#' @return the masked segment:  numeric vector c(start, end)

adjustSegment <-function(seg, masks, min_extension = 1e6) {
    if (nrow(masks) > 0) {
        for(i in 1:nrow(masks)) {
            seg = adjustSegmentWithMask(seg, masks[i,],min_extension)
        }
    }
    seg
}

maskGermlineSegments<- function(dfGermlineSegments, dfErsaMask, min_extension = 1e6) {
    adjustSegmentsPerChr <- function(dfChrSegments) {
        chr <- dfChrSegments$Chr[1]
        chrMask <- dfErsaMask %>% filter(Chr == chr) %>% select(-Chr) %>% as.matrix()
        adjSegments <- apply(dfChrSegments %>% select(SegStart, SegEnd), MARGIN=1, adjustSegment, chrMask, min_extension)
        dfChrSegments %>% mutate(MaskedSegStart = adjSegments[1,], MaskedSegEnd = adjSegments[2,])
    }
    dfGermlineSegments %>% group_by(Chr) %>% do(adjustSegmentsPerChr(.))
}

readErsaMask <- function(filename) {
    read.table(filename, header = TRUE, col.names = c('Chr', 'MaskStart', 'MaskEnd'))
}

adjustGermlineSegments <- function(germlineSegments, ersaMask) {
    maskedSegments <- maskGermlineSegments(germlineSegments, ersaMask)

    #
    outputSegments <- maskedSegments %>% filter(MaskedSegEnd > MaskedSegStart) %>%
        mutate(IsTruncated = (SegEnd != MaskedSegEnd) | (SegStart != MaskedSegStart )) %>%
        mutate(
            SnpStart = case_when((SegStart != MaskedSegStart) ~ paste0('bp:', MaskedSegStart), TRUE ~ SnpStart),
            SnpEnd = case_when((SegEnd != MaskedSegEnd) ~ paste0('bp:', MaskedSegEnd), TRUE ~ SnpEnd),
            NoSnp=NA,
            Length=(MaskedSegEnd-MaskedSegStart),
            Unit='bp',
            NoMismatch=NA ) %>%
        select(-MaskedSegStart, -MaskedSegEnd, -IsTruncated)
    outputSegments
}

#germlineSegments <- read.germline('../../data/SOD1_germline_2_1_wg_3cM_128.match.gz')
#head(germlineSegments)
#ersaMask <- readErsaMask('../../data/ersa.out.msk')
#head(ersaMask)




