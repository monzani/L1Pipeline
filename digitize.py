#!/usr/bin/env python

from os import system, environ
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
environ['EVTFILE'] = staged.stageIn(environ['EVTFILE'])
environ['digiChunkFile'] = staged.stageOut(files['chunk']['digi'])

status = runner.run(config.apps['digi']+' '+config.digiOptions)

staged.finish()

sys.exit(status)
