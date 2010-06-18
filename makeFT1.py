#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc --add-env=oracle11 python2.5

import os
import sys

if __name__ == "__main__":
    print >> sys.stderr, "This module is not supported as main script"
    sys.exit(1)

import config

import fileNames
import meritFiles
import runner
import rounding


def makeFT1(files, level, outFileTypes, workDir, **args):
    status = 0

    assert len(outFileTypes) == 1
    fileType = outFileTypes[0]

    evtClassDefsPython = config.packages['evtClassDefs']['python']

    stSetup = config.stSetup
    app = os.path.join('$FITSGENROOT', '$CMTCONFIG', 'makeFT1.exe')

    stagedMeritFile = files['merit']

    stagedFt1File = files[fileType]

    tCuts = config.cutFiles[fileType]
    classifier = config.ft1Classifier

    # run start and stop from merit file
    mStart, mStop = meritFiles.startAndStop(stagedMeritFile)
    print >> sys.stderr, 'merit:', mStart, mStop

    cutStart = rounding.roundDown(mStart, config.ft1Digits)
    cutStop = rounding.roundUp(mStop, config.ft1Digits)

    dictionary = config.ft1Dicts[fileType[:3]]

    version = fileNames.version(stagedFt1File)

    cmtPath = config.stCmtPath

    cmd = '''
    cd %(workDir)s
    export CMTPATH=%(cmtPath)s
    source %(stSetup)s
    PYTHONPATH=%(evtClassDefsPython)s:$PYTHONPATH ; export PYTHONPATH
    %(app)s rootFile=%(stagedMeritFile)s fitsFile=%(stagedFt1File)s TCuts=%(tCuts)s event_classifier="%(classifier)s" tstart=%(cutStart).17g tstop=%(cutStop).17g dict_file=%(dictionary)s file_version=%(version)s
    ''' % locals()

    status |= runner.run(cmd)

    return status
