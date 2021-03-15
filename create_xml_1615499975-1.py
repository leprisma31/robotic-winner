#!/usr/bin/python
################################################## python3 imports
import sys
#import re
import regex as re
import time
import csv
import pandas
import os
import argparse
import shutil 
################################################## script help page
parser = argparse.ArgumentParser()
parser.add_argument("1.",help="Path to sample,experiment file.")
parser.add_argument("2.",help="Path to parameter reference file.")
parser.add_argument("3.",help="Path to select parameters.")
parser.add_argument("4.",help="Path to xml file template.")
parser.add_argument("5.",help="Terminal time stamp syntax.")
parser.add_argument("6.",help="Signature.") #####
parser.parse_args()
################################################## sys.argv[n]


os.putenv("se", sys.argv[1]) 
os.putenv("rf", sys.argv[2]) 
os.putenv("sp",sys.argv[3])
os.putenv("xmlt", sys.argv[4])
os.putenv("stid", sys.argv[5])
os.putenv("sign",sys.argv[6])

TMPDIR=os.environ.get("TMPDIR")
Nslots=int(os.environ.get("NSLOTS"))

se=sys.argv[1]
rf=sys.argv[2]
sp=sys.argv[3]
xmlt=sys.argv[4]
stid=sys.argv[5]
sign=sys.argv[6]


##################################################
################################################## Directory Paths
outpath='/path/to/out'
##################################################
##################################################

def create_filepaths_dictionary(se):
    d={}
    k1='filePaths'
    k2='experiments'
    with open(se,'r') as file:
        for line in file.read().split('\n'):
            line=line.strip()
            if line == '':
                break #!
            else:
	            line=line.split(',')
	            d.setdefault(k1,[]).append(line[0])
	            d.setdefault(k2,[]).append(line[1])
    return d,len(d)
##################################################
def create_parameters_dictionary(rf,TMPDIR,sp):
    with open(rf,'r') as file1:
        reference={}
        for line in file1.read().split('\n'):
            line=line.strip()
            parameter=line.split(',')
            t_f=parameter[1] in  ['GUI-1','GUI-2','filePaths','experiments','string','boolean','int','short','referenceChannel','labelMods']
            if parameter[2] == '' and t_f == True:
            	reference[parameter[1]]=''
            else:
                reference[parameter[1]]=parameter[2]
    
    with open(sp,'r') as file2:
        trial={}
        for line in file2.read().split('\n'):
            line=line.strip()
            parameter=line.split(',')
            trial[parameter[0]]=parameter[1] # 2 columns
    reference.update(trial)
    return reference

