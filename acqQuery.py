
import os
import random
import sys
import time

import cx_Oracle

import config

#import GPLinit


class acqError(Exception):
    pass


def waitABit(minDelay=None, maxDelay=None):
    if minDelay is None: minDelay = config.minDbWait
    if maxDelay is None: maxDelay = config.maxDbWait
    delay = random.randrange(minDelay, maxDelay+1)
    log.info("Waiting %d seconds." % delay)
    time.sleep(delay)
    return


def query(runs, fields):
    '''@brief Query fields from ACQSUMMARY

    @arg runs An ieterable of run numbers.

    @arg fields An iterable of fields to query.

    @return A dictionary with run number for keys and iterables of field vaules,
    in order, as values.
    
    '''

    augFields = ['STARTEDAT'] + list(fields)
    fieldStr = ', '.join(augFields)
    runStr = '(' + ', '.join(str(run) for run in runs) + ')'
    cmd = 'select %s from %s where STARTEDAT in %s' % (fieldStr, config.acqTable, runStr)
    print >> sys.stderr, cmd
    
    connectString = config.connectString
    print >> sys.stderr, 'Connecting to %s' % connectString

    for retry in range(config.dbRetries):
        try:
            if retry: waitABit()
            dbOk = False
            con = cx_Oracle.connect(connectString)
            cur = con.cursor()
            stuff = cur.execute(cmd)
            results = cur.fetchall()
            con.close()
            dbOk = True
            break
        except cx_Oracle.DatabaseError:
            continue
        continue
    print >> sys.stderr, 'Status %s after %d tries.' % (dbOk, retry+1)
    if not dbOk: raise acqError

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
            start = os.environ['tStart']
            stop = os.environ['tStop']
            return start, stop
        else:
            raise
        pass
        
    results = tuple(glastTime.dt2Met(dt) for dt in row)

    return results
