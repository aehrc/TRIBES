import click
from functools import update_wrapper
import re
from os import path
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.functions import *
from pyspark.sql.types import *

@click.group()
def cli():
    pass

def with_spark(func):
    def do(**kwargs):
        click.echo("Creating spark session")
        conf = SparkConf().set('spark.driver.memory','10G')
        spark = SparkSession.Builder().config(conf=conf).getOrCreate()
        return func(spark,spark.sparkContext, **kwargs)
    return update_wrapper(do, func)



GERMLINE_SCHEMA_FIX = StructType()\
    .add("Fam1_Id1", StringType()) \
    .add("Fam2_Id2", StringType()) \
    .add("Chr", StringType()) \
    .add("SegStart_SegEnd", StringType()) \
    .add("SnpStart_SnpEnd", StringType()) \
    .add("NoSnp", IntegerType()) \
    .add("Length", DoubleType()) \
    .add("Unit", StringType()) \
    .add("NoMismatch", IntegerType()) \
    .add("Res1", StringType()) \
    .add("Res2", StringType()) 

GERMLINE_SCHEMA = StructType()\
    .add("Fam1", StringType()) \
    .add("Id1", StringType()) \
    .add("Fam2", StringType()) \
    .add("Id2", StringType()) \
    .add("Chr", StringType()) \
    .add("SegStart", IntegerType()) \
    .add("SegEnd", IntegerType()) \
    .add("SnpStart", StringType()) \
    .add("SnpEnd", StringType()) \
    .add("NoSnp", IntegerType()) \
    .add("Length", DoubleType()) \
    .add("Unit", StringType()) \
    .add("NoMismatch", IntegerType()) \
    .add("Res1", StringType()) \
    .add("Res2", StringType())

@cli.command()
@click.argument('input')
#@click.argument('output')
@with_spark
def ibd(spark, sc, input):
    """ Convert the full graph to the plain edges representation with numerical ids
        to be used by dga or as an input for further conversion to metis
    """
    df = spark.createDataFrame(sc.textFile(input)\
        .map(str.split), StructType([StructField(f.name, StringType()) for f in GERMLINE_SCHEMA.fields]))\
        .select(*[col(f.name).cast(f.dataType) for f in GERMLINE_SCHEMA.fields])
    ibd_per_pair = df.groupBy(col('Id1'), col('Id2')).sum('Length')
    ibd_per_pair.show()
@cli.command()
@click.argument('input')
#@click.argument('output')
@with_spark
def ibd2(spark, sc, input):
    """ Convert the full graph to the plain edges representation with numerical ids
        to be used by dga or as an input for further conversion to metis
    """
    raw_df = spark.read.csv(input, sep='\t', schema=GERMLINE_SCHEMA_FIX)
    df = raw_df.select(
        split(col('Fam1_Id1'),' ')[1].alias('Id1'),
        split(col('Fam2_Id2'),' ')[1].alias('Id2'),
        col('Length')
    )
    ibd_per_pair = df.groupBy(col('Id1'), col('Id2')).sum('Length')
    ibd_per_pair.show()


if __name__ == '__main__':
    cli()
