#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc --add-env=oracle11 python2.5

import os
import sys

if __name__ == "__main__":
    print >> sys.stderr, "This module is not supported as main script"
    sys.exit(1)

import config

import runner


def diffRsp(files, outFileTypes, workDir, **args):
    status = 0

    inFileType = 'ft1NoDiffRsp'

    assert len(outFileTypes) == 1
    outFileType = outFileTypes[0]

    stSetup = config.stSetup
    app = os.path.join('$LIKELIHOODROOT', '$CMTCONFIG', 'gtdiffrsp.exe')

    stagedInFile = files[inFileType]

    stagedFt2File = files['ft2Fake']

    stagedOutFile = files[outFileType]

    model = config.diffRspModel
    irf = config.diffRspIrf

    diffRspMinClass = config.diffRspMinClass

    cmtPath = config.stCmtPath

    cmd = '''
    cd %(workDir)s
    export CMTPATH=%(cmtPath)s
    source %(stSetup)s
    mv %(stagedInFile)s %(stagedOutFile)s
    %(app)s scfile=%(stagedFt2File)s evfile=%(stagedOutFile)s srcmdl=%(model)s irfs=%(irf)s evclsmin=%(diffRspMinClass)r
    ''' % locals()
    
    status |= runner.run(cmd)

    return status
