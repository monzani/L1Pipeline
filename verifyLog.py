#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import fileNames
import registerPrep

status = 0

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

realVerifyLogFile = fileNames.fileName('verifyLog', dlId, runId, next=False)
registerPrep.prep('verifyLog', realVerifyLogFile)

sys.exit(status)
