#!/sdf/group/fermi/a/isoc/flightOps/rhel6_gcc44/ISOC_PROD/bin/shisoc python2.6

"""@brief Make monitoring histograms.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

import config

backupGplTools = '/afs/slac.stanford.edu/g/glast/ground/PipelineConfig/GPLtools/prod/python'
sys.path.append(backupGplTools)

import runner

workDir = os.path.join('/tmp', `os.getpid()`)
os.mkdir(workDir)

codeDir = config.l1ExeDir

# You have to supply file names, but you don't actually need a file.
# This seems unlikely to exist.
digiFile = '/no/such/directory/noSuchFile.root'
calFile = digiFile
fastMonFile = digiFile
meritFile = digiFile
reconFile = digiFile
tkrMonFile = digiFile

if len(sys.argv) > 1:
    reportTypes = sys.argv[1:]
else:
    reportTypes = [
        'calHist', 'calTrend',
        'digiHist', 'digiTrend',
        'fastMonTrend',
        'meritHist', 'meritTrend',
        'reconHist', 'reconTrend',
        'tkrTrend',
        ]
    pass

for reportType in reportTypes:

    options = config.monitorOptions[reportType]

    package = config.packages['Monitor']
    l1Setup = config.l1Setup
    app = package['app']


    if 'fastMon' in reportType:
        inFileOpts = '-f %s' % fastMonFile
    elif 'tkrTrend' in reportType:
        inFileOpts = '-k %s' % tkrMonFile
    else:
        inFileOpts = '-d %s' % digiFile
        if 'recon' in reportType:
            inFileOpts += ' -r %s -a %s' % (reconFile, calFile)
        elif 'merit' in reportType:
            inFileOpts += ' -m %s' % (meritFile,)
            pass
        pass
 
    tdBin = config.tdBin[reportType]

    # CHANGE THIS!
    tmpHead = 'temp'
    tmpOut = tmpHead + '_time.root'
    htmlHead = 'html'

    instDir = config.L1Build
    glastExt = config.glastExt

    cmd = '''
    cd %(workDir)s
    export INST_DIR=%(instDir)s 
    export GLAST_EXT=%(glastExt)s
    source %(l1Setup)s
    %(app)s -b %(tdBin)s -c %(options)s %(inFileOpts)s -o %(tmpHead)s -g %(htmlHead)s -w %(codeDir)s -q || exit 1
    ''' % locals()

    status = runner.run(cmd)

    continue

for fileName in os.listdir(workDir): os.remove(os.path.join(workDir, fileName))
os.rmdir(workDir)
