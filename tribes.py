#!/usr/bin/env python

import sys
import click
import yaml
from os import path
import os
from click_option_group import OptionGroup
import shutil


DEF_QC_FILTER='INFO/MQ>59 & INFO/MQRankSum>-2 & AVG(FORMAT/DP)>20 & AVG(FORMAT/DP)<100 & INFO/QD>15 & INFO/BaseQRankSum>-2 & INFO/SOR<1'

class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)


def fcons(h,t):
    t.append(h)
    return t
cons = Infix(fcons)


pipeline = OptionGroup('PIPELINE', help='Pipeline configuation\n')
io = OptionGroup('INPUT/OUTPUT', help='Input/output configuration\n')
ctl = OptionGroup('CONTROL', help='Execution control\n')

#@click.group()
#@click.option('--noop', help='Name to greet', is_flag=True)
#@click.option('--verbose', help='Name to greet', is_flag=True)
#def cli(noop, verbose):
#    pass


@click.command()
@io.option('--vcf', required = True, default = None, type=str)
@io.option('--ref', required = True, default = None, type=str, 
        help='Reference data directory')
@io.option('--output', required = True, default = None, type=str, 
        help='The prefix for the output file.')
@io.option('--output-segments/--no-output-segments', required = False, default = True, show_default=True,
        help='Whether to output segment files.')

@pipeline.option('--qc/--no-qc', required = False, default = False, is_flag = True, 
        help="apply quality control filter defined in BCF_FILTER_EXPR.")
@pipeline.option('--qc-filter', required = False, default = DEF_QC_FILTER, type=str, metavar = 'BCF_FILTER_EXPR', show_default=True,
        help="`bcftools` filter expression to use in qc step.")
@pipeline.option('--non-missing/--no-non-missing', required = False, default = True, is_flag = True, show_default=True,
        help='Keep only loci with all non missing calls.')
@pipeline.option('--bi-snp/--no-bi-snp', required = False, default = True, is_flag = True, show_default=True, 
        help='Keep only bi-allelic SNPs.')
@pipeline.option('--maf/--no-maf', required = False, default = True, is_flag=True, show_default=True,
        help='Filter out SNPs with minor allele frequency less than value given.')
@pipeline.option('--maf-min', required = False, default = 0.01, type=float, show_default=True,
        help='Min MAF to keep.')
@pipeline.option('--ld-prune/--no-ld-prune', required = False, default = False, is_flag = True, show_default=True,
        help='Peform ld pruning with R2 of 0.95 (?)')
@pipeline.option('--phase/--no-phase', required = False, default = True, is_flag = True, show_default=True,
        help='Peform phasing')
@pipeline.option('--phase-with-ref/--phase-without-ref', required = False, default = True, is_flag = True, show_default=True,
        help='Phase with reference')
@ctl.option('--continue/--no-continue', required = False, default = True, is_flag = True, show_default=True,
        help='Continue execution if the working dir exists for the same configuration')
@ctl.option('--clean', required = False, default = False, is_flag = True, show_default=True,
        help='Clean the working directory before execution')
@ctl.option('--force', required = False, default = False, is_flag = True, show_default=True,
        help='Force execution on uncleaned directory')

def estimate(vcf, ref, bi_snp, qc, qc_filter, maf, maf_min, ld_prune, non_missing, phase, phase_with_ref, output,
    output_segments, **flags):
    """ Estimate relatedness using IBD0
    """
    click.echo("Estimate")
    click.echo(flags)
    #click.echo(sys.argv)
    click.echo("Ctx: %s" % click.get_current_context().params)
    vcf_ext = '.vcf.gz'

    errors = []
    vcf.endswith('.vcf.gz') or errors.append("input file: `%s` does not have the required extension of `.vcf.gz`" % vcf)
    path.isfile(vcf) or errors.append("input file: `%s` does not exists" % vcf)
    path.isdir(ref) or errors.append("reference data dir `%s` does not exists" % ref)

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)

    work_dir = path.join(path.dirname(vcf), '_workdir')
    print("Working dir is: %s" % work_dir)    

    if not path.isdir(work_dir):
        os.makedirs(work_dir)
    

    if not path.islink(path.join(work_dir, path.basename(vcf))):
        os.symlink(vcf, path.join(work_dir, path.basename(vcf)))


    base_sample = path.basename(vcf)[0:-len(vcf_ext)]
    print("Base sample name: %s" %base_sample)


    config = dict()
    process_steps = [base_sample]
    qc and ('QC' |cons| process_steps) and True # (config['qc_filter'] = qc_filter)
    (bi_snp and non_missing and 'BiSnpNM' |cons| process_steps) or \
        (bi_snp and 'BiSnp' |cons| process_steps) or \
        (non_missing and 'NM' |cons| process_steps) 
    maf and ("MAF@%s" % maf_min) |cons| process_steps
    ld_prune and 'LD' |cons| process_steps
    phase and ('RPH' if phase_with_ref else 'PH') |cons| process_steps


    rel_sample = "_".join(process_steps)
    print("Ref sample: %s" % rel_sample)
    print("XConfig: %s" % config)

    config = dict(rel_sample = rel_sample, 
        ref_dir = ref, 
        rel_true= '')
    config_filename = path.join(work_dir, 'config.yaml')
    print("Writing configuration: %s to config file %s" % (config, config_filename))
    with open(config_filename, "w") as cf:
        yaml.dump(config, cf, default_flow_style=False)
    # fail if config already exists

    os.system("./tribes -d %s estimate_degree" % work_dir)


    shutil.copy2(path.join(work_dir, rel_sample + "_GRM-allchr_FPI_IBD.csv"), output + ".csv")

    if (output_segments):
        shutil.copy2(path.join(work_dir, rel_sample + "_GRM-allchr_FPI_IBD-segments.match.gz"), output + "-segments.match.gz")

if __name__ == '__main__':
    estimate()


