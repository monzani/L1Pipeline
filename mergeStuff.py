#!/usr/bin/env python

"""@brief Merge results of chunk or crumb processing.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
import os
env = os.environ
import re
import sys

#import runner

import config

import fileNames
import stageFiles

staged = stageFiles.StageSet()

dlId = env['DOWNLINK_ID']
fileType = env['fileType']
chunkId = os.environ.get('CHUNK_ID')

if chunkId is None:
    mergeLevel = 'run'
else:
    mergeLevel = 'chunk'
    pass

files = fileNames.setup(dlId, runId, chunkId)

realInFiles = fileNames.findPieces(fileType, dlId, runId, chunkId)
inFiles = [staged.stageIn(iFile) for iFile in realInFiles]

realOutFile = files[fileType][mergeLevel]
outFile = staged.stageOut(realOutFile)

##wbf## os.system(config.hadd+" "+env['outFile']+" "+env['inFiles'])
cmd = config.hadd+" "+env['outFile']+" "+env['inFiles']
#cmd = config.hadd + (' %s' % outFile) + ((' %s' * len(inFiles)) % tuple(inFiles))

status = runner.run(cmd)

staged.finish()

sys.exit(status)
