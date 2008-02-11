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
reconFile = digiFile
calFile = digiFile

reportTypes = [
    'digiEor', 'digiTrend',
    'reconEor', 'reconTrend',
    'calEor', 'calTrend',
    ]
for reportType in reportTypes:

    options = config.monitorOptions[reportType]

    package = config.packages['Monitor']
    setup = package['setup']
    app = package['app']


    if 'recon' in reportType:
        recon = '-r %s -a %s' % (reconFile, calFile)
    else:
        recon = ''
        pass

    tdBin = config.tdBin[reportType]

    # CHANGE THIS!
    tmpHead = 'temp'
    tmpOut = tmpHead + '_time.root'
    htmlHead = 'html'

    cmd = """cd %(workDir)s
source %(setup)s
%(app)s -b %(tdBin)s -c %(options)s -d %(digiFile)s %(recon)s -o %(tmpHead)s -g %(htmlHead)s -w %(codeDir)s -q || exit 1
""" % locals()

    status = runner.run(cmd)

    continue

for fileName in os.listdir(workDir): os.remove(os.path.join(workDir, fileName))
os.rmdir(workDir)
