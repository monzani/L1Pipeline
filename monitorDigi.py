#!/usr/bin/env python

"""@brief Make monitoring histograms for a digi chunk.

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
env['digiMonChunkFile'] = staged.stageOut(env['digiMonChunkFile'])

#env['JOBOPTIONS'] = config.reconOptions

status = runner.run(config.digiMonApp)

staged.finish()

sys.exit(status)
