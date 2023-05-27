#!/sdf/group/fermi/a/isoc/flightOps/rhel6_gcc44/ISOC_PROD/bin/shisoc python2.6

import os
import sys

import config

backupGplTools = '/afs/slac/g/glast/ground/PipelineConfig/GPLtools/prod/python'
sys.path.append(backupGplTools)

import runner


if len(sys.argv) > 1:
    names = sys.argv[1:]
else:
    names = config.cvsPackages.keys() + config.githubPackages.keys() + config.sConsPackages.keys()
    pass

def doPackage(packName):
    if packName in config.sConsPackages:
        doSConsPackage(packName)
    elif packName in config.cvsPackages:
        doCvsPackage(packName)
    elif packName in config.githubPackages:
        doGithubPackage(packName)
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
    packName=%(packName)s
    cvs co -r %(version)s -d %(packName)s %(checkOutName)s
    cd %(glastLocation)s 
    %(scons)s -C GlastRelease --with-GLAST-EXT=%(glastExt)s --supersede %(L1Build)s --site-dir=../SConsShared/site_scons --compile-opt %(packName)s 
    ''' % args

    runner.run(cmd)

    if packName == "Monitor":
        cmd = os.path.join(config.L1ProcROOT, 'compileRunStrip.py')
        runner.run(cmd)
        pass
    return


def doGithubPackage(packName):
    package = config.packages[packName]

    args = {
        'L1Build': config.L1Build,
        'glastLocation': config.glastLocation,
        'glastExt': config.glastExt,
        'scons': config.scons,
        'packName': packName,
        }
    args.update(package)

    args['source'] = '%(repository)s/archive/%(version)s.tar.gz' % args
    args['directory'] = '%(packName)s-%(version)s' % args

    cmd = '''
    root=%(root)s
    rm -rf $root
    mkdir -p $(dirname $root)
    cd %(L1Build)s
    packName=%(packName)s
    wget -O - %(source)s | tar xzv
    mv %(directory)s %(packName)s
    cd %(glastLocation)s 
    %(scons)s -C GlastRelease --with-GLAST-EXT=%(glastExt)s --supersede %(L1Build)s --site-dir=../SConsShared/site_scons --compile-opt %(packName)s 
    ''' % args

    runner.run(cmd)


def doCvsPackage(packName):
    package = config.packages[packName]

    args = {
        'L1Build': config.L1Build,
        'packName': packName,
        }
    args.update(package)

    cmd = '''
    root=%(root)s
    rm -rf $root
    mkdir -p $(dirname $root)
    cd %(L1Build)s
    packName=%(packName)s
    cvs co -r %(version)s -d %(packName)s %(checkOutName)s
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
