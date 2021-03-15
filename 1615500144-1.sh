#!/bin/bash -l
#$ -P #project
#$ -l h_rt=24:00:00
#$ -N mqpar_jo
#$ -j y
#$ -pe omp #n
#$ -m e
#$ # -M email@email
#$ -l cpu_arch=!bulldozer

# Load modules

module load mono/6.10.0
module load maxquant/1.6.17.0
module load python3/3.7.7

############################# out directory
outpath1=/path/to/out
############################# required arguments

arg1=$1
arg2=$2
arg3=$3
arg4=$4
timestamp=$5
signature=$6

############################# new directories
mkdir $outpath/$timestamp
mkdir $outpath/$timestamp/combine/
mkdir $outpath/$timestamp/index/


############################# script
python ./1615499975-1.py \
    $arg1 \
    $arg2 \
    $arg3 \
    $arg4 \
    $timestamp \
    $signature 

echo 'Bash: ' python ./1615499975-1.py \
    $arg1 \
    $arg2 \
    $arg3 \
    $arg4 \
    $timestamp \
    $signature

############################# run MaxQuant @ TMPDIR
cd $TMPDIR
MaxQuantCmd $TMPDIR/$timestamp.mqpar.$signature.xml

############################# transfers

mv $TMPDIR/*.xml $outpath/$timestamp/
mv $TMPDIR/combine $outpath/$timestamp/combine/
mv $TMPDIR/index $outpath/$timestamp/index/

