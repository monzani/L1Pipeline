#!/usr/bin/env python

import os
import sys

import config
import fileNames
import runner
import stageFiles

dlId = os.environ['DOWNLINK_ID']
runId = os.environ['RUNID']
chunkId = os.environ['CHUNK_ID']
files = fileNames.setup(dlId, runId, chunkId)

staged = stageFiles.StageSet()
os.environ['EVTFILE'] = staged.stageIn(os.environ['EVTFILE'])
os.environ['digiChunkFile'] = staged.stageOut(files['chunk']['digi'])

status = runner.run(config.apps['digi']+' '+config.digiOptions)

staged.finish()

sys.exit(status)