##################################################
def create_xml(xml,pad,stid,TMPDIR,sign): ###########
    filename=stid+'.mqpar.'+sign+'.xml' ############
    pad['fixedSearchFolder']=TMPDIR+'/index'
    pad['fixedCombinedFolder']=TMPDIR+'/combine'
    pad['tempFolder']=TMPDIR+'/temp'
    pad['numThreads']=Nslots
    print('# Samples',pad['numSamples'])
    print('Project:',pad['project'])
    template=open(xml,'r')

    newFile=open(TMPDIR+'/'+filename,'w') ###########
    for line in template.read().split('\n'):
        line=line.strip() #!
        if bool(re.search(r'>(.*?)</',line)): # <tag></tag>
            i=line.find('</')
            te=line[i+2:-1]
            if te in pad: ##### !!!!!
                if te in ['short','boolean','int','string']:
                    newFile.write('')
                else:
                    v=pad[te]
                    v='>'+str(v)+'</'
                    print(v,line)
                    lineNew=re.sub(r'>(.*?)</',v,line)+'\n'
                    newFile.write(lineNew)
            else: 
                line=line+'\n'
                newFile.write(line) 
        elif bool(re.search(r'<([a-zA-Z]+)>',line)): # <tag>
            i=line.find('<')
            te=line[i+1:-1]
            if te in pad:
                if te == 'restrictMods': # list of modifications
                    rm=pad['restrictMods']
                    if rm == '':
                        newFile.write('<restrictMods>'+'\n')
                    else:
                        rm=rm.split(';')
                        newFile.write('<restrictMods>'+'\n')
                        for i in range(len(rm)):
                            lineNew='<string>'+rm[i]+'</string>'+'\n'
                            newFile.write(lineNew)
                elif te == 'fixedModifications': # 1 modification
                    lineNew='<fixedModifications>'+'\n'+'<string>'+pad['fixedModifications']+'</string>'+'\n'
                    newFile.write(lineNew)
                elif te == 'enzymes': # 1 enzyme
                    lineNew='<enzymes>'+'\n'+'<string>'+pad['enzymes']+'</string>'+'\n'
                    newFile.write(lineNew)
                elif te == 'referenceChannel': #  default ''
                    newFile.write('<referenceChannel>'+'\n')
                    for i in range(int(pad['numSamples'])): #numSamples
                        lineNew='<string></string>'+'\n'
                        newFile.write(lineNew)
                elif te == 'labelMods':
                    lineNew='<labelMods>'+'\n'+'<string></string>'+'\n'
                    newFile.write(lineNew)
                elif te == 'paramGroupIndices':
                    newFile.write('<paramGroupIndices>'+'\n')
                    for i in range(int(pad['numSamples'])): #numSamples
                        lineNew='<int>0</int>'+'\n'
                        newFile.write(lineNew)
                elif te == 'ptms':
                    newFile.write('<ptms>'+'\n')
                    for i in range(int(pad['numSamples'])): #numSamples
                        lineNew='<boolean>False</boolean>'+'\n'
                        newFile.write(lineNew)
                elif te == 'fractions':
                    newFile.write('<fractions>'+'\n')
                    for i in range(int(pad['numSamples'])): #numSamples
                        lineNew='<short>'+pad['fractions']+'</short>'+'\n'
                        newFile.write(lineNew)
                elif te == 'experiments': ###
                    newFile.write('<experiments>'+'\n')
                    exper=pad['experiments']
                    for key in exper:
                        lineNew='<string>'+key+'</string>'+'\n'
                        newFile.write(lineNew)
                elif te == 'filePaths':
                    newFile.write('<filePaths>'+'\n')
                    rw=pad['filePaths']
                    for key in rw:
                        lineNew='<string>'+key+'</string>'+'\n'
                        newFile.write(lineNew)
                else: ###### !
                    lineNew='<'+te+'>'+'\n'
                    newFile.write(lineNew)
            else: ####### !
                line=line+'\n'
                newFile.write(line)
        else: 
            line=line+'\n'
            newFile.write(line)
    print('fixedSearchFolder:',pad['fixedSearchFolder'])
    print('fixedCombinedFolder:',pad['fixedCombinedFolder'])
    print('tempFolder:',pad['tempFolder'])
    print('numThreads:',pad['numThreads'])
    print('filename:',filename)
    print('Project:',pad['project'])
    newFile.close() ###########
################################################## 
out1,N=create_filepaths_dictionary(se)
out2=create_parameters_dictionary(rf,TMPDIR,sp)
out2.update(out1)
out2.update({'numSamples':str(N)})
create_xml(xmlt,out2,stid,TMPDIR,sign) # 


################################################## Parameter CSV File
with open(outpath+'/'+stid+'/'+stid+'.parameters.'+sign+'.csv', 'w') as f: 
    for key in out2.keys():
        f.write("%s,%s\n"%(key,out2[key]))
    #f.write('Sample-Experiment:,'+se+'\n')
    #f.write('Parameter Reference File:,'+rf+'\n')
    #f.write('Select parameters:,'+sp+'\n')
    #f.write('xml template:,'+xmlt+'\n')
    #f.write('Time Stamp:,'+stid+'\n')
    #f.write('Signature:,'+sign+'\n')


##################################################

print('##################################################')
print('# of Additional Required Path(s): 3')
print('Paths May Need to be Modified:')
##################################################
print('##################################################')
print('Sample-Experiment:',se)
print('Parameter Reference File:',rf)
print('Select parameters:',sp)
print('xml template:',xmlt)
print('Time Stamp:',stid)
print('Signature:',sign)

################################################## 
print('##################################################')

################################################## Transfer files







