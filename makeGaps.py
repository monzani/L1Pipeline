#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc --add-env=oracle11 python2.5

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

package = config.packages['findGaps']
setup = package['setup']

app = config.apps['findGaps']

cmd = '''
cd %(workDir)s
source %(setup)s
%(app)s -d %(stagedDigiFile)s -g %(stagedGapFile)s
''' % locals()

status |= runner.run(cmd)
if status: finishOption = 'wipe'

registerPrep.prep('digiGap', realGapFile)

status |= staged.finish(finishOption)

sys.exit(status)
