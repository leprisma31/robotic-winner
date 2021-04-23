# robotic-winner

The qsub_mqpar-vX.sh bash script accepts file paths to:

1) a create_xml-vX.py script
2) an `out` directory
3) and to an environment variable, `$TMPDIR` 

The create_xml-vX.py script requires 6 arguments.
The code generates a .xml file for MaxQuant review of .raw (proteomics) data:

qsub ./qsub_mqpar-vX.sh \
     ./metadata.txt \ # , delimited text file with locations to .raw files, file label
     ./reference.txt \ # , delimited textfile with tag name,value
     ./select_tags.txt \ # , delimited text file with tag name,value
     ./xml_template.xml \ # xml template
     $(date +%s)
     Signature



