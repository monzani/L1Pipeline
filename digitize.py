#!/usr/bin/env python

from os import system, environ
import sys

import config
import fileNames
import runner
import stageFiles

files = fileNames.setup(environ['DOWNLINK_ID'], environ['RUNID'], \
                        environ['CHUNK_ID'])

staged = stageFiles.StageSet()
environ['EVTFILE'] = staged.stageIn(environ['EVTFILE'])
environ['digiChunkFile'] = staged.stageOut(files['chunk']['digi'])

status = runner.run(config.apps['digi']+' '+config.digiOptions)

staged.finish()

sys.exit(status)
