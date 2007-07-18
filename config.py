"""@brief Configuration.

@author W. Focke <focke@slac.stanford.edu>
"""

import os

L1Version = "1.11"
installRoot = "/afs/slac.stanford.edu/g/glast/ground/PipelineConfig/SC/L1Pipeline"
L1ProcROOT = os.path.join(installRoot, L1Version)
L1Xml = os.path.join(L1ProcROOT, 'xml')

LATCalibRoot = '/afs/slac/g/glast/ground/releases/calibrations/'
L1Cmt = os.path.join(installRoot, 'builds')

L1Disk = '/nfs/farm/g/glast/u40/L1'
L1Dir = os.path.join(L1Disk, 'rootData')

# uncomment for test mode
# should have a software switch for this, possibly finding out
# from the pipeline whethter we're running on (test or dev) or prod server
#L1Dir = os.path.join(L1Dir, 'test')

afsStage = "/afs/slac/g/glast/ground/PipelineStaging"

maxCpu = 1000

#maxCrumbSize = 48000 # SVAC pipeline uses this
#maxCrumbSize = 250   # tiny
maxCrumbSize = 6353   # ~.5Hr on tori.  Also about half of medium q limit

glastRoot = '/afs/slac.stanford.edu/g/glast'
groundRoot = os.path.join(glastRoot, 'ground')
glastSetup = os.path.join(groundRoot, 'scripts', 'group.sh')
#
cmtConfig = 'rh9_gcc32opt'
installArea = os.path.join(L1Cmt, 'InstallArea', cmtConfig)
installBin = os.path.join(installArea, 'bin')
#
glastExt = os.path.join(groundRoot, 'GLAST_EXT', cmtConfig)
#
releaseDir = os.path.join(groundRoot, 'releases', 'volume14')
glastVersion = 'v8r1109p7'
releaseName = 'EngineeringModel'
gleamPackage = 'LatIntegration'
#
glastName = '-'.join((releaseName, glastVersion))
glastLocation = os.path.join(releaseDir, glastName)
gleam = os.path.join(glastLocation, 'bin', gleamPackage)
cmtScript = os.path.join(glastLocation, releaseName, glastVersion, 'cmt',
                         'setup.sh') # do we need this?
cmtPath = ':'.join((glastLocation, L1Cmt))
os.environ['CMTPATH'] = cmtPath
#
digiOptions = os.path.join(L1ProcROOT, 'digi.jobOpt')
reconOptions = os.path.join(L1ProcROOT, 'recon.jobOpt')

rootSys = os.path.join(glastExt, 'ROOT/v5.14.00d/root')
haddRootSys = rootSys
hadd = os.path.join(glastExt, haddRootSys, 'bin', 'hadd')


ST="/nfs/farm/g/glast/u30/builds/rh9_gcc32opt/ScienceTools/ScienceTools-v9"
PFILES="."
stBinDir = os.path.join(ST, 'bin')

packages = {
    'Common': {
        'repository': 'dataMonitoring',
        'version': 'v1r2p0',
        },
    'FastMon': {
        'repository': 'dataMonitoring',
        'version': 'v1r1p0',
        },
    'Monitor': {
        'repository': 'svac',
        'version': 'mk20070716',
        },
    'TestReport': {
        'repository': 'svac',
        'version': 'TRdp20070706',
        },
    'EngineeringModelRoot': {
        'repository': 'svac',
        'version': 'v3r0p3',
        },
    'pipelineDatasets': {
        'repository': 'users/richard',
        'version': 'v0r4',
        },
    }

# fill in standard values for standard packages
for packName in packages:
    package = packages[packName]
    packages[packName]['root'] = os.path.join(L1Cmt, packName, package['version'])
    package['bin'] = os.path.join(package['root'], cmtConfig)
    package['cmtDir'] = os.path.join(package['root'], 'cmt')
    package['setup'] = os.path.join(package['cmtDir'], 'setup.sh')
    package['checkOutName'] = os.path.join(package['repository'], packName)
    continue

