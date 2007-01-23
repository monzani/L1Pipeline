#!/usr/bin/env python

from os import system, environ
#from os import environ as env
#from os import path

#env['GLAST_EXT']='/afs/slac/g/glast/ground/GLAST_EXT/rh9_gcc32opt'
#env['L1ProcROOT']='/nfs/farm/g/glast/u33/wai/pipeline_tests'
#env['LATCalibRoot']='/afs/slac/g/glast/ground/releases/calibrations'
#env['EVTFILE']='/nfs/farm/g/glast/u35/MC-tasks/SC1-Level0-test/ldf/CCSDS/000000001.evt'
#env['digiChunkFile']='larry_digi.root'

import config

#env['JOBOPTIONS']=config.digiOptions

#env['JOBOPTIONS']='/afs/slac/u/ek/wai/pipeline_tests/ldf2digi.txt'

system("mkdir "+environ['TestDir']+"/"+environ['RUN_ID']+";"+config.digiApp+' '+environ['L1ProcROOT']+'/digi.jobOpt;chgrp -R glast-pipeline '+environ['TestDir']+'/'+environ['RUN_ID'])
