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

#environ['JOBOPTIONS'] = config.digiOptions

#cmd = "mkdir "+environ['TestDir']+"/"+environ['CHUNK_ID']+";"+config.digiApp+' '+environ['Larry_L1ProcROOT']+'/digi.jobOpt;chgrp -R glast-pipeline '+environ['TestDir']+'/'+environ['CHUNK_ID']

status = runner.run(config.digiApp+' '+config.digiOptions)

staged.finish()

sys.exit(status)
