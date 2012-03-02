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

tStart, tStop = acqQuery.runTimes(runNumber)
pipeline.setVariable('tStart', '%.17g' % tStart)
pipeline.setVariable('tStop', '%.17g' % tStop)

mootKey, mootAlias = acqQuery.query([runNumber], ['moot_key', 'moot_alias'])[runNumber]
pipeline.setVariable('mootKey', mootKey)
pipeline.setVariable('mootAlias', mootAlias)

sys.exit(status)
