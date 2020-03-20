#!/usr/bin/env python

import sys
import click
import yaml
from os import path
import os
from click_option_group import OptionGroup
import shutil
import subprocess
from _version import __version__ 
import hashlib
import time


DEF_QC_FILTER='INFO/MQ>59 & INFO/MQRankSum>-2 & AVG(FORMAT/DP)>20 & AVG(FORMAT/DP)<100 & INFO/QD>15 & INFO/BaseQRankSum>-2 & INFO/SOR<1'
ROOT_DIR = path.abspath(path.dirname(__file__))
VCF_GZ_EXT = '.vcf.gz'


def hash_obj(obj, hash_size = 4):
    return hashlib.blake2b(str(obj).encode(), digest_size = hash_size).hexdigest()

class ApplicationError(Exception):
    def __init__(self, msg):
        self.msg = msg


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

class Context:
    def __init__(self, yes, verbose):
        self._yes = yes
        self._verbose = verbose

    def debug(self, msg):
        if self._verbose:
            click.echo("DEBUG: %s" % msg)

    def echo(self, msg):
        click.echo(msg)

    def info(self, msg):
        click.echo(msg)

    def warn(self, msg):
        click.echo("WARN: %s" % msg)

    def error(self, msg):
        click.echo("ERROR: %s " % msg)

    def raise_error(self, msg):
        raise ApplicationError(msg)

    def confirm(self, msg):
        if self._yes:
            self.debug("Responding YES to: %s" % msg)
            return True
        else:
            return click.confirm(msg)

class TribesDir:

    def __init__(self, input_file, work_dir, config, base_sample, rel_sample, output_estimate, output_segments):
        self._input_file = input_file
        self._work_dir = work_dir
        self._config = config
        self._base_sample = base_sample
        self._rel_sample = rel_sample
        self._output_estimate = output_estimate
        self._output_segments = output_segments

    @property
    def work_dir(self):
        return self._work_dir
    
    def exists(self):
        return path.exists(self._work_dir)

    def is_workdir(self):
        return path.isdir(self._work_dir) and path.isfile(path.join(self._work_dir,'.tribes'))

    def clean(self, ctx):
        if self.exists():
            if self.is_workdir():
                if ctx.confirm("Do you want to remove the working directory: '%s'?" % self._work_dir):
                    ctx.debug("Deletig working directory: '%s'." % self._work_dir)
                    shutil.rmtree(self._work_dir, ignore_errors=True)
            else:
                raise ApplicationError("Path '%s' exits but cannot be cleaned becasue is not a TRIBES workdir." % self._work_dir)

    def _ensure_exits(self, ctx):
        if path.exists(self._work_dir) and not path.isdir(self._work_dir):
            raise ApplicationError("Path '%s' for workdir exits but is not a directory." % self._work_dir)
        if not path.isdir(self._work_dir):
            os.makedirs(self._work_dir)
            with open(path.join(self._work_dir,'.tribes'), 'w') as token:
                token.write("TRIBES")
        elif self.is_workdir():
            pass
            ctx.debug("Using an existing working dir: '%s'" % self._work_dir)
        else:
            raise ApplicationError("The dir '%s' already exists but is not a `TRIBES` working directory." % self._work_dir)



    def _write_config(self, ctx, config, force = False):
        config_filename = path.join(self._work_dir, 'config.yaml')

        # check if the config exists in the working dir
        # and if yes than if it matches 
        if path.isfile(config_filename):
            ctx.debug("There is an existing config file at: '%s'" % config_filename)
            with open(config_filename, 'r') as ef:
                existing_config = yaml.load(ef, Loader=yaml.FullLoader)
            ctx.debug("The existing config is: %s" % existing_config)
            if existing_config != config:
                if not force:
                    raise ApplicationError(
"""The existing configuration in working directory: '%s' does not match the current set of options.
Remove this directory or use `--clean` to cleanup the directory and run the new configuration.
""" % self._work_dir)
                else:
                    ctx.warn("Forcing excution unclean directory despite mismatching options. The results mayby incorrect")

        ctx.debug("Writing configuration: %s to config file %s" % (config, config_filename))
        with open(config_filename, "w") as cf:
            yaml.dump(config, cf, default_flow_style=False)


    def _link_input(self, ctx, input_file):
        workdir_input = path.join(self._work_dir, self._base_sample + VCF_GZ_EXT)
        if not path.exists(workdir_input):
            #Debubg linking file
            os.symlink(input_file, workdir_input)
        elif not path.islink(workdir_input) or (path.realpath(workdir_input) != path.realpath(input_file)):
            raise ApplicationError("The working dir input file: '%s' is not a link or \
does not point to input '%s'. (Points to: '%s' instead." %  
                    (workdir_input, path.realpath(input_file), path.realpath(workdir_input)))

    def initialize(self, ctx, force=False):
        self._ensure_exits(ctx)
        self._write_config(ctx, self._config, force)
        self._link_input(ctx, self._input_file)

    def run_snakemake(self, ctx, options=''):
        #change to running with subprocess.run
        cmd = "%s -d %s %s estimate_degree" % (path.join(ROOT_DIR,'tribes-snakemake'), 
            self._work_dir, options)
        ctx.debug("Running snakemake with cmd: '%s'." % cmd)
        result = subprocess.run(cmd.split(), stdout = None, stderr = None)
        exit_code = result.returncode
        if exit_code != 0:
            raise ApplicationError("Snakemake execution failed with exit code: %s." % exit_code)

    def _save_estimate(self, ctx, output_path):
        work_estimate_path = path.join(self._work_dir, self._rel_sample + "_GRM-allchr_FPI_IBD.csv")
        ctx.debug("Saving degree estimate to: '%s' from: '%s'." % (output_path, work_estimate_path))
        shutil.copy2(work_estimate_path, output_path)

    def _save_segments(self, ctx, output_path):
        work_segments_path = path.join(self._work_dir, self._rel_sample + "_GRM-allchr_FPI_IBD-segments.match.gz")
        ctx.debug("Saving IBD segments to: '%s' from: '%s'." % (output_path, work_segments_path))
        shutil.copy2(work_segments_path, output_path)

    def save_outputs(self, ctx):
        self._output_estimate and self._save_estimate(ctx, self._output_estimate)
        self._output_segments and self._save_segments(ctx, self._output_segments)

