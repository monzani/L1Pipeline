#!/usr/bin/env python

"""@brief Merge results of chunk or crumb processing.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
from os import environ
import shutil
import string
import sys

import runner

import config

import fileNames
import pipeline
import stageFiles
import rootFiles

def finalize(status):
    staged.finish()
    templist=realOutFile.split('/')
    outFileName=templist[len(templist)-1]
    logipath='/L1Proc/'+fileType+'/'+outFileName
    # print "logipath=",logipath,"filepath=",outFile
    pipeline.setVariable('REGISTER_LOGIPATH', logipath)
    pipeline.setVariable('REGISTER_FILEPATH', realOutFile)
    sys.exit(status)

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
realOutFile = files[mergeLevel][fileType]

inFiles = [staged.stageIn(iFile) for iFile in realInFiles]

for i_infile in range(len(inFiles)):
    print >> sys.stderr, "Infile ", i_infile, " is ", inFiles[i_infile], " and realInFile is ", realInFiles[i_infile]

if len(realInFiles) == 1:
    # We're "merging" 1 file.  So it's just a copy.
    # 
    # Stage the input, but not the output.  This might seems wasteful
    # relative to copying the unstaged input to the unstaged output,
    # but they're probably on the same fiesystem, and this reduces the
    # load on the file server in that case.
    print >> sys.stderr, 'Single input file, copying %s to %s' % \
          (inFiles[0], realOutFile)
    shutil.copyfile(inFiles[0], realOutFile)
    finalize(0)
    pass

outFile = staged.stageOut(realOutFile)


if fileType in ['digiMon', 'reconMon']:
    environ['LD_LIBRARY_PATH'] = ""
    environ['CMTPATH'] = config.cmtPath
    inFileString = ''.join([' -i %s ' % ff for ff in inFiles])
    cmd = "source " + config.glastSetup + " ;  source " + config.packages['TestReport']['setup'] + "  ; LD_LIBRARY_PATH=$LD_LIBRARY_PATH:" + config.glastExt + "/xerces/2.6.0/lib:" + config.glastLocation + "/lib:" + config.rootSys + "/lib ; export LD_LIBRARY_PATH ; " + config.apps['reportMerge'] + " " + inFileString + " -o " + outFile + " -c $L1ProcROOT/merge.txt" + " ; chgrp -R glast-pipeline " + config.L1Disk


elif fileType in ['digi', 'recon']:
    treeName = string.capitalize(fileType)
    rootFiles.concatenate_prune(outFile, inFiles, treeName)
    cmd = ''

else:
    environ['LD_LIBRARY_PATH'] = config.haddRootSys+"/lib:"+environ['LD_LIBRARY_PATH']
    environ['ROOTSYS'] = config.haddRootSys
    cmd = config.hadd + (' %s' % outFile) + ((' %s' * len(inFiles)) % tuple(inFiles)) + " ;chgrp -R glast-pipeline " + config.L1Disk


    pass

status = runner.run(cmd)

finalize(status)
