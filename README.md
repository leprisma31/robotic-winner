# robotic-winner


MaxQuant is a quantitative proteomics software package designed by the  Max Planck Institute for analyzing large-scale mass-spectrometric data sets. You can download the Max Planck Institute's software & or the MaxQuant gui at https://www.biochem.mpg.de/6304115/maxquant. 

I created a shell-python3 compatible script (`qsub_mqpar-v1.sh` if `create_xml-v1.py` or `qsub_mqpar-v2.sh` if `create_xml-v2.py`)  which generates an XML file from a template file, `11TMT.txt`, & accepts tag values from `required.txt` & `select_tags.txt`, select-tags.txt, which includes 10 specified html </tag> values, required to execute the MaxQuant program. `metadata.txt` & `UP000005640_9606.fasta`,  is a ',' delimited list of proteomics samples names with their path locations or a .fasta file, respectively. The new XMl file is then read by the executable (non-gui) MaxQuant program, & the .py script directs out files to paths listed in `out.txt`. 
The scripts includes 'module load' or 'qsub' comands & requires installation of mono/6.10.0, maxquant/1.6.17, or python3/3.7.7 .     


***** select_tags.txt includes parameters for 10 tags, which * may vary depending on the (your) proteomics experiment: 
Project, TMT11 # your project name\
includeContaminants,True # * can be modified\
minpeplen,7 # * can be modified\
minuniquepeptides,0 # * can be modified\
restrictMods, # not included in 11TMT.txt, the list of accepted modifications are viewable by the MaxQuant GUI \
fixedModifications, # not included in 11TMT.txt, the list of accepted modifications are viewable by the MaxQuant GUI\ 
fastafilePath,C:\Users\nslavov\Desktop\swissprot_human_20180730.fasta # * can be modified\
identifierparserule,>([^\s]*) # * can be modified\
descriptionparserule,>(.*) # * can be modified\
enzymes,Trypsin/P # * can be modified\


The qsub_mqpar-vX.sh (qsub_mqpar-v1.sh or qsub_mqpar-v2.sh) bash script accepts file paths to:

1) a create_xml-vX.py script # either (if qsub_mqpar-v1.sh: create_xml-v1.py or create_xml-v2.py if qsub_mqpar-v2.sh)
2) an `out` directory which contains directories & summary table(s) of proteomics analyses including a peptides.txt file
3) and to an environment variable, `$TMPDIR` 

The create_xml-vX.py script requires 6 arguments.
The code (lines 32-38) generates a .xml file for MaxQuant review of .raw (proteomics) data. 

qsub ./qsub_mqpar-vX.sh \
     ./metadata.txt # "," delimited text file with path locations to .raw files & the file label (of the sample)\
     ./required.txt # required\
     ./select_tags.txt # , delimited text file with xml tag-name, followed by a select 'value' (required)\
     ./11TMT.xml # referece parameter xml file\
     $(date +%s) # time\
     Signature # name\



