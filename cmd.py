#!/usr/bin/env python

import sys
import click
import yaml
from os import path
import os

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


@click.group()
@click.option('--noop', help='Name to greet', is_flag=True)
@click.option('--verbose', help='Name to greet', is_flag=True)
def cli(noop, verbose):
    pass


@cli.command()
@click.option('--vcf', required = True, default = None, type=str)
@click.option('--ref', required = True, default = None, type=str, 
        help='Reference data directory')
@click.option('--qc/--no-qc', required = False, default = False, is_flag = True, 
        help="apply quality control filter defined in BCF_FILTER_EXPR.")
@click.option('--qc-filter', required = False, default = None, type=str, metavar = 'BCF_FILTER_EXPR', 
        help="bcftools filter expression to use in qc step.")
@click.option('--non-missing/--no-non-missing', required = False, default = True, is_flag = True)
@click.option('--bi-snp/--no-bi-snp', required = False, default = True, is_flag = True)
@click.option('--maf/--no-maf', required = False, default = True, is_flag=True,
        help='Filter out loci with minor allele frequency less than given.')
@click.option('--maf-min', required = False, default = 0.01, type=float,
        help='Filter out loci with minor allele frequency less than given.')
@click.option('--ld-prune/--no-ld-prune', required = False, default = False, is_flag = True, 
        help='Peform ld prunning')
@click.option('--phase/--no-phase', required = False, default = True, is_flag = True, 
        help='Peform ld prunning')
@click.option('--phase-with-ref/--phase-without-ref', required = False, default = True, is_flag = True, 
        help='Peform ld prunning')
def estimate(vcf, ref, bi_snp, qc, qc_filter, maf, maf_min, ld_prune, non_missing, phase, phase_with_ref,  **flags):
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
    #path.isdir(ref) or errors.append("reference data dir `%s` does not exists" % ref)

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)

    work_dir = path.dirname(vcf)
    print("Working dir is: %s" % work_dir)    

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


if __name__ == '__main__':
    cli()


