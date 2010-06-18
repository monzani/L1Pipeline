#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Make monitoring histograms.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

if __name__ == "__main__":
    print >> sys.stderr, "This module is not supported as main script"
    sys.exit(1)

import config

import runner


def runStrip(files, idArgs, outFileTypes, workDir, **args):
    status = 0

    assert len(outFileTypes) == 1
    reportType = outFileTypes[0]

    options = config.monitorOptions[reportType]

    package = config.packages['Monitor']
    setup = package['setup']
    app = package['app']

    outFile = files[reportType]

    if 'fastMon' in reportType:
        stagedFmt = files['fastMonTuple']
        inFileOpts = '-f %s' % stagedFmt
    elif 'tkrTrend' in reportType:
        stagedInFile = files['tkrMonitor']
        inFileOpts = '-k %s' % stagedInFile
    else:
        stagedDigiFile = files['digi']
        inFileOpts = '-d %s' % stagedDigiFile
        if 'recon' in reportType:
            stagedReconFile = files['recon']
            stagedCalFile = files['cal']
            inFileOpts += ' -r %s -a %s' % (stagedReconFile, stagedCalFile)
        elif 'merit' in reportType:
            stagedMeritFile = files['merit']
            inFileOpts += ' -m %s' % (stagedMeritFile,)
            configFile = config.normalizedRateConfigs[reportType]
            options += ' -e %s' % (configFile)
            pass
        pass

    tdBin = config.tdBin[reportType]

    codeDir = config.packages['Monitor']['bin']

    # if reportType in ['calHist', 'calTrend']:
    #     zOpt = '' # keep transient data in a temp file
    # else:
    #     zOpt = '-z' # keep transient data in memory
    #     pass
    zOpt = ''

    datasource = os.environ['DATASOURCE']
    if datasource == 'MC':
        mcOpt = '-t MC'
    else:
        mcOpt = ''
        pass

    # CHANGE THIS!
    tmpHead = 'temp'
    tmpOut = tmpHead + '_time.root'
    htmlHead = 'html'

    cmd = """cd %(workDir)s
    source %(setup)s
    %(app)s %(zOpt)s -b %(tdBin)s -c %(options)s %(inFileOpts)s -o %(tmpHead)s -g %(htmlHead)s -w %(codeDir)s -p %(mcOpt)s || exit 1
    mv %(tmpOut)s %(outFile)s
    """ % locals()

    status |= runner.run(cmd)

    return status

    
