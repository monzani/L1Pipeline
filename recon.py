#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Reconstruct a crumb.

Really most everything has already been set up at this point. This is just
here to handle staging and set JOBOPTIONS.

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
crumbId = os.environ['CRUMB_ID']

staged = stageFiles.StageSet()
finishOption = config.finishOption

realDigiFile = fileNames.fileName('digi', dlId, runId, chunkId, crumbId)
os.environ['digiChunkFile'] = staged.stageIn(realDigiFile)
realFT2Fake = fileNames.fileName('ft2Fake', dlId)
os.environ['fakeFT2File'] = staged.stageIn(realFT2Fake)

realReconFile = fileNames.fileName('recon', dlId, runId, chunkId, crumbId)
stagedReconFile = staged.stageOut(realReconFile)
os.environ['reconCrumbFile'] = stagedReconFile
realMeritFile = fileNames.fileName('merit', dlId, runId, chunkId, crumbId)
os.environ['meritCrumbFile'] = staged.stageOut(realMeritFile)
realCalFile = fileNames.fileName('cal', dlId, runId, chunkId, crumbId)
os.environ['calCrumbFile'] = staged.stageOut(realCalFile)
realGcrFile = fileNames.fileName('gcr', dlId, runId, chunkId, crumbId)
os.environ['gcrCrumbFile'] = staged.stageOut(realGcrFile)

workDir = os.path.dirname(stagedReconFile)

datasource = os.environ['DATASOURCE']
if datasource == 'LPA':
    geometry = 'latAssembly/latAssemblySegVols.xml'
elif datasource == 'MC':
    geometry = 'flight/flightSegVols.xml'
    pass
os.environ['gleamGeometry'] = geometry

#setupScript = config.cmtScript
app = config.apps['recon']
options = config.reconOptions[datasource]

cmd = '''
cd %(workDir)s
%(app)s %(options)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
