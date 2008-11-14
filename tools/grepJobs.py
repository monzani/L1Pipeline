#!/usr/bin/env python

import os
import re
import sys
import time

verbose = True

ofRe = re.compile('OutputFile<(.*?)>', re.S)
spaceRe = re.compile('\s')
l1JobRe = re.compile('^([0-9]+)\s+glastraw\s+RUN\s+glastdataq')


def l1Jobs():
    cmd = 'bjobs -wu glastraw'
    jobs = []
    for line in os.popen(cmd):
        mob = l1JobRe.match(line)
        if mob:
            jobs.append(mob.group(1))
            pass
        continue
    return jobs


def getLog(jobId):
    cmd = 'bjobs -l %s' % jobId
    data = os.popen(cmd).read()
    data = spaceRe.sub('', data)
    mob = ofRe.search(data)
    name = mob.group(1)
    return name


def grepFile(fileName, reOb):
    match = False
    for line in open(fileName):
        if reOb.search(line):
            match = True
            break
        continue
    return match

def tailFile(fileName, reOb):
    match = False
    line = os.popen('tail -1 %s' % fileName).read()
    if reOb.search(line):
        match = True
        if verbose: print >> sys.stderr, line,
        pass
    return match

def grepJob(jobId, reOb):
    logFile = getLog(jobId)
    match = grepFile(logFile, reOb)
    return match


def tailJob(jobId, reOb):
    logFile = getLog(jobId)
    match = tailFile(logFile, reOb)
    return match


def checkJobs(jobs):
    test = set(jobs)
    current = set(l1Jobs())
    goodJobs = test & current
    return goodJobs


def grepAllJobs(pattern):
    reOb = re.compile(pattern)
    jobs = l1Jobs()
    matches = [job for job in jobs if grepJob(job, reOb)]
    good = checkJobs(matches)
    return good


def tailAllJobs(pattern):
    reOb = re.compile(pattern)
    jobs = l1Jobs()
    matches = [job for job in jobs if tailJob(job, reOb)]
    good = checkJobs(matches)
    return good


def stopIfTail(jobs, reOb):
    stopped = []
    for job in jobs:
        if tailJob(job, reOb):
            chatter = os.popen('bstop %s' % job).read()
            if verbose: print >> sys.stderr, chatter,
            stopped.append(job)
            pass
        continue
    return stopped


def main_grepAll():
    pattern = sys.argv[1]
    matches = grepAllJobs(pattern)
    for match in matches:
        print match,
        continue
    print
    return


def main_tailStopAll():
    pattern, waitAfterStop, waitBetweenJobs = sys.argv[1:]
    reOb = re.compile(pattern)
    waitAfterStop = float(waitAfterStop)
    waitBetweenJobs = float(waitBetweenJobs)

    jobs = l1Jobs()    
    jobs = stopIfTail(jobs, reOb)
    print ' '.join(jobs)

    now = time.time()
    then = time.ctime(now + waitAfterStop)
    if verbose: print >> sys.stderr, 'Sleeping until %s (%ss)' % (then, waitAfterStop)
    time.sleep(waitAfterStop)

    for job in jobs:
        chatter = os.popen('bresume %s' % job).read()
        if verbose: print >> sys.stderr, chatter,
        time.sleep(waitBetweenJobs)
        continue

    return

main = main_tailStopAll

if __name__ == "__main__":
    main()
    
    
