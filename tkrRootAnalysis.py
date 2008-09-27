#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Do TKR analysis.

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
chunkId = os.environ.get('CHUNK_ID')
crumbId = os.environ.get('CRUMB_ID')

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

realDigiFile = fileNames.fileName('digi', dlId, runId, chunkId, crumbId)
stagedDigiFile = staged.stageIn(realDigiFile)
realReconFile = fileNames.fileName('recon', dlId, runId, chunkId, crumbId)
stagedReconFile = staged.stageIn(realReconFile)

realOutFile = fileNames.fileName('tkrAnalysis', dlId, runId, chunkId, crumbId)
stagedOutFile = staged.stageOut(realOutFile)

workDir = os.path.dirname(stagedOutFile)


# do the work
app = config.apps['tkrAnalysis']
cmtScript = config.packages['calibTkrUtil']['setup']

cmd = """
cd %(workDir)s
source %(cmtScript)s
%(app)s %(stagedDigiFile)s %(stagedReconFile)s %(stagedOutFile)s
""" % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
