#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Make SVAC tuple.

@author W. Focke <focke@slac.stanford.edu>
"""
from os import environ
import os

import sys

import GPLinit

import fileNames
import runner
import stageFiles

import config


files = fileNames.setup(environ['DOWNLINK_ID'], environ['RUNID'], \
                        environ['CHUNK_ID'])

staged = stageFiles.StageSet()
finishOption = config.finishOption

stagedDigiFile = staged.stageIn(files['chunk']['digi'])
stagedReconFile = staged.stageIn(files['chunk']['recon'])

stagedOutFile = staged.stageOut(files['chunk']['svac'])
stagedHistFile = staged.stageOut(files['chunk']['svacHist'])

outDir = files['dirs']['chunk']

if staged.setupOK:
    workDir = staged.stageDir
else:
    workDir = outDir
    pass

# make an empty file to use as dummy MC
mcFile = os.path.join(workDir, 'emptyFile')
open(mcFile, 'w').close()

# contents of JO file
options = \
"""%(mcFile)s
%(stagedDigiFile)s
%(stagedReconFile)s
%(stagedOutFile)s
%(stagedHistFile)s
""" \
% locals()

# write JO file
optionFile = os.path.join(workDir, 'jobOptions.txt')
open(optionFile, 'w').write(options)

# do the work
svacTupleApp = config.apps['svacTuple']
svacTupleCmt = config.packages['EngineeringModelRoot']['setup']

cmd = """
cd %(workDir)s
source %(svacTupleCmt)s
%(svacTupleApp)s %(optionFile)s
""" % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
