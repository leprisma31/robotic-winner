#!/bin/bash -l
#$ -P project
#$ -l h_rt=24:00:00
#$ -N batch.jo
#$ -j y
#$ -pe omp 28
#$ -m e
#$ -M email@email.com

# Load modules

module load mono/6.10.0
module load maxquant/1.6.17.0
module load python3/3.7.7

out.txt=./out.txt
batch=$1
signature=$2
out=./out/MQ$(date +%s)/
pyscript=./create_xml-vX.py

while IFS=, read -r field1 field2 field3 field4
do
	timestamp=$(date +%s)
	python $pyscript $field1 $field2 $field3 $field4 $timestamp $signature
	PATH=$out/$timestamp
	mkdir -p $PATH $TMPDIR/index/ $TMPDIR/temp/
	cd $TMPDIR 
	MaxQuantCmd $tiemstamp.mqpar.$signature.xml
	mv $TMPDIR/*mqpar* $TMPDIR/combined/ $TMPDIR/index/ $TMPDIR/temp/ $PATH
	find $PATH/combined/txt -type f -name peptides* -print >> $out.txt
done < batch.txt