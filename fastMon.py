#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import GPLinit

import fileNames
import runner
import stageFiles


dlId = os.environ['DOWNLINK_ID']
runId = os.environ['RUNID']
chunkId = os.environ['CHUNK_ID']
files = fileNames.setup(dlId, runId, chunkId)
realInFile = files['chunk']['event']
realErrorFile = files['chunk']['fastMonError']
realHistFile = files['chunk']['fastMonHist']
realTupleFile = files['chunk']['fastMonTuple']

staged = stageFiles.StageSet()
finishOption = config.finishOption

inFile = staged.stageIn(realInFile)
errorFile = staged.stageOut(realErrorFile)
histFile = staged.stageOut(realHistFile)
tupleFile = staged.stageOut(realTupleFile)

if staged.setupOK:
    workDir = staged.stageDir
else:
    workDir = files['chunk']['dirs']['fastMon']
    pass

package = config.packages['FastMon']
os.environ.update(package['env'])

dmRoot = config.L1Cmt

extra = package['extraSetup']
setup = package['setup']
app = config.apps['fastMon']

newLatexDir = config.installBin

cmd = '''
cd %(workDir)s
export DATAMONITORING_ROOT=%(dmRoot)s
export FAST_MON_DIR=%(workDir)s
%(extra)s
source %(setup)s
export PYTHONPATH=${PYTHONPATH}:%(workDir)s
%(app)s -o %(tupleFile)s -p %(histFile)s -e %(errorFile)s %(inFile)s
ls -lahR
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
