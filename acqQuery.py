
import sys

import cx_Oracle

import config

#import GPLinit



def checkRunStatus(runNumber, field):
    '''broken junk'''
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


def query(runs, fields):
    '''@brief Query fields from ACQSUMMARY

    @arg runs An ieterable of run numbers.

    @arg fields An iterable of fields to query.

    @return A dictionary with run number for keys and iterables of field vaules,
    in order, as values.
    
    '''

    con = cx_Oracle.connect(config.connectString)
    cur = con.cursor()

    augFields = ['STARTEDAT'] + list(fields)
    fieldStr = ', '.join(augFields)
    runStr = '(' + ', '.join(str(run) for run in runs) + ')'
    cmd = 'select %s from %s where STARTEDAT in %s' % (fieldStr, config.acqTable, runStr)
    print >> sys.stderr, cmd
    
    stuff = cur.execute(cmd)
    results = cur.fetchall()
    con.close()

    dResults = dict((row[0], row[1:]) for row in results)

    return dResults


def runTimes(run):
    '''@brief Get MET of first and last events observed in a run.

    @arg run The run number.

    @return tStart, tStop

    '''
    import glastTime

    fields = ['EVTUTC0', 'EVTUTC1']
    dtResults = query([run], fields)

    try:
        row = dtResults[run]
    except KeyError:
        print >> sys.stderr, "Run %s isn't in acqsummary!" % run
        if config.testMode:
            print >> sys.stderr, "Returning bogus times."
            return 238555581.0, 238555742.0
        else:
            raise
        pass
        
    results = tuple(glastTime.dt2Met(dt) for dt in row)

    return results
