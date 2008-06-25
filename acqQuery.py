
import sys

import cx_Oracle

import config

import GPLinit



def checkRunStatus(runNumber, field):
    con = cx_Oracle.connect(config.connectString)
    cur = con.cursor()
    cmd = 'select %s from %s where STARTEDAT = %s' % \
          (field, config.acqTable, runNumber)
    print >> sys.stderr, cmd
    
    stuff = cur.execute(cmd)
    results = cur.fetchall()
    con.close()

    if len(results) != 1:
        print >> sys.stderr, "Did not get exactly 1 status for run %s, results=%s; not retiring." % (runNumber, results)
    
    runStatus = results[0][0]
    statusFinal = runStatus in ['Complete', 'Incomplete']

    print >> sys.stderr, 'Run %s has status %s, final=%s' % \
          (runNumber, runStatus, statusFinal)

    return statusFinal, runStatus

