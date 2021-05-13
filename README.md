# robotic-winner

The qsub_mqpar-vX.sh bash script accepts file paths to:

1) a create_xml-vX.py script
2) an `out` directory
3) and to an environment variable, `$TMPDIR` 

The create_xml-vX.py script requires 6 arguments.
The code (lines 12-19) generate a .xml file for MaxQuant review of .raw (proteomics) data:

qsub ./qsub_mqpar-vX.sh \
     ./metadata.txt \ # , delimited text file with path locations to .raw files, file label
     ./required.txt \ # required
     ./select_tags.txt \ # , delimited text file with xml format tag-name,value
     ./11TMT.xml \ # referece parameter xml file
     $(date +%s)
     Signature



