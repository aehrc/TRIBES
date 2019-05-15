##
## Specific for ALS850
##

# Condiguration

configfile: "config.yaml"


include: "core.smake"
include: "process.smake"
include: "relations.smake"

# Variables

FLUSH_DIR="/flush3/{USER}".format(**os.environ)
REL_SAMPLE=config['rel_sample']


rule estimate_degree:
    input:
        "_".join([REL_SAMPLE,'GRM-allchr','FPI', 'IBD.csv'])

rule estimate_degree_vs_true:
    input:
        "_".join([REL_SAMPLE,'GRM-allchr','FPI', 'IBD','RVT.html'])

rule all:
    input:   
        rules.estimate_degree.output
