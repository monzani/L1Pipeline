#!/usr/bin/env python

"""@brief Merge results of chunk or crumb processing.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
from os import environ

import re
import sys

import runner

import config

import fileNames
import stageFiles
import pipeline

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

 environ['LD_LIBRARY_PATH']=""
 environ['ROOTSYS']=config.rootSys
 environ['CMTPATH']=config.cmtPath

 infilestring=""
 for i_infile in range(len(inFiles)):
  print "Infile",i_infile,"is",inFiles[i_infile]
  infilestring=infilestring+"-i "+inFiles[i_infile]

 print "infilestring=",infilestring

 cmd = "source /afs/slac/g/glast/ground/scripts/group.sh; CMTCONFIG="+config.cmtConfig+"; export CMTCONFIG; GLAST_EXT="+config.glastExt+"; export GLAST_EXT; cd "+config.testReportDir+"/cmt; source setup.sh; LD_LIBRARY_PATH=$LD_LIBRARY_PATH:"+config.glastExt+"/xerces/2.6.0/lib; export LD_LIBRARY_PATH; "+config.reportMergeApp+" "+infilestring+" -o "+outFile+" -c $L1ProcROOT/merge.txt"

else:

# cmd = config.hadd+" "+environ['outFile']+" "+environ['inFiles']

 environ['LD_LIBRARY_PATH']=config.haddRootSys+"/lib:"+environ['LD_LIBRARY_PATH']
 environ['ROOTSYS']=config.haddRootSys
 cmd = config.hadd + (' %s' % outFile) + ((' %s' * len(inFiles)) % tuple(inFiles))


status = runner.run(cmd)

staged.finish()

templist=realOutFile.split('/')
outFileName=templist[len(templist)-1]
logipath='/L1Proc/'+fileType+'/'+outFileName
print "logipath=",logipath,"filepath=",outFile
pipeline.setVariable('REGISTER_LOGIPATH', logipath)
pipeline.setVariable('REGISTER_FILEPATH', realOutFile)

sys.exit(status)
