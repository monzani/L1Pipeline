#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Make monitoring histograms.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

import config

import GPLinit

import fileNames
#import pipeline
import registerPrep
import runner
import stageFiles

dlId = os.environ['DOWNLINK_ID']
runId = os.environ['RUNID']
chunkId = os.environ.get('CHUNK_ID') # might not be set

if chunkId is None:
    level = 'run'
else:
    level = 'chunk'
    pass

files = fileNames.setup(dlId, runId, chunkId)

staged = stageFiles.StageSet()
finishOption = config.finishOption

if staged.setupOK:
    workDir = staged.stageDir
else:
    workDir = files['dirs']['run']
    pass

reportType = os.environ['reportType']

options = config.monitorOptions[reportType]
fileType = config.monitorOutFiles[reportType]

realDigiFile = files[level]['digi']
realOutFile = files[level][reportType]

package = config.packages['Monitor']
setup = package['setup']
app = package['app']

digiFile = staged.stageIn(realDigiFile)
outFile = staged.stageOut(realOutFile)

if 'recon' in reportType:
    realReconFile = files[level]['recon']
    stagedReconFile = staged.stageIn(realReconFile)
    realCalFile = files[level]['cal']
    stagedCalFile = staged.stageIn(realCalFile)
    recon = '-r %s -a %s' % (stagedReconFile, stagedCalFile)
else:
    recon = ''
    pass

tdBin = config.tdBin

codeDir = config.packages['Monitor']['bin']

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
%(app)s -b %(tdBin)s -c %(options)s -d %(digiFile)s %(recon)s -o %(tmpHead)s -g %(htmlHead)s -w %(codeDir)s -p %(mcOpt)s || exit 1
mv %(tmpOut)s %(outFile)s
""" % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

if 'Trend' in reportType:
    # This is a trending report, at run level.  Has to be registered.
    registerPrep.prep(fileType, realOutFile)
    pass

sys.exit(status)
