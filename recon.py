#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Reconstruct a crumb.

Really most everything has already been set up at this point. This is just
here to handle staging and set JOBOPTIONS.

@author W. Focke <focke@slac.stanford.edu>
"""

from os import system, environ
import sys

import GPLinit

import config
import fileNames
import runner
import stageFiles

##wbf## system(config.reconApp+' '+environ['Larry_L1ProcROOT']+'/recon.jobOpt; chgrp -R glast-pipeline '+environ['TestDir']+'/'+environ['CHUNK_ID'])

files = fileNames.setup(environ['DOWNLINK_ID'], environ['RUNID'], \
                        environ['CHUNK_ID'], environ['CRUMB_ID'])

staged = stageFiles.StageSet()

environ['digiChunkFile'] = staged.stageIn(files['chunk']['digi'])
environ['reconCrumbFile'] = staged.stageOut(files['crumb']['recon'])
environ['meritCrumbFile'] = staged.stageOut(files['crumb']['merit'])
environ['calCrumbFile'] = staged.stageOut(files['crumb']['cal'])

#environ['JOBOPTIONS'] = config.reconOptions

status = runner.run(config.apps['recon'] + ' ' + config.reconOptions)

status |= staged.finish()

sys.exit(status)
