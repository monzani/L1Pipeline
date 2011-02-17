#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc --add-env=oracle11 python2.5

"""@brief Make sure we are done processing a run/downlink.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys
import time

#import cx_Oracle

import config

import GPLinit

import acqQuery
import fileNames
import l1Logger
import lockFile
import pipeline


def checkRunStatus(runNumber):
    results = acqQuery.query([runNumber], ['STATUS'])

    if len(results) != 1:
        # If the run is not in ACQSUMMARY, something is wrong.
        # If there are multiple entries, something is wrong.
        # In either case, err on the side of caution.
        print >> sys.stderr, "Did not get exactly 1 status for run %s, results=%s; not retiring." % (runNumber, results)
        return False, "WeirdlyBroken"
    print >> sys.stderr, results
    
    runStatus = results[runNumber][0]
    statusFinal = runStatus in ['Complete', 'Incomplete']

    print >> sys.stderr, 'Run %s has status %s, final=%s' % \
          (runNumber, runStatus, statusFinal)

    return statusFinal, runStatus


def checkTokens(head, runId):
    tokenDir = fileNames.tokenDir(head, runId)
    print >> sys.stderr, 'Looking for chunk tokens in %s' % tokenDir
    try:
        tokenFiles = os.listdir(tokenDir)
    except OSError:
        # Probably should not cleanup here if we're in prod mode.
        #
        # Or at least send a message to the log watcher.
        msg = 'Token directory %s is nonexistent or unreadable.' % tokenDir
        print >> sys.stderr, msg
        l1Logger.warn(msg)
        tokenFiles = []
        pass
    if tokenFiles:
        print >> sys.stderr, 'Token files %s remain, not cleaning up.' % tokenFiles
    else:
        print >> sys.stderr, 'Found none.'
        pass
    statusTokens = not tokenFiles
    return statusTokens

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

runNumber = int(os.environ['runNumber'])

rootDir = os.path.dirname(fileNames.fileName('chunkList', dlId, runId)) #bleh

dataSource = os.environ['DATASOURCE']

# Here we need to check that all the chunk locks (created by the halfpipe,
# removed by this script before now) are gone, AND that some database
# somewhere (GLAST_ISOC.ACQSUMMARY) says that the run is as complete as it
# will get, before launching cleanup and updating run status in the data
# catalog.

hpFinal, hpRunStatus = checkRunStatus(runNumber)
tokenStatus = checkTokens(head, runId)
mergeStatus = not fileNames.checkMergeLock(runId)
verifyStatus = not fileNames.checkVerifyLock(runId)
readyToRetire = hpFinal and tokenStatus and mergeStatus

print >> sys.stderr, "hpFinal=%(hpFinal)s, tokenStatus=%(tokenStatus)s, mergeStatus=%(mergeStatus)s, verifyStatus=%(verifyStatus)s" % locals()

if readyToRetire and verifyStatus:
    print >> sys.stderr, "Run %s is as done as it's going to get, retiring." % runId
    subTask = config.cleanupSubTask[pipeline.getTask()][dataSource]
    stream = runNumber

    # goodReconPis = os.environ.get('goodReconPis')
    # args = 'goodReconPis=%s' % goodReconPis
    args = ''

    pipeline.createSubStream(subTask, stream, args)
    l1RunStatus = hpRunStatus
else:
    print >> sys.stderr, "Not retiring run %(runId)s" % locals()
    l1RunStatus = config.waitingStatus
    pass

pipeline.setVariable('l1RunStatus', l1RunStatus)

if not mergeStatus:
    print >> sys.stderr, 'Not removing run lock due to merging problems.'
    print >> sys.stderr, 'Failing due to presence of %s' % fileNames.mergeLockName(runId)
    sys.exit(1)
    pass

if readyToRetire and not verifyStatus :
    print >> sys.stderr, 'Not removing run lock due to missing data.'
    print >> sys.stderr, 'Failing due to presence of %s' % fileNames.verifyLockName(runId)
    sys.exit(2)
    pass

print >> sys.stderr, \
    "Attempting to remove lock from [%s] at [%s]" % (rootDir, time.ctime())
lockFile.unlockDir(rootDir, runId, dlId)
    
