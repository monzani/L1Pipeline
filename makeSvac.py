#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Make SVAC tuple.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

import config

import GPLinit

import fileNames
import runner
import stageFiles


head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']
chunkId = os.environ['CHUNK_ID']
crumbId = os.environ.get('CRUMB_ID')

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

realDigiFile = fileNames.fileName('digi', dlId, runId, chunkId, crumbId)
stagedDigiFile = staged.stageIn(realDigiFile)
realReconFile = fileNames.fileName('recon', dlId, runId, chunkId, crumbId)
stagedReconFile = staged.stageIn(realReconFile)

realSvacFile = fileNames.fileName('svac', dlId, runId, chunkId, crumbId)
stagedSvacFile = staged.stageOut(realSvacFile)

workDir = os.path.dirname(stagedSvacFile)

realHistFile = fileNames.fileName('svacHist', dlId, runId, chunkId, crumbId)
#stagedHistFile = staged.stageOut(realHistFile) # don't want to keep this
stagedHistFile = os.path.join(workDir, os.path.basename(realHistFile))

# make an empty file to use as dummy MC
mcFile = os.path.join(workDir, 'emptyFile')
open(mcFile, 'w').close()

# contents of JO file
options = \
"""%(mcFile)s
%(stagedDigiFile)s
%(stagedReconFile)s
%(stagedSvacFile)s
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
