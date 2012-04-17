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

    l1Setup = config.l1Setup
    instDir = config.L1Build
    glastExt = config.glastExt
    
    tStart = float(os.environ['tStart']) - config.ft2Pad
    tStop = float(os.environ['tStop']) + config.ft2Pad

    template = config.ft2Template
    templOpt = '-templateFT2 %s' % template

    cmd = '''
    cd %(workDir)s
    export INST_DIR=%(instDir)s 
    export GLAST_EXT=%(glastExt)s
    TIMING_DIR=$GLAST_EXT/extFiles/v0r9/jplephem ; export TIMING_DIR
    source %(l1Setup)s
    %(app)s -m7file %(stagedM7File)s -ft2file %(stagedFt2FitsFile)s -ft2start %(tStart).17g -ft2stop %(tStop).17g %(templOpt)s
    ''' % locals()

    status |= runner.run(cmd)

    return status
