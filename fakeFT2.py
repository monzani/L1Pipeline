#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""Should merge this with ft2Entries.
"""

import os
import sys

import config

import runner
import pipeline

def fakeFT2(files, workDir, runDir, staged, idArgs, **args):
    status = 0

    dlId, runId, chunkId, crumbId = idArgs

    app = config.apps['makeFT2']

    # input file
    # for fake FT2 M7
    realM7File = os.path.join(os.environ['DOWNLINK_RAWDIR'], 'magic7_%s.txt' % dlId)
    stagedM7File = staged.stageIn(realM7File)

    # output
    stagedFt2FitsFile = files['ft2Fake']
    ft2FakeBase = os.path.basename(stagedFt2FitsFile )
    permanentFt2File = os.path.join(runDir, ft2FakeBase)
    for stagee in staged.stagedFiles:
        if stagee.location == stagedFt2FitsFile: break
        continue
    stagee.destinations.append(permanentFt2File)

    setupScript = config.packages['ft2Util']['setup']
    
    tStart = float(os.environ['tStart']) - config.ft2Pad
    tStop = float(os.environ['tStop']) + config.ft2Pad

    cmtPath = config.cmtPath

    cmd = '''
    cd %(workDir)s
    export CMTPATH=%(cmtPath)s
    source %(setupScript)s
    %(app)s -m7file %(stagedM7File)s -ft2file %(stagedFt2FitsFile)s -ft2start %(tStart).17g -ft2stop %(tStop).17g
    ''' % locals()

    status |= runner.run(cmd)

    return status
