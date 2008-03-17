#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

sys.path.append(config.gplPath)

import runner


if len(sys.argv) > 1:
    names = sys.argv[1:]
else:
    names = config.cmtPackages.keys()
    pass

for packName in names:
    package = config.packages[packName]

    args = {
        'glastSetup': config.glastSetup,
        'L1Cmt': config.L1Cmt,
        'glastExt': config.glastExt,
        'cmtConfig': config.cmtConfig,
        'cmtPath': config.cmtPath,
        'rootSys': config.rootSys,
        }
    args.update(package)

    cmd = '''
    source %(glastSetup)s
    CMTCONFIG=%(cmtConfig)s ; export CMTCONFIG
    CMTPATH=%(cmtPath)s ; export CMTPATH
    GLAST_EXT=%(glastExt)s ; export GLAST_EXT
    LD_LIBRARY_PATH="" ; export LD_LIBRARY_PATH
    ROOTSYS=%(rootSys)s ; export ROOTSYS
    cd %(L1Cmt)s
    rm -rf %(root)s
    cmt co -r %(version)s %(checkOutName)s
    cd %(cmtDir)s
    cmt config
    make clean
    make
    ''' % args

    runner.run(cmd)

    if packName == "Monitor":
        cmd = os.path.join(config.L1ProcROOT, 'compileRunStrip.py')
        runner.run(cmd)
        pass
    
    continue
