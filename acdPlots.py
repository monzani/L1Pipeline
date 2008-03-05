#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import sys
import os

import config

import fileNames
import stageFiles

status = 0

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

staged = stageFiles.StagedSet()

realInFile = fileNames.fileName('digiEor', dlId, runId)
stagedInFile = staged.stageIn(realInFile)

app = config.apps['acdPlots']

cmd = '%(app)s -i %(stagedInFile)s' % locals()

status |= runner.run(cmd)

sys.exit(status)
