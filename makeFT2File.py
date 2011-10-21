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

fileType = 'ft2'

app = config.apps['mergeFT2']

# input
ft2SecondsFile = fileNames.fileName('ft2Seconds', dlId, runId)
stagedFt2SecondsFile = staged.stageIn(ft2SecondsFile)

# output
fitsFt2File = fileNames.fileName(fileType, dlId, runId, next=True)
stagedFt2FitsFile = staged.stageOut(fitsFt2File)

workDir = os.path.dirname(stagedFt2FitsFile)
l1Setup = config.l1Setup
instDir = config.L1Build
glastExt = config.glastExt
            
version = fileNames.version(fitsFt2File)

template = config.ft2Template
templOpt = '-new_tpl %s' % template

cmd = '''
cd %(workDir)s
export INST_DIR=%(instDir)s 
export GLAST_EXT=%(glastExt)s
source %(l1Setup)s
%(app)s -FT2_fits_File %(stagedFt2SecondsFile)s -FT2_fits_merged_File %(stagedFt2FitsFile)s -Version %(version)s %(templOpt)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if not status: registerPrep.prep(fileType, fitsFt2File)

sys.exit(status)
