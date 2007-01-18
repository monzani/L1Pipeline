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
env['reconChunkFile'] = staged.stageOut(env['reconChunkFile'])
env['reconMonChunkFile'] = staged.stageOut(env['reconMonChunkFile'])

#env['JOBOPTIONS'] = config.reconOptions

status = runner.run(config.reconMonApp)

staged.finish()

sys.exit(status)
