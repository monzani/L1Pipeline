#!/usr/bin/env python

"""@brief Merge results of chunk or crumb processing.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
from os import environ

import re
import sys

#import runner

import config

import fileNames
import stageFiles

staged = stageFiles.StageSet()

fileType = environ['fileType']
dlId = environ['DOWNLINK_ID']
runId= environ['RUNID']
chunkId = environ.get('CHUNK_ID')

if chunkId is None:
    mergeLevel = 'run'
else:
    mergeLevel = 'chunk'
    pass

files = fileNames.setup(dlId, runId, chunkId)

realInFiles = fileNames.findPieces(fileType, dlId, runId, chunkId)
inFiles = [staged.stageIn(iFile) for iFile in realInFiles]

realOutFile = files[mergeLevel][fileType]
outFile = staged.stageOut(realOutFile)

##wbf## system(config.hadd+" "+environ['outFile']+" "+environ['inFiles'])

if fileType in ['digiMon', 'reconMon']:

 glastRoot='/afs/slac/g/glast'
 cmtConfig='rh9_gcc32opt'
 rootSys=glastRoot+'/ground/GLAST_EXT/'+cmtConfig+'/ROOT/v4.02.00/root'
 glastExt=glastRoot+'/ground/GLAST_EXT/'+cmtConfig
 cmtPath='/afs/slac/g/glast/ground/releases/volume07/EngineeringModel-v6r070329p29em1:/afs/slac/g/glast/ground/PipelineConfig/SC/L1Pipeline/builds'

 reportMergeApp=glastRoot+'/ground/PipelineConfig/SC/L1Pipeline/builds/TestReport/v3r6p36/'+cmtConfig+'/MergeHistFiles.exe'

 environ['LD_LIBRARY_PATH']=""
 environ['ROOTSYS']=rootSys
 environ['CMTPATH']=cmtPath

 infilestring=""
 for i_infile in range(len(inFiles)):
  infilestring=infilestring+"-i "+inFiles[i_infile]

 cmd = "source /afs/slac/g/glast/ground/scripts/group.sh; CMTCONFIG="+cmtConfig+"; export CMTCONFIG; GLAST_EXT="+glastExt+"; export GLAST_EXT; cd /afs/slac/g/glast/ground/PipelineConfig/SC/L1Pipeline/builds/TestReport/v3r6p36/cmt; source setup.sh; LD_LIBRARY_PATH=$LD_LIBRARY_PATH:"+glastExt+"/xerces/2.6.0/lib; export LD_LIBRARY_PATH; "+reportMergeApp+" "+infilestring+" -o "+outFile+" -c $L1ProcROOT/merge.txt"

else:

 cmd = config.hadd+" "+environ['outFile']+" "+environ['inFiles']

#cmd = config.hadd + (' %s' % outFile) + ((' %s' * len(inFiles)) % tuple(inFiles))

status = runner.run(cmd)

staged.finish()

sys.exit(status)
