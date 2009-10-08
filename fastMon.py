#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import re
import sys

import config

import GPLinit

import fileNames
import pipeline
import runner
import stageFiles

status = 0

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']
chunkId = os.environ['CHUNK_ID']

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

package = config.packages['FastMon']

reportType = os.environ['reportType']
if reportType == 'fastMonTuple':
    realInFile = os.environ['EVTFILE']
    realErrorFile = fileNames.fileName('fastMonError', dlId, runId, chunkId)
    errorFile = staged.stageOut(realErrorFile)
    realM7File = os.path.join(os.environ['DOWNLINK_RAWDIR'], 'magic7_%s.txt' % dlId) 
    m7File = staged.stageIn(realM7File)
    realTupleFile = fileNames.fileName('fastMonTuple', dlId, runId, chunkId)
    tupleFile = staged.stageOut(realTupleFile)
    saaDef = package['saaDefinition']
    varArgs = '-o %(tupleFile)s -e %(errorFile)s -m %(m7File)s -s %(saaDef)s' % locals()
    app = config.apps['fastMonTuple']
    workDir = os.path.dirname(errorFile)
elif reportType == 'fastMonHist':
    realInFile = fileNames.fileName('fastMonTuple', dlId, runId, chunkId)
    realHistFile = fileNames.fileName('fastMonHist', dlId, runId, chunkId)
    histFile = staged.stageOut(realHistFile)
    varArgs = '-o %(histFile)s' % locals()
    app = config.apps['fastMonHist']
    workDir = os.path.dirname(histFile)
    pass

inFile = staged.stageIn(realInFile)

os.environ.update(package['env'])

dmRoot = config.L1Cmt

extra = package['extraSetup']
setup = package['setup']

dataSource = os.environ['DATASOURCE']
if dataSource in ['LCI']:
    optionTag = 'fastMonLci'
elif dataSource in ['LPA', 'MC']:
    optionTag = 'fastMon'
else:
    print >> sys.stderr, 'Bad DATASOURCE %s' % dataSource
    status = 1
    pass
configFile = config.monitorOptions[optionTag]

python = config.python

cmd = '''
cd %(workDir)s
export DATAMONITORING_ROOT=%(dmRoot)s
export FAST_MON_DIR=%(workDir)s
%(extra)s
source %(setup)s
export PYTHONPATH=${PYTHONPATH}:%(workDir)s
%(python)s %(app)s -c %(configFile)s %(varArgs)s %(inFile)s
''' % locals()

if not status: status |= runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
