#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc --add-env=oracle11 python2.5

import os
import sys

import config

#import cx_Oracle

import GPLinit

#import acqQuery
import fileNames
import pipeline
import registerPrep
import runner
import stageFiles

status = 0

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

staged = stageFiles.StageSet(excludeIn=config.excludeIn)
finishOption = config.finishOption

# runNumber = int(runId.lstrip('r0'))

# def checkRunStatus(runNumber):
#     con = cx_Oracle.connect(config.connectString)
#     cur = con.cursor()
#     cmd = 'select STATUS from GLASTOPS_ACQSUMMARY where STARTEDAT = %s' % runNumber
#     print >> sys.stderr, cmd
    
#     stuff = cur.execute(cmd)
#     results = cur.fetchall()
#     con.close()

#     if len(results) != 1:
#         # If the run is not in ACQSUMMARY, something is wrong.
#         # If there are multiple entries, something is wrong.
#         # In either case, err on the side of caution.
#         print >> sys.stderr, "Did not get exactly 1 status for run %s, results=%s; not retiring." % (runNumber, results)
#         return False, "WeirdlyBroken"
    
#     runStatus = results[0][0]
#     statusFinal = runStatus in ['Complete', 'Incomplete']

#     print >> sys.stderr, 'Run %s has status %s, final=%s' % \
#           (runNumber, runStatus, statusFinal)

#     return statusFinal, runStatus

# staged = stageFiles.StageSet(excludeIn=config.excludeIn)
# finishOption = config.finishOption

# final, acqStatus = checkRunStatus(runNumber)

# if acqStatus != 'Complete':
#     print >> sys.stderr, "Can't make gaps for non-complete runs!"
#     sys.exit(1)
#     pass

realDigiFile = fileNames.fileName('digi', dlId, runId)
stagedDigiFile = staged.stageIn(realDigiFile)

#runDir = fileNames.fileName(None, None, runId)
#realGapFile = os.path.join(runDir, 'gaps.txt')
realGapFile = fileNames.fileName('gap', dlId, runId, next=True)
stagedGapFile = staged.stageOut(realGapFile)

workDir = os.path.dirname(stagedDigiFile)

package = config.packages['findGaps']
setup = package['setup']

app = config.apps['findGaps']

cmd = '''
cd %(workDir)s
source %(setup)s
%(app)s -d %(stagedDigiFile)s -g %(stagedGapFile)s
''' % locals()

#open(stagedGapFile, 'w').close()
status |= runner.run(cmd)
if status: finishOption = 'wipe'

registerPrep.prep('gap', realGapFile)
#pipeline.setVariable('L1_gap_fileName', realGapFile)

status |= staged.finish(finishOption)

sys.exit(status)
