# robotic-winner


MaxQuant is a quantitative proteomics software package designed by the  Max Planck Institute for analyzing large-scale mass-spectrometric data sets. You can download the Max Planck Institute's GUI software at https://www.biochem.mpg.de/6304115/maxquant. 

I created a python3—shell compatible—script
which generates an XML file to be read by the MaxQuant executable
program. The XML file is similar in structure to the HTML mark-up
language, and the .py script accepts tab-delimited file(s) including
specified html </tag> values (select_tags.txt), the 10 parameters required to execute the non-gui MaxQuant
program.

The qsub_mqpar-vX.sh (qsub_mqpar-v1.sh or qsub_mqpar-v2.sh) bash script accepts file paths to:

1) a create_xml-vX.py script # either (if qsub_mqpar-v1.sh: create_xml-v1.py or create_xml-v2.py if qsub_mqpar-v2.sh)
2) an `out` directory
3) and to an environment variable, `$TMPDIR` 

The create_xml-vX.py script requires 6 arguments.
The code (lines 12-19) generates a .xml file for MaxQuant review of .raw (proteomics) data. 

qsub ./qsub_mqpar-vX.sh \
     ./metadata.txt \ # "," delimited text file with path locations to .raw files & the file label (of the sample)
     ./required.txt \ # required
     ./select_tags.txt \ # , delimited text file with xml tag-name, followed by a select 'value' (required)
     ./11TMT.xml \ # referece parameter xml file
     $(date +%s) # time 
     Signature # name



