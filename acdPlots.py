#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

if __name__ == "__main__":
    print >> sys.stderr, "This module is not supported as main script"
    sys.exit(1)

import config

import GPLinit

import runner


def acdPlots(files, idArgs, **args):
    fileType = 'acdPlots'

    status = 0

    dlId, runId, chunkId, crumbId = idArgs

    stagedInFile = files['digiHist']
    stagedOutFile = files[fileType]

    package = config.packages['Monitor']
    setup = package['setup']
    app = config.apps[fileType]

    libraryPath = config.libraryPath

    cmd = '''
    source %(setup)s
    #export LD_LIBRARY_PATH=%(libraryPath)s
    %(app)s -i %(stagedInFile)s -t %(stagedOutFile)s
    ''' % locals()

    status |= runner.run(cmd)

    return status
