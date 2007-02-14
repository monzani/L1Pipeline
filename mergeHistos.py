#!/usr/bin/env python

from os import system, environ

glastRoot='/afs/slac/g/glast'
cmtConfig='rh9_gcc32opt'
rootSys=glastRoot+'/ground/GLAST_EXT/'+cmtConfig+'/ROOT/v4.02.00/root'
glastExt=glastRoot+'/ground/GLAST_EXT/'+cmtConfig
cmtPath='/afs/slac/g/glast/ground/releases/volume07/EngineeringModel-v6r070329p29em1:/afs/slac/g/glast/ground/PipelineConfig/SC/L1Pipeline/builds'

reportMergeApp=glastRoot+'/ground/PipelineConfig/SC/L1Pipeline/builds/TestReport/v3r6p36/'+cmtConfig+'/MergeHistFiles.exe'

environ['LD_LIBRARY_PATH']=""
environ['ROOTSYS']=rootSys
environ['CMTPATH']=cmtPath

system("source /afs/slac/g/glast/ground/scripts/group.sh; CMTCONFIG="+cmtConfig+"; export CMTCONFIG; GLAST_EXT="+glastExt+"; export GLAST_EXT; cd /afs/slac/g/glast/ground/PipelineConfig/SC/L1Pipeline/builds/TestReport/v3r6p36/cmt; source setup.sh; LD_LIBRARY_PATH=$LD_LIBRARY_PATH:"+glastExt+"/xerces/2.6.0/lib; export LD_LIBRARY_PATH; "+reportMergeApp+" -I $Larry_L1ProcROOT/inputFiles.txt -o $TestDir/merged_digi_hist.root -c $Larry_L1ProcROOT/merge.txt; chgrp -R glast-pipeline $TestDir")
