
# Condiguration

singularity: "docker://docker.io/piotrszul/tribes"
configfile: "config.yaml"

include: "core.smake"
include: "process.smake"
include: "relations.smake"

# Variables

REL_SAMPLE=config['rel_sample']

localrules: usage

rule usage:
    shell:
        "echo 'Usage:' ;"
        "echo '    tribes -d <working dir> (estimate_degree|estimate_degree_vs_true)'"


rule estimate_degree:
    input:
        ["_".join([s,'GRM-allchr','FPI', 'IBD.csv']) for s in expand(REL_SAMPLE, **config)]

rule estimate_degree_vs_true:
    input:
        "_".join([REL_SAMPLE,'GRM-allchr','FPI', 'IBD','RVT.html'])

