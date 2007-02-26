#!/usr/bin/env python

from os import system, environ
import sys

import config
import fileNames
import runner
import stageFiles

files = fileNames.setup(environ['DOWNLINK_ID'], environ['RUNID'], \
                        environ['CHUNK_ID'])

staged = stageFiles.stageSet()
env['EVTFILE'] = staged.stageIn(env['EVTFILE'])
env['digiChunkFile'] = staged.stageOut(files['chunk']['digiChunk'])

env['JOBOPTIONS'] = config.digiOptions

#cmd = "mkdir "+environ['TestDir']+"/"+environ['CHUNK_ID']+";"+config.digiApp+' '+environ['Larry_L1ProcROOT']+'/digi.jobOpt;chgrp -R glast-pipeline '+environ['TestDir']+'/'+environ['CHUNK_ID']

status = runner.run(config.digiApp)

staged.finish()

sys.exit(status)
