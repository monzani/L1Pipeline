#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import GPLinit

import fileNames
import registerPrep
import runner
import stageFiles

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

# fileType = 'ft2NoQual'
inFileType = os.environ['inFileType']
outFileType = os.environ['outFileType']

app = config.apps['mergeFT2']

# input
ft2SecondsFile = fileNames.fileName(inFileType, dlId, runId)
stagedFt2SecondsFile = staged.stageIn(ft2SecondsFile)

# output
fitsFt2File = fileNames.fileName(outFileType, dlId, runId, next=True)
stagedFt2FitsFile = staged.stageOut(fitsFt2File)

workDir = os.path.dirname(stagedFt2FitsFile)
l1Setup = config.l1Setup
instDir = config.L1Build
glastExt = config.glastExt
            
version = fileNames.version(fitsFt2File)

procVer = config.procVer

cmd = '''
cd %(workDir)s
source %(setupScript)s
export INST_DIR=%(instDir)s 
export GLAST_EXT=%(glastExt)s
source %(l1Setup)s
%(app)s -inputFT2 %(stagedFt2SecondsFile)s -outputFT2 %(stagedFt2FitsFile)s -version %(version)s -procVer %(procVer)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if not status: registerPrep.prep(outFileType, fitsFt2File)

sys.exit(status)
