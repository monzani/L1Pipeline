#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc --add-env=oracle11 python2.5

"""@brief Make sure we are done processing a run/downlink.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys
import time

import cx_Oracle

import config
import fileNames
import lockFile
import pipeline


def checkRunStatus(runNumber):
    con = cx_Oracle.connect(config.connectString)
    cur = con.cursor()
    cmd = 'select STATUS from GLASTOPS_ACQSUMMARY where STARTEDAT = %s' % runNumber
    print >> sys.stderr, cmd
    
    stuff = cur.execute(cmd)
    results = cur.fetchall()
    con.close()

    if len(results) != 1:
        # If the run is not in ACQSUMMARY, something is wrong.
        # If there are multiple entries, something is wrong.
        # In either case, err on the side of caution.
        print >> sys.stderr, "Did not get exactly 1 status for run %s, results=%s; not retiring." % (runNumber, results)
        return False
    
    runStatus = results[0][0]
    statusFinal = runStatus in ['Complete', 'Incomplete']

    print >> sys.stderr, 'Run %s has status %s, final=%s' % \
          (runNumber, runStatus, statusFinal)

    return statusFinal

def checkTokens(head, runId):
    tokenDir = fileNames.tokenDir(head, runId)
    print >> sys.stderr, 'Looking for chunk tokens in %s' % tokenDir
    try:
        tokenFiles = os.listdir(tokenDir)
    except OSError:
        # Probably should not cleanup here if we're in prod mode.
        print >> sys.stderr, 'Token directory %s is nonexistent or unreadable.' % tokenDir
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

runNumber = os.environ['runNumber']

rootDir = os.path.dirname(fileNames.fileName('chunkList', dlId, runId)) #bleh

# Here we need to check that all the chunk locks (created by the halfpipe,
# removed by this script before now) are gone, AND that some database
# somewhere (GLAST_ISOC.ACQSUMMARY) says that the run is as complete as it
# will get, before launching cleanup and updating run status in the data
# catalog.
#
# but for now we punt
#readyToRetire = False

runStatus = checkRunStatus(runNumber)
tokenStatus = checkTokens(head, runId)
readyToRetire = runStatus and tokenStatus

subTask = config.cleanupSubTask[os.environ['DATASOURCE']]

if readyToRetire:
    print >> sys.stderr, "Run %s is as done as it's going to get, retiring." % runId
    stream = 0
    args = ''
    pipeline.createSubStream(subTask, stream, args)
else:
    print >> sys.stderr, "Not retiring run %s: runStatus=%s, toeksnStatus=%s" % (runId, runStatus, tokenStatus)
    pass

# Here we should copy the run status from ACQSUMMARY to Karen's table.

print >> sys.stderr, \
      "Attempting to remove lock from [%s] at [%s]" % (rootDir, time.ctime())
lockFile.unlockDir(rootDir, runId, dlId)

