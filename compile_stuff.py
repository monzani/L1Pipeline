#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

sys.path.append(config.gplPath)

import runner


if len(sys.argv) > 1:
    names = sys.argv[1:]
else:
    names = config.cvsPackages.keys() + config.cmtPackages.keys()
    pass

def doPackage(packName):
    if packName in config.cmtPackages:
        doCmtPackage(packName)
    elif packName in config.cvsPackages:
        doCvsPackage(packName)
        pass
    return

def doCmtPackage1(packName):
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
    return

def doCmtPackage2(packName):
    package = config.packages[packName]

    args = {
        'L1Cmt': config.L1Cmt,
        'l1SetupScript': os.path.join(config.L1ProcROOT, 'setup.sh'),
        }
    args.update(package)

    cmd = '''
    source %(l1SetupScript)s
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
    return

doCmtPackage = doCmtPackage2


def doCvsPackage(packName):
    package = config.packages[packName]

    args = {
        'l1SetupScript': os.path.join(config.L1ProcROOT, 'setup.sh'),
        'tmpDir': os.path.join('/tmp', config.fullTaskName),
        }
    args.update(package)
    
    cmd = '''
    source %(l1SetupScript)s
    tmpDir=%(tmpDir)s
    mkdir -p $tmpDir
    cd $tmpDir
    checkOutName=%(checkOutName)s
    cvs co -r %(version)s $checkOutName
    root=%(root)s
    rm -rf $root
    mkdir -p $(dirname $root)
    mv $checkOutName $root
    rm -rf $tmpDir
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


# for packName in names:
#     package = config.packages[packName]

#     args = {
#         'glastSetup': config.glastSetup,
#         'L1Cmt': config.L1Cmt,
#         'glastExt': config.glastExt,
#         'cmtConfig': config.cmtConfig,
#         'cmtPath': config.cmtPath,
#         'rootSys': config.rootSys,
#         }
#     args.update(package)

#     cmd = '''
#     source %(glastSetup)s
#     CMTCONFIG=%(cmtConfig)s ; export CMTCONFIG
#     CMTPATH=%(cmtPath)s ; export CMTPATH
#     GLAST_EXT=%(glastExt)s ; export GLAST_EXT
#     LD_LIBRARY_PATH="" ; export LD_LIBRARY_PATH
#     ROOTSYS=%(rootSys)s ; export ROOTSYS
#     cd %(L1Cmt)s
#     rm -rf %(root)s
#     cmt co -r %(version)s %(checkOutName)s
#     cd %(cmtDir)s
#     cmt config
#     make clean
#     make
#     ''' % args

#     runner.run(cmd)

#     if packName == "Monitor":
#         cmd = os.path.join(config.L1ProcROOT, 'compileRunStrip.py')
#         runner.run(cmd)
#         pass
    
#     continue

for packName in names:
    doPackage(packName)
    continue
