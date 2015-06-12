#!/afs/slac/g/glast/isoc/flightOps/rhel6_gcc44/ISOC_PROD/bin/shisoc python2.6

import os
import sys

import pyfits as pf

import config

import GPLinit

import fileNames
import fileOps
import registerPrep
import runner
import stageFiles

status = 0

runId = os.environ['RUNID']
dlId = runId

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

outFileType = os.environ['outFileType']

app = config.apps['mergeFT2']

# input
inputFile = os.environ['inputFT2Seconds']
stagedInputFile = staged.stageIn(inputFile)

# output
ft2SecondsFile = fileNames.fileName(outFileType, dlId, runId, next=True)
stagedFt2SecondsFile = staged.stageOut(ft2SecondsFile)

#l1Setup = config.l1Setup
#instDir = config.L1Build
#glastExt = config.glastExt
            
version = fileNames.version(ft2SecondsFile)
outBase = os.path.basename(stagedFt2SecondsFile)
procVer = config.ft2SecondsProcVer

hduList = pf.open(stagedInputFile)
header = hduList[0].header
header['FILENAME'] = outBase
header['VERSION'] = version
header['PROC_VER'] = procVer
hduList.writeto(stagedFt2SecondsFile)
hduList.close()

workDir = os.path.dirname(stagedFt2SecondsFile)

sumCmd = """HOME=%s
source %s
fchecksum infile=%s update=yes datasum=yes""" % \
(workDir, config.astroTools, stagedFt2SecondsFile)
status |= runner.run(sumCmd)

status |= staged.finish(finishOption)

if not status: registerPrep.prep(outFileType, ft2SecondsFile)

sys.exit(status)
