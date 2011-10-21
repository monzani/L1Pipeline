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


def makeFT1(files, inFileTypes, outFileTypes, workDir, **args):
    status = 0

    inFileType = inFileTypes[0]

    assert len(outFileTypes) == 1
    outFileType = outFileTypes[0]

    evtClassDefsPython = config.packages['evtClassDefs']['python']

    stSetup = config.stSetup
    app = config.apps['makeFT1']

    stagedMeritFile = files[inFileType]
    stagedFt1File = files[outFileType]

    xmlClassifier = config.xmlClassifier
    tCuts = config.filterClassifyMap[outFileType]['cutFile']
    classifier = config.filterClassifyMap[outFileType]['classifier']
    dictionary = config.filterClassifyMap[outFileType]['ft1Dict']

    # run start and stop from merit file
    mStart, mStop = meritFiles.startAndStop(stagedMeritFile)
    print >> sys.stderr, 'merit:', mStart, mStop

    cutStart = rounding.roundDown(mStart, config.ft1Digits)
    cutStop = rounding.roundUp(mStop, config.ft1Digits)

    version = fileNames.version(stagedFt1File)
    procVer = config.procVer

    instDir = config.ST
    glastExt = config.glastExt

    cmd = '''
    cd %(workDir)s
    export INST_DIR=%(instDir)s 
    export GLAST_EXT=%(glastExt)s 
    source %(stSetup)s
    PYTHONPATH=%(evtClassDefsPython)s:$PYTHONPATH ; export PYTHONPATH
    %(app)s rootFile=%(stagedMeritFile)s fitsFile=%(stagedFt1File)s TCuts=%(tCuts)s xml_classifier="%(xmlClassifier)s" evtclsmap=%(classifier)s tstart=%(cutStart).17g tstop=%(cutStop).17g dict_file=%(dictionary)s file_version=%(version)s proc_ver=%(procVer)s
    ''' % locals()

    status |= runner.run(cmd)

    return status
