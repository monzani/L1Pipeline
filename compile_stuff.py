#!/sdf/group/fermi/a/isoc/flightOps/rhel6_gcc44/ISOC_PROD/bin/shisoc python2.6

import os
import sys

import config

backupGplTools = '/sdf/group/fermi/a/ground/PipelineConfig/L1Proc/5.9/GPLtools/python'
sys.path.append(backupGplTools)

import runner


if len(sys.argv) > 1:
    names = sys.argv[1:]
else:
    names = config.githubPlain.keys() + config.githubSCons.keys()
    pass

def doPackage(packName):
    if packName in config.githubPlain:
        doGithubPlain(packName)
    elif packName in config.githubSCons:
        doGithubSCons(packName)
        pass
    return

def doGithubSCons(packName):
    package = config.packages[packName]

    args = {
        'L1Build': config.L1Build,
        'glastLocation': config.glastLocation,
        'glastExt': config.glastExt,
        'scons': config.scons,
        'githubMain': config.githubMain,
        'packName': packName,
        }
    args.update(package)

    args['source'] = '%(githubMain)s/%(packName)s/archive/%(version)s.tar.gz' % args
    args['directory'] = '%(packName)s-%(version)s' % args

    cmd = '''
    root=%(root)s
    rm -rf $root
    mkdir -p $(dirname $root)
    cd %(L1Build)s
    packName=%(packName)s
    directory=%(directory)s
    wget -O - %(source)s | tar xzv
    mv %(directory)s %(packName)s
    cd %(glastLocation)s 
    %(scons)s -C GlastRelease --with-GLAST-EXT=%(glastExt)s --supersede %(L1Build)s --site-dir=../SConsShared/site_scons --compile-opt %(packName)s 
    ''' % args

    runner.run(cmd)

    if packName == "Monitor":
        cmd = os.path.join(config.L1ProcROOT, 'compileRunStrip.py')
        runner.run(cmd)
        pass
    return


def doGithubPlain(packName):
    package = config.packages[packName]

    args = {
        'L1Build': config.L1Build,
        'githubMain': config.githubMain,
        'packName': packName,
        }
    args.update(package)

    args['source'] = '%(githubMain)s/%(packName)s/archive/%(version)s.tar.gz' % args
    args['directory'] = '%(packName)s-%(version)s' % args

    cmd = '''
    root=%(root)s
    rm -rf $root
    mkdir -p $(dirname $root)
    cd %(L1Build)s
    packName=%(packName)s
    directory=%(directory)s
    wget -O - %(source)s | tar xzv
    mv %(directory)s %(packName)s
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
