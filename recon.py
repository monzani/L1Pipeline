#!/usr/bin/env python

"""@brief Reconstruct a crumb.

Really most everything has already been set up at this point. This is just
here to handle staging and set JOBOPTIONS.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
env = os.environ
import sys

import runner
import stageFiles

import config


staged = stageFiles.StageSet()

env['digiChunkFile'] = staged.stageIn(env['digiChunkFile'])
env['reconCrumbFile'] = staged.stageOut(env['reconCrumbFile'])

env['JOBOPTIONS'] = config.reconOptions

status = runner.run(config.reconApp)

staged.finish()

sys.exit(status)
