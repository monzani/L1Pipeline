#!/sdf/data/fermi/a/isoc/flightOps/rhel6_gcc44/ISOC_PROD/bin/shisoc --add-env=oracle11 python2.6

import os
import sys

import config

import GPLinit

import fileNames
import pipeline
import registerPrep
import runner
import stageFiles

status = 0

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

realDigiFile = fileNames.fileName('digi', dlId, runId)
stagedDigiFile = staged.stageIn(realDigiFile)

realGapFile = fileNames.fileName('digiGap', dlId, runId, next=True)
stagedGapFile = staged.stageOut(realGapFile)

workDir = os.path.dirname(stagedDigiFile)
l1Setup = config.l1Setup
instDir = config.L1Build
glastExt = config.glastExt
app = config.apps['findGaps']

cmd = '''
cd %(workDir)s
export INST_DIR=%(instDir)s 
export GLAST_EXT=%(glastExt)s
source %(l1Setup)s
%(app)s -d %(stagedDigiFile)s -g %(stagedGapFile)s
''' % locals()

status |= runner.run(cmd)
if status: finishOption = 'wipe'

registerPrep.prep('digiGap', realGapFile)

status |= staged.finish(finishOption)

sys.exit(status)
