##
## Specific for ALS850
##

# Condiguration

configfile: "config.yaml"


include: "core.smake"
include: "process.smake"
include: "germline.smake"

# Variables

FLUSH_DIR="/flush3/{USER}".format(**os.environ)
REL_SAMPLE=config['rel_sample']

rule all:
    input:   
        "_".join([REL_SAMPLE,'GRM-allchr','IBD.csv'])

rule all_report:
    input:
        "_".join([REL_SAMPLE,'GRM-allchr','IBD','RVT.html'])

rule report_with_mask:
    input:
        "_".join([REL_SAMPLE,'GRM-allchr','FPI', 'IBD','RVT.html'])
