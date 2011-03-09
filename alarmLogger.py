#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

if __name__ == "__main__":
    print >> sys.stderr, "This module is not supported as main script"
    sys.exit(1)

import config

import GPLinit

import alarmParser
import runner

def alarmLogger(files, idArgs, inFileTypes, workDir, **args):
    status = 0

    dlId, runId, chunkId, crumbId = idArgs

    fileType, = inFileTypes

    stagedInFile = files[fileType]

    alarmParser.doAlarms(stagedInFile, fileType, dlId, runId)

    return status
