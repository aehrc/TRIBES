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
        "_".join([REL_SAMPLE,'GRM','IBD-allchr.csv'])

rule all_report:
    input:
        "_".join([REL_SAMPLE,'GRM','IBD-allchr','RVT.html'])

