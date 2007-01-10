#!/usr/bin/env python

"""@brief Reconstruct a crumb.

Really most everything has already been set up at this point, this is just
here to handle staging.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
env = os.environ
import sys

import stageFiles

import config


staged = stageFiles.StageSet()

env['digiChunkFile'] = staged.stageIn(env['digiChunkFile'])
env['reconCrumbFile'] = staged.stageOut(env['reconCrumbFile'])

env['JOBOPTIONS'] = config.reconOptions

status = os.system(config.reconApp)

staged.finish()
