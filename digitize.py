#!/usr/bin/env python

from os import system, environ
import sys

#from os import environ as env
#from os import path

#env['GLAST_EXT']='/afs/slac/g/glast/ground/GLAST_EXT/rh9_gcc32opt'
#env['L1ProcROOT']='/nfs/farm/g/glast/u33/wai/pipeline_tests'
#env['LATCalibRoot']='/afs/slac/g/glast/ground/releases/calibrations'
#env['EVTFILE']='/nfs/farm/g/glast/u35/MC-tasks/SC1-Level0-test/ldf/CCSDS/000000001.evt'
#env['digiChunkFile']='larry_digi.root'

import config
import fileNames
import runner
import stageFiles

files = fileNames.setup(environ['DOWNLINK_ID'], environ['RUNID'], \
                        environ['CHUNK_ID'])

#env['digiChunkFile'] = staged.stageIn(files['chunk']['digiChunk'])

#env['JOBOPTIONS']=config.digiOptions

#env['JOBOPTIONS']='/afs/slac/u/ek/wai/pipeline_tests/ldf2digi.txt'

##wbf## system("mkdir "+environ['TestDir']+"/"+environ['CHUNK_ID']+";"+config.digiApp+' '+environ['Larry_L1ProcROOT']+'/digi.jobOpt;chgrp -R glast-pipeline '+environ['TestDir']+'/'+environ['CHUNK_ID'])

cmd = "mkdir "+environ['TestDir']+"/"+environ['CHUNK_ID']+";"+config.digiApp+' '+environ['Larry_L1ProcROOT']+'/digi.jobOpt;chgrp -R glast-pipeline '+environ['TestDir']+'/'+environ['CHUNK_ID']

status = runner.run(cmd)
sys.exit(status)
