#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Make monitoring histograms.

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
chunkId = os.environ.get('CHUNK_ID') # might not be set

if chunkId is None:
    level = 'run'
else:
    level = 'chunk'
    pass

staged = stageFiles.StageSet()
finishOption = config.finishOption

reportType = os.environ['reportType']

options = config.monitorOptions[reportType]

realDigiFile = fileNames.fileName('digi', dlId, runId, chunkId)
realOutFile = fileNames.fileName(reportType, dlId, runId, chunkId)

package = config.packages['Monitor']
setup = package['setup']
app = package['app']

digiFile = staged.stageIn(realDigiFile)
outFile = staged.stageOut(realOutFile)

workDir = os.path.dirname(outFile)

if 'recon' in reportType:
    realReconFile = fileNames.fileName('recon', dlId, runId, chunkId)
    stagedReconFile = staged.stageIn(realReconFile)
    realCalFile = fileNames.fileName('cal', dlId, runId, chunkId)
    stagedCalFile = staged.stageIn(realCalFile)
    recon = '-r %s -a %s' % (stagedReconFile, stagedCalFile)
else:
    recon = ''
    pass

tdBin = config.tdBin[reportType]

codeDir = config.packages['Monitor']['bin']

if reportType in ['calEor', 'calTrend']:
    zOpt = '' # keep transient data in a temp file
else:
    zOpt = '-z' # keep transient data in memory
    pass

datasource = os.environ['DATASOURCE']
if datasource == 'MC':
    mcOpt = '-t MCOktTest'
else:
    mcOpt = ''
    pass

# CHANGE THIS!
tmpHead = 'temp'
tmpOut = tmpHead + '_time.root'
htmlHead = 'html'

cmd = """cd %(workDir)s
source %(setup)s
%(app)s %(zOpt)s -b %(tdBin)s -c %(options)s -d %(digiFile)s %(recon)s -o %(tmpHead)s -g %(htmlHead)s -w %(codeDir)s -p %(mcOpt)s || exit 1
mv %(tmpOut)s %(outFile)s
""" % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
