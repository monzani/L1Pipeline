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


files = fileNames.setup(environ['DOWNLINK_ID'], environ['RUNID'], \
                        environ['CHUNK_ID'])

staged = stageFiles.StageSet()

stagedDigiFile = staged.stageIn(files['chunk']['digi'])
nameBase = files['chunk']['head']

if env['reportType'] == 'recon':
    stagedReconFile = staged.stageIn(files['chunk']['recon'])
    outDir = files['dirs']['reconMon']
    stagedOutFile = files['chunk']['reconMon']
else:
    stagedReconFile = 'noSuchFile'
    outDir = files['dirs']['digiMon']
    stagedOutFile = files['chunk']['digiMon']
    pass


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
