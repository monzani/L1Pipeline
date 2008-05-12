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

package = config.packages['Monitor']
setup = package['setup']
app = package['app']

realOutFile = fileNames.fileName(reportType, dlId, runId, chunkId)
outFile = staged.stageOut(realOutFile)

workDir = os.path.dirname(outFile)

if 'fastMon' in reportType:
    realFmt = fileNames.fileName('fastMonTuple', dlId, runId, chunkId)
    stagedFmt = staged.stageIn(realFmt)
    inFileOpts = '-f %s' % stagedFmt
else:
    realDigiFile = fileNames.fileName('digi', dlId, runId, chunkId)
    stagedDigiFile = staged.stageIn(realDigiFile)
    inFileOpts = '-d %s' % stagedDigiFile
    if 'recon' in reportType:
        realReconFile = fileNames.fileName('recon', dlId, runId, chunkId)
        stagedReconFile = staged.stageIn(realReconFile)
        realCalFile = fileNames.fileName('cal', dlId, runId, chunkId)
        stagedCalFile = staged.stageIn(realCalFile)
        inFileOpts += ' -r %s -a %s' % (stagedReconFile, stagedCalFile)
    elif 'merit' in reportType:
        realMeritFile = fileNames.fileName('merit', dlId, runId, chunkId)
        stagedMeritFile = staged.stageIn(realMeritFile)
        inFileOpts += ' -m %s' % (stagedMeritFile,)
        configFile = config.normalizedRateConfigs[reportType]
        options += ' -e %s' % (configFile)
        pass
    pass

tdBin = config.tdBin[reportType]

codeDir = config.packages['Monitor']['bin']

# if reportType in ['calEor', 'calTrend']:
#     zOpt = '' # keep transient data in a temp file
# else:
#     zOpt = '-z' # keep transient data in memory
#     pass
zOpt = ''

datasource = os.environ['DATASOURCE']
if datasource == 'MC':
    mcOpt = '-t MC'
else:
    mcOpt = ''
    pass

# CHANGE THIS!
tmpHead = 'temp'
tmpOut = tmpHead + '_time.root'
htmlHead = 'html'

cmd = """cd %(workDir)s
source %(setup)s
%(app)s %(zOpt)s -b %(tdBin)s -c %(options)s %(inFileOpts)s -o %(tmpHead)s -g %(htmlHead)s -w %(codeDir)s -p %(mcOpt)s || exit 1
mv %(tmpOut)s %(outFile)s
""" % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
