#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

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

realInFile = os.environ['EVTFILE']
realM7File = os.path.join(os.environ['DOWNLINK_RAWDIR'], 'magic7_%s.txt' % dlId)
realErrorFile = fileNames.fileName('fastMonError', dlId, runId, chunkId)
realHistFile = fileNames.fileName('fastMonHist', dlId, runId, chunkId)
realTupleFile = fileNames.fileName('fastMonTuple', dlId, runId, chunkId)

staged = stageFiles.StageSet()
finishOption = config.finishOption

inFile = staged.stageIn(realInFile)
m7File = staged.stageIn(realM7File)
errorFile = staged.stageOut(realErrorFile)
histFile = staged.stageOut(realHistFile)
tupleFile = staged.stageOut(realTupleFile)

workDir = os.path.dirname(errorFile)

package = config.packages['FastMon']
os.environ.update(package['env'])

dmRoot = config.L1Cmt

extra = package['extraSetup']
setup = package['setup']
app = config.apps['fastMon']

python = config.python

cmd = '''
cd %(workDir)s
export DATAMONITORING_ROOT=%(dmRoot)s
export FAST_MON_DIR=%(workDir)s
%(extra)s
source %(setup)s
export PYTHONPATH=${PYTHONPATH}:%(workDir)s
%(python)s %(app)s -o %(tupleFile)s -p %(histFile)s -e %(errorFile)s -m %(m7File)s %(inFile)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
