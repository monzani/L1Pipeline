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

#digiFile = os.path.join(config.L1ProcROOT, 'data', 'r0192524537_e00000000000000978971_digi.root')
#reconFile = os.path.join(config.L1ProcROOT, 'data', 'r0192524537_e00000000000000978971_recon.root')
digiFile = '/nfs/farm/g/glast/u33/borgland/Releases/GlastRelease-v12r11/Data/processing-Orbit-1_25k/digi.root'
reconFile = '/nfs/farm/g/glast/u33/borgland/Releases/GlastRelease-v12r11/Data/processing-Orbit-1_25k/recon.root'
calFile = '/nfs/farm/g/glast/u33/borgland/Releases/GlastRelease-v12r11/Data/processing-Orbit-1_25k/caltuple.root'

reportTypes = ['digiEor', 'digiTrend', 'reconEor', 'reconTrend']
for reportType in reportTypes:

    options = config.monitorOptions[reportType]
    fileType = config.monitorOutFiles[reportType]

    package = config.packages['Monitor']
    setup = package['setup']
    app = package['app']


    if 'recon' in reportType:
        recon = '-r %s -a %s' % (reconFile, calFile)
    else:
        recon = ''
        pass

    tdBin = config.tdBin

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
