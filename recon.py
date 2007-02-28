#!/usr/bin/env python

"""@brief Reconstruct a crumb.

Really most everything has already been set up at this point. This is just
here to handle staging and set JOBOPTIONS.

@author W. Focke <focke@slac.stanford.edu>
"""

from os import system, environ
import sys

import config
import fileNames
import runner
import stageFiles

##wbf## system(config.reconApp+' '+environ['Larry_L1ProcROOT']+'/recon.jobOpt; chgrp -R glast-pipeline '+environ['TestDir']+'/'+environ['CHUNK_ID'])

files = fileNames.setup(environ['DOWNLINK_ID'], environ['RUNID'], \
                        environ['CHUNK_ID'], environ['CRUMB_ID'])

#staged = stageFiles.StageSet()

#env['digiChunkFile'] = staged.stageIn(files['chunk']['digiChunk'])
#env['reconCrumbFile'] = staged.stageOut(files['crumb']['reconCrumb'])

#env['JOBOPTIONS'] = config.reconOptions

status = runner.run(config.reconApp+' '+config.reconOptions)

#staged.finish()

sys.exit(status)
