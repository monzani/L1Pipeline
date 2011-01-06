#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc --add-env=oracle11 python2.5

import os
import sys

import config

import GPLinit

import acqQuery
import pipeline

status = 0

runId = os.environ['RUNID']

runNumber = int(runId.lstrip('r0'))

tStart = os.environ['tStart']
tStop = os.environ['tStop']
mootKey = os.environ['mootKey']
mootAlias = os.environ['mootAlias']

pipeline.setVariable('tStart', tStart)
pipeline.setVariable('tStop', tStop)
pipeline.setVariable('mootKey', mootKey)
pipeline.setVariable('mootAlias', mootAlias)

sys.exit(status)
