#!/bin/bash -l
#$ -P project_name #required
#$ -l h_rt=24:00:00
#$ -N mqpar_jo
#$ -j y
#$ -pe omp 28
#$ -m e

# Load modules

module load mono/6.10.0
module load maxquant/1.6.17.0
module load python3/3.7.7

############################# REQUIRED REQUIRED REQUIRED REQUIRED REQUIRED REQUIRED
out=/directory/to/path/out
pyscript=/path/to/create_xml-v2.py
shscript='qsub_mqpar-v2'
echo '.sh script:' $shscript
echo '.py script:' $pyscript
############################# REQUIRED REQUIRED REQUIRED REQUIRED REQUIRED REQUIRED 

arg1=$1
arg2=$2
arg3=$3
arg4=$4
timestamp=$5
signature=$6
echo $arg1 $arg2 $arg3 $arg4 $timestamp $signature
####################################################

python $pyscript \
    $arg1 \
    $arg2 \
    $arg3 \
    $arg4 \
    $timestamp \
    $signature 
####################################################

mkdir $out/$timestamp

####################################################
mkdir $TMPDIR/combine/
mkdir $TMPDIR/index/
mkdir $TMPDIR/temp/ #####

cd $TMPDIR
MaxQuantCmd $timestamp.mqpar.$signature.xml #######
mv $TMPDIR/*mqpar* $out/$timestamp/
mv $TMPDIR/combined $out/$timestamp/ # combine
mv $TMPDIR/index $out/$timestamp/
mv $TMPDIR/temp $out/$timestamp/ #####
