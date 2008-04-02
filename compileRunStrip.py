#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Make monitoring histograms.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

import config

sys.path.append(config.gplPath)

import runner

workDir = os.path.join('/tmp', `os.getpid()`)
os.mkdir(workDir)

codeDir = config.packages['Monitor']['bin']

digiFile = '/no/such/directory/no_such_file.root'
calFile = digiFile
fastMonFile = digiFile
meritFile = digiFile
reconFile = digiFile

if len(sys.argv) > 1:
    reportTypes = sys.argv[1:]
else:
    reportTypes = [
        'calEor', 'calTrend',
        'digiEor', 'digiTrend',
        'fastMonTrend',
        'meritEor', 'meritTrend',
        'reconEor', 'reconTrend',
        ]
    pass

for reportType in reportTypes:

    options = config.monitorOptions[reportType]

    package = config.packages['Monitor']
    setup = package['setup']
    app = package['app']


    if 'fastMon' in reportType:
        inFileOpts = '-f %s' % fastMonFile
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

    cmd = """cd %(workDir)s
source %(setup)s
%(app)s -b %(tdBin)s -c %(options)s %(inFileOpts)s -o %(tmpHead)s -g %(htmlHead)s -w %(codeDir)s -q || exit 1
""" % locals()

    status = runner.run(cmd)

    continue

for fileName in os.listdir(workDir): os.remove(os.path.join(workDir, fileName))
os.rmdir(workDir)
