#!/usr/bin/env python

"""@brief Make SVAC tuple.

@author W. Focke <focke@slac.stanford.edu>
"""
from os import environ
import os

import sys

import fileNames
import runner
import stageFiles

import config


files = fileNames.setup(environ['DOWNLINK_ID'], environ['RUNID'], \
                        environ['CHUNK_ID'])

staged = stageFiles.StageSet()

stagedDigiFile = staged.stageIn(files['chunk']['digi'])
stagedReconFile = staged.stageIn(files['chunk']['recon'])

stagedOutFile = staged.stageOut(files['chunk']['svac'])
stagedHistFile = staged.stageOut(files['chunk']['svacHist'])

outDir = files['dirs']['chunk']

# make an empty file to use as dummy MC
mcFile = os.path.join(outDir, 'emptyFile')
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
optionFile = os.path.join(outDir, 'jobOptions.txt')
open(optionFile, 'w').write(options)

# do the work
svacTupleApp = config.svacTupleApp
svacTupleCmt = config.svacTupleCmt
cmd = 'cd %(outDir)s ; printenv ; source %(svacTupleCmt)s ; printenv LD_LIBRARY_PATH ; %(svacTupleApp)s %(optionFile)s' % locals()
status = runner.run(cmd)

staged.finish()

sys.exit(status)