# add nonstandard package info
packages['FastMon']['app'] = os.path.join(packages['FastMon']['root'],
                                          'python', 'pDataProcessor.py')
packages['FastMon']['env'] = {
    'XML_CONFIG_DIR': os.path.join(packages['FastMon']['root'], 'xml'),
    }
packages['FastMon']['extraSetup'] = 'eval `/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/isoc isoc_env --add-env=flightops --add-env=root`'

packages['Monitor']['app'] = os.path.join(packages['Monitor']['bin'],
                                          'runStrip_t.exe')
packages['Monitor']['configDir'] = os.path.join(packages['Monitor']['root'],
                                                'src')

packages['TestReport']['app'] = os.path.join(packages['TestReport']['bin'],
                                             'TestReport.exe')
packages['TestReport']['mergeApp'] = os.path.join(packages['TestReport']['bin'],
                                                  'MergeHistFiles.exe')

packages['EngineeringModelRoot']['app'] = os.path.join(packages['EngineeringModelRoot']['bin'], 'RunRootAnalyzer.exe')


apps = {
    'digi': gleam,
    'digiMon': packages['TestReport']['app'],
    'digiEor': packages['Monitor']['app'],
    'fastMon': packages['FastMon']['app'],
    'makeFT1': os.path.join(stBinDir, 'makeFT1'),
    'recon': gleam,
    'reconMon': packages['TestReport']['app'],
    'reportMerge': packages['TestReport']['mergeApp'],
    'svacTuple': packages['EngineeringModelRoot']['app'],
    }

monitorOptions = {
    'digiEor': os.path.join(packages['Monitor']['configDir'],
                            'monconfig_digi_end2end_histos.xml'),
    'digiTdMon': os.path.join(packages['Monitor']['configDir'],
                              'monconfig_digi_end2end_trending.xml'),
    'reconEor': os.path.join(packages['Monitor']['configDir'],
                             'monconfig_recon_end2end_histos.xml'),
    'reconTdMon': os.path.join(packages['Monitor']['configDir'],
                               'monconfig_recon_end2end_trending.xml'),
    }

monitorOutFiles = {
    'fastMon': 'FASTMON',
    'digiEor': 'DIGIHIST',
    'digiTdMon': 'tripe',
    'reconEor': 'RECONHIST',
    'reconTdMon': 'tripe',
    }

mergeConfigs = {
    'digiEor': os.path.join(packages['Monitor']['configDir'],
                            'MergeHistos_e2e_digi.txt'),
    'digiMon': os.path.join(L1ProcROOT, 'merge_digi.txt'),
    'fastMon': os.path.join(L1ProcROOT, 'fast_mon_config.txt'),
    'reconEor': os.path.join(packages['Monitor']['configDir'],
                             'MergeHistos_e2e_recon.txt'),
    'reconMon': os.path.join(L1ProcROOT, 'merge_recon.txt'),
    }

tdBin = 10

ingestor = {
    'digiTdMon': '/afs/slac.stanford.edu/g/glast/ground/bin/ingestDigiTrending',
    'reconTdMon': '/afs/slac.stanford.edu/g/glast/ground/bin/ingestRecoTrending',
    }

joiner = '*'

rootPath = os.path.join(rootSys, 'lib')
pythonPath = rootPath
libraryPath = ':'.join((os.path.join(L1Cmt, 'lib'), \
                        os.path.join(glastLocation, 'lib'), \
                        rootPath))

# LSF stuff
# allocationGroup = 'glastdata' # don't use this anymore, policies have changed
# allocationGroup="%(allocationGroup)s" # ripped from XML template
#
quickQueue = 'express'
reconQueue = 'medium'
#standardQueue = 'glastdataq'
standardQueue = 'long'
slowQueue = 'xlong'
#
reconMergeScratch = " -R &quot;select[scratch&gt;70]&quot; "

if __name__ == "__main__":
    print L1Dir
    print reconApp
    