class TribesPipeline():

    @classmethod
    def _build_pipeline(cls, bi_snp, qc, qc_filter, maf, maf_min, ld_prune, non_missing, phase, phase_with_ref, **kwargs):
        config = dict()
        process_steps = []
        qc and ('QC' |cons| process_steps) and config.__setitem__('qc_filter', qc_filter)
        (bi_snp and non_missing and 'BiSnpNM' |cons| process_steps) or \
            (bi_snp and 'BiSnp' |cons| process_steps) or \
            (non_missing and 'NM' |cons| process_steps) 
        maf and ("MAF@%s" % maf_min) |cons| process_steps and config.__setitem__('maf_min', maf_min)
        ld_prune and 'LD' |cons| process_steps 
        phase and ('RPH' if phase_with_ref else 'PH') |cons| process_steps
        return process_steps, config

    @classmethod
    def create(cls, input_vcf, ref_dir, base_sample, output_estimate = None, output_segments = None, **kwargs):
        process_steps, config = TribesPipeline._build_pipeline(**kwargs)
        return TribesPipeline(input_vcf, ref_dir, base_sample, process_steps, config, output_estimate, output_segments)

    def __init__(self, input_vcf, ref_dir, base_sample, steps, config, output_estimate = None, output_segments = None):
        self.input_vcf = input_vcf
        self.ref_dir = ref_dir
        self.base_sample = base_sample
        self.steps = steps
        self.config = config
        self.output_estimate = output_estimate
        self.output_segments = output_segments

    @property
    def rel_sample(self):
        return  "_".join([self.base_sample] + self.steps)


    def validate(self):
        errors = []
        self.input_vcf.endswith('.vcf.gz') or errors.append("input file: `%s` does not have the required extension of `.vcf.gz`" % self.input_vcf)
        path.isfile(self.input_vcf) or errors.append("input file: `%s` does not exists" % self.input_vcf)
        path.isdir(self.ref_dir ) or errors.append("reference data dir `%s` does not exists" % self.ref_dir)
        return errors


    def create_executor(self, work_dir):
        pipeline_config = dict(input_vcf = self.input_vcf,
            rel_sample = self.rel_sample, 
            ref_dir = self.ref_dir, rel_true= '', 
            ** self.config)
        pipeline_config_hash = hash_obj(pipeline_config)
        return TribesDir(self.input_vcf, work_dir.format(pipeline_config_hash), pipeline_config, 
            self.base_sample,
            self.rel_sample,
            self.output_estimate, self.output_segments)

    def __str__(self):
        return """Tribes Pipeline:
    VCF input: '%s'
    Ref data dir: '%s'
    Base sample: '%s'
    Preprocessing: %s
    Config: %s
    Relatedness output: %s
    Segments output: %s""" % (self.input_vcf, self.ref_dir, self.base_sample, self.steps, self.config, 
        self.output_estimate, self.output_segments)


