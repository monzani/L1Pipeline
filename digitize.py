#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import GPLinit

import fileNames
import runner
import stageFiles

dlId = os.environ['DOWNLINK_ID']
runId = os.environ['RUNID']
chunkId = os.environ['CHUNK_ID']
files = fileNames.setup(dlId, runId, chunkId)

staged = stageFiles.StageSet()
finishOption = config.finishOption

os.environ['EVTFILE'] = staged.stageIn(os.environ['EVTFILE'])
os.environ['digiChunkFile'] = staged.stageOut(files['chunk']['digi'])

status = runner.run(config.apps['digi']+' '+config.digiOptions)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
