#!/usr/bin/env python

"""@brief Make monitoring histograms for a digi chunk.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
env = os.environ
import sys

import fileNames
import runner
import stageFiles

import config


staged = stageFiles.StageSet()

realDigiFile = env['digiChunkFile']
stagedDigiFile = staged.stageIn(realDigiFile)
digiDir = os.path.dirname(realDigiFile)
nameBase = fileNames.baseHead(realDigiFile)

try:
    realReconFile = env['reconChunkFile']
    stagedReconFile = staged.stageIn(realReconFile)
except KeyError:
    stagedReconFile = 'noSuchFile'
    pass

#outDir = os.path.join(inDir, digiMon)
outDir = env['TestDir']
outName = fileNames.join((nameBase, env['PIPELINE_PROCESS'], config.L1Version), 'root')
realOutFile = os.path.join(outDir, outName)
#stagedOutFile = staged.stageOut(realOutFile)
stagedOutFile = realOutFile

glastVersion = config.glastVersion
testReportVersion = config.testReportVersion

tkrCalibSerNo = '-9999'
calCalibSerNo = '-9999'

# contents of JO file
options = \
"""%(stagedDigiFile)s
%(stagedReconFile)s
%(outDir)s
%(nameBase)s
%(testReportVersion)s
%(glastVersion)s
%(tkrCalibSerNo)s
%(calCalibSerNo)s
""" \
% locals()

# write JO file
optionFile = os.path.join(outDir, 'jobOptions.txt')
open(optionFile, 'w').write(options)


# do the work
digiMonApp = config.digiMonApp
digiMonCmt = config.digiMonCmt
cmd = 'cd %(outDir)s ; printenv CMTPATH; source %(digiMonCmt)s ; printenv LD_LIBRARY_PATH; %(digiMonApp)s %(optionFile)s' % locals()
status = runner.run(cmd)

staged.finish()

sys.exit(status)