#
# The actual command line interface
#

pipeline = OptionGroup('PIPELINE', help='Pipeline configuation\n')
io = OptionGroup('INPUT/OUTPUT', help='Input/output configuration\n')
ctl = OptionGroup('CONTROL', help='Execution control\n')


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
        help='Peform ld pruning with R2 of 0.95')
@pipeline.option('--phase/--no-phase', required = False, default = True, is_flag = True, show_default=True,
        help='Peform phasing')
@pipeline.option('--phase-with-ref/--phase-without-ref', required = False, default = True, is_flag = True, show_default=True,
        help='Phase with reference')
@ctl.option('--clean', required = False, default = False, is_flag = True, show_default=True,
        help='Clean the working directory before execution')
@ctl.option('--force', required = False, default = False, is_flag = True, show_default=True,
        help='Force execution on uncleaned directory')
@ctl.option('--work-dir', required = False, default = None, type=str, show_default=True,
        help='Working directory.')
@ctl.option('--keep-work-dir', required = False, default = False, is_flag=True, show_default=True,
        help='Keeps the working directory after sucessful execution.')
@click.option('--yes', required = False, default = False, is_flag=True, show_default=True,
        help='Answer yes to all prompts')
@click.option('--verbose', required = False, default = False, is_flag=True, show_default=True,
        help='Be more verobose')
@click.option('--snakemake-opts', required = False, default = "", type=str, show_default=False,
        help='Extra options to pass to snakemake.')

def estimate(vcf, ref, output,
    output_segments, work_dir, keep_work_dir, yes, clean, force, verbose, snakemake_opts, **pipeline_opts):
    """ Estimate relatedness using IBD0
    """
    tribes = None
    try:
        ctx = Context(yes, verbose)
        ctx.echo("TRIBES version: %s\n" % __version__)
        ctx.echo("Estimating relatedness using IBD0.")

        # Echo parameters
        ctx.debug("Options in effect: %s." % click.get_current_context().params)

        if not vcf.endswith(VCF_GZ_EXT):
            ctx.raise_error("Input file: `%s` does not have the required extension of `.vcf.gz`." % vcf)

        base_sample = path.basename(vcf)[0:-len(VCF_GZ_EXT)]
        ctx.debug("Base sample name: %s" %base_sample)
        pipeline = TribesPipeline.create(vcf, ref, base_sample, 
            output + "-estimate.csv", output + "-segments.match.gz" if output_segments else None,
            **pipeline_opts)

        errors = pipeline.validate()
        errors and ctx.raise_error("\n- ".join(["There were errors in pipeline validation:"] + errors))

        ctx.echo(str(pipeline))
        if work_dir is None:
            work_dir = path.join(path.dirname(vcf), '_tribes_{0}')
            ctx.debug("Defaulting working dir to: '%s'" % work_dir)

        tribes = pipeline.create_executor(work_dir)
        ctx.echo("Working dir is: '%s'." % tribes.work_dir)    
        if clean:
            tribes.clean(ctx)
        tribes.initialize(ctx, force)
        ctx.info("\nRuning `tribes-snakemake` in working dir: '%s' ...\n" % tribes.work_dir)
        tribes.run_snakemake(ctx, snakemake_opts)
        ctx.info("\n... `tribes-snakemake` sucessful.\n")
        tribes.save_outputs(ctx)
        if not keep_work_dir:
            tribes.clean(ctx)
        ctx.info("Done.")
    except ApplicationError as e:
        ctx.error(e.msg)
        if tribes and tribes.exists():
            ctx.warn("The working directory: '%s' was not removed. Please remove it manually if needed." % tribes.work_dir)
        ctx.echo("Exiting...")
        exit(1)

if __name__ == '__main__':
    print(__file__)
    estimate()


