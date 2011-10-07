#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

backupGplTools = '/afs/slac.stanford.edu/g/glast/ground/PipelineConfig/GPLtools/prod/python'
sys.path.append(backupGplTools)

import runner


if len(sys.argv) > 1:
    names = sys.argv[1:]
else:
    names = config.cvsPackages.keys() + config.sConsPackages.keys() + config.cmtPackages.keys()
    pass

def doPackage(packName):
    if packName in config.sConsPackages:
        doSConsPackage(packName)
    #elif packName in config.cmtPackages:
    #    doCmtPackage(packName)
    elif packName in config.cvsPackages:
        doCvsPackage(packName)
        pass
    return

def doSConsPackage(packName):
    package = config.packages[packName]

    args = {
        'L1Build': config.L1Build,
        'glastLocation': config.glastLocation,
        'glastExt': config.glastExt,
        'scons': config.scons,
        'packName': packName,
        }
    args.update(package)

    cmd = '''
    root=%(root)s
    rm -rf $root
    mkdir -p $(dirname $root)
    cd %(L1Build)s
    cvs co -r %(version)s -d %(root)s %(checkOutName)s
    cd %(glastLocation)s 
    %(scons)s --with-GLAST-EXT=%(glastExt)s --supersede %(L1Build)s --compile-opt %(packName)s 
    ''' % args

    runner.run(cmd)

    if packName == "Monitor":
        cmd = os.path.join(config.L1ProcROOT, 'compileRunStrip.py')
        runner.run(cmd)
        pass
    return



def doCmtPackage(packName):
    package = config.packages[packName]

    args = {
        'L1Build': config.L1Build,
        }
    args.update(package)

    cmd = '''
    root=%(root)s
    rm -rf $root
    mkdir -p $(dirname $root)
    cd %(L1Build)s
    cvs co -r %(version)s -d %(root)s %(checkOutName)s
    ''' % args

    runner.run(cmd)

    if packName == "Monitor":
        #cmd = os.path.join(config.L1ProcROOT, 'compileRunStrip.py')
        #runner.run(cmd)
        pass
    return




def doCvsPackage(packName):
    package = config.packages[packName]

    args = {
        'L1Build': config.L1Build,
        }
    args.update(package)

    cmd = '''
    root=%(root)s
    rm -rf $root
    mkdir -p $(dirname $root)
    cd %(L1Build)s
    cvs co -r %(version)s -d %(root)s %(checkOutName)s
    ''' % args

    if packName == 'IGRF':
        igrfDir = os.path.join(package['root'], 'python')
        cmd += '''cd %s
        make clean
        make
        ''' % igrfDir
        pass

    runner.run(cmd)

    return

for packName in names:
    doPackage(packName)
    continue
