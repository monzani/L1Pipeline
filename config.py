#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Configuration.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

L1Name = os.environ.get('L1_TASK_NAME') or "L1Proc"
L1Version = os.environ.get('PIPELINE_TASKVERSION') or os.environ.get('L1_TASK_VERSION') or "1.48"
fullTaskName = '-'.join([L1Name, L1Version])
installRoot = os.environ.get('L1_INSTALL_DIR') or "/afs/slac.stanford.edu/g/glast/ground/PipelineConfig/Level1"

#L1Cmt = os.path.join(installRoot, 'builds')
L1CmtBase = os.environ.get('L1_BUILD_DIR') or '/afs/slac/g/glast/ground/releases/volume03/L1Proc'
L1Cmt = os.path.join(L1CmtBase, L1Version)

doCleanup = True

mode = False
if not mode:
    try:
        mode = os.environ['PIPELINE_MODE']
    except KeyError:
        print >> sys.stderr, 'PIPELINE_MODE not set.'
        pass
    pass
if not mode:
    try:
        pfa = os.environ['PIPELINE_FROMADDRESS']
        mode = pfa.split('@')[0].split('-')[1]
    except KeyError:
        print >> sys.stderr, 'PIPELINE_FROMADDRESS not set.'
        pass
    pass
if not mode:
    mode = 'dev'
    pass
mode = mode.lower()
if mode in ['prod']:
    testMode = False
else:
    testMode = True
    pass
print >> sys.stderr, "Test mode: %s" % testMode

L1ProcROOT = os.path.join(installRoot, L1Version)
L1Xml = os.path.join(L1ProcROOT, 'xml')
L1Data = os.path.join(L1ProcROOT, 'data')

LATCalibRoot = '/afs/slac/g/glast/ground/releases/calibrations/'

calibFlavors = { # not using this now, have separate JO files for LPA & MC
    'LPA': {
        'Acd': 'vanilla',
        'Cal': 'vanilla',
        'Tkr': 'vanilla',
        },
    'MC': {
        'Acd': 'MC_OktoberFest07-L1Proc-recon',
        'Cal': 'MC_OktoberFest07',
        'Tkr': 'MC_OktoberFest07',
        }
    }


L1Disk = '/nfs/farm/g/glast/u52/L1'
L1Dir = os.path.join(L1Disk, 'rootData')

dataCatDir = '/Data/IandT/Level1'

xrootGlast = 'root://glast-rdr.slac.stanford.edu//glast'
xrootSubDir = '%s/%s/%s' % (dataCatDir, mode, L1Version)
xrootBase = xrootGlast + xrootSubDir

if testMode: L1Dir = os.path.join(L1Dir, 'test')

stageDisks = [ # staging buffers with integer weights
    ("/afs/slac/g/glast/ground/PipelineStaging", 1),
    ("/afs/slac/g/glast/ground/PipelineStaging2", 1),
    ("/afs/slac/g/glast/ground/PipelineStaging3", 1),
    ("/afs/slac/g/glast/ground/PipelineStaging4", 1),
    ("/afs/slac/g/glast/ground/PipelineStaging5", 1),
    ]
stageBase = 'l1Stage'
#stageDirs = [os.path.join(disk, stageBase) for disk in stageDisks]

#maxCrumbSize = 48000 # SVAC pipeline uses this
#maxCrumbSize = 250   # tiny
#maxCrumbSize = 6353   # ~.5Hr on tori (muons).  Also about half of (old) medium q limit
#maxCrumbSize = 17000   # ~.5Hr on cob (skymodel).
minCrumbCpuf = 7
maxCrumbs = 7 # Maximum number of crumbs/chunk. Not used by current algorithm.
crumbSize = 5000 # typical crumb size
crumbMmr = 2.0 # largestCrumb / smallestCrumb

defaultRunStatus = 'WAITING'
defaultDataSource = 'LPA'

runSubTask = {
    'LCI': 'doLci',
    'LPA': 'doRun',
    'MC': 'doRun',
    }
chunkSubTask = {
    'LCI': 'doChunkLci',
    'LPA': 'doChunk',
    'MC': 'doChunk',
    }
cleanupSubTask = {
    'LCI': 'cleanupCompleteRunLci',
    'LPA': 'cleanupCompleteRun',
    'MC': 'cleanupCompleteRun',
    }


glastRoot = '/afs/slac.stanford.edu/g/glast'
groundRoot = os.path.join(glastRoot, 'ground')
glastSetup = os.path.join(groundRoot, 'scripts', 'group.sh')
glastSetupCsh = os.path.join(groundRoot, 'scripts', 'group.cshrc')
#
cmtConfig = 'rh9_gcc32opt'
installArea = os.path.join(L1Cmt, 'InstallArea', cmtConfig)
installBin = os.path.join(installArea, 'bin')
#
glastExt = os.path.join(groundRoot, 'GLAST_EXT', cmtConfig)
#
releaseDir = os.path.join(groundRoot, 'releases', 'volume12')
glastVersion = 'v13r11p6'
releaseName = 'GlastRelease'
gleamPackage = 'Gleam'
#
glastName = '-'.join((releaseName, glastVersion))
glastLocation = os.path.join(releaseDir, glastName)
gleam = os.path.join(glastLocation, 'bin', gleamPackage)
cmtScript = os.path.join(
    glastLocation,
    releaseName,
    glastVersion,
    'cmt',
    'setup.sh',
    ) # do we need this?
#
digiOptions = {
    'LCI': os.path.join(L1Data, 'digi.jobOpt'),
    'LPA': os.path.join(L1Data, 'digi.jobOpt'),
    'MC': os.path.join(L1Data, 'digi.jobOpt.mc'),
    }
reconOptions = {
    'LPA': os.path.join(L1Data, 'recon.jobOpt'),
    'MC': os.path.join(L1Data, 'recon.jobOpt.mc'),
}

rootSys = os.path.join(glastExt, 'ROOT/v5.16.00-gl1/root')
haddRootSys = rootSys
hadd = os.path.join(glastExt, haddRootSys, 'bin', 'hadd')


isoc = '/afs/slac/g/glast/isoc/flightOps'
#isocPlatform = os.popen(os.path.join(isoc, 'isoc-platform')).readline().strip()
isocPlatform = 'rhel3_gcc32'
isocBin = os.path.join(isoc, isocPlatform, 'ISOC_PROD', 'bin')

isocScript = os.path.join(isocBin, 'isoc')
isocEnv = 'eval `%s isoc_env --add-env=flightops --add-env=root`' % isocScript

stVersion = 'v9r5'
ST="/nfs/farm/g/glast/u30/builds/rh9_gcc32opt/ScienceTools/ScienceTools-%s" % stVersion
#ST = os.path.join(L1Cmt, "ScienceTools", "ScienceTools-%s" % stVersion)
stSetup = os.path.join(ST, 'ScienceTools', stVersion, 'cmt', 'setup.sh')
PFILES = ".;"
stBinDir = os.path.join(ST, 'bin')
#aspLauncher = '/nfs/farm/g/glast/u33/ASP/ASP/AspLauncher/v1/rh9_gcc32/aspLauncher.sh'
aspLauncher = '/bin/true'

cmtPath = ':'.join((L1Cmt, glastLocation, glastExt, ST))

cmtPackages = {
    'Common': {
        'repository': 'dataMonitoring',
        'version': 'v3r0p13',
        },
    'EngineeringModelRoot': {
        'repository': 'svac',
        'version': 'v3r14',
        },
    'evtClassDefs': {
        'repository': '',
        'version': 'v0r2',
        },
    'FastMon': {
        'repository': 'dataMonitoring',
        'version': 'v3r0p13',
        },
    'ft2Util': {
        'repository': '',
        'version': 'v1r1p44',
        },
    'GPLtools': {
        'repository': '',
        'version': 'v1r10',
        },
    'Monitor': {
        'repository': 'svac',
        'version': 'v1r0p13',
        },
    'pipelineDatasets': {
        'repository': 'users/richard',
        'version': 'v0r4',
        },
    'TestReport': {
        'repository': 'svac',
        'version': 'v5r8',
        },
    }

cvsPackages = {
    'AlarmsCfg': {
        'repository': 'dataMonitoring',
        'version': 'v1r0p4',
        },
    'DigiReconCalMeritCfg': {
        'repository': 'dataMonitoring',
        'version': 'v1r0p15',
        },
    'FastMonCfg': {
        'repository': 'dataMonitoring',
        'version': 'v1r0p10',
        },
    'IGRF': {
        'repository': 'dataMonitoring',
        'version': 'v1r0p1',
        },
    }

packages = dict(cmtPackages)
packages.update(cvsPackages)

# fill in standard values for standard packages
for packName in packages:
    package = packages[packName]
    package['root'] = os.path.join(
        L1Cmt, package['repository'], packName, package['version'])
    package['bin'] = os.path.join(package['root'], cmtConfig)
    package['cmtDir'] = os.path.join(package['root'], 'cmt')
    package['setup'] = os.path.join(package['cmtDir'], 'setup.sh')
    package['checkOutName'] = os.path.join(package['repository'], packName)
    continue

# add nonstandard package info
packages['Common']['python'] = os.path.join(
    packages['Common']['root'], 'python')

packages['EngineeringModelRoot']['app'] = os.path.join(
    packages['EngineeringModelRoot']['bin'], 'RunRootAnalyzer.exe')

packages['evtClassDefs']['data'] = os.path.join(
    packages['evtClassDefs']['root'], 'data')
packages['evtClassDefs']['python'] = os.path.join(
    packages['evtClassDefs']['root'], 'python')

packages['ft2Util']['app'] = os.path.join(
    packages['ft2Util']['bin'], 'makeFT2Entries.exe')

packages['FastMon']['python'] = os.path.join(
    packages['FastMon']['root'], 'python')
packages['FastMon']['app'] = os.path.join(
    packages['FastMon']['python'], 'pDataProcessor.py')
packages['FastMon']['configDir'] = os.path.join(
        packages['FastMonCfg']['root'], 'xml')
packages['FastMon']['env'] = {
    'XML_CONFIG_DIR': packages['FastMon']['configDir']
    }
packages['FastMon']['extraSetup'] = isocEnv

packages['GPLtools']['python'] = os.path.join(
    packages['GPLtools']['root'], 'python')

packages['IGRF']['python'] = os.path.join(packages['IGRF']['root'], 'python')

packages['Monitor']['app'] = os.path.join(
    packages['Monitor']['bin'], 'runStrip_t.exe')
packages['Monitor']['trendMerge'] = os.path.join(
    packages['Monitor']['bin'], 'treemerge.exe')
packages['Monitor']['mergeApp'] = os.path.join(
    packages['Monitor']['bin'], 'MergeHistFiles.exe')

apps = {
    'acdPlots': os.path.join(
        packages['Monitor']['bin'], 'MakeACDNicePlots.exe'),
    'alarmHandler': os.path.join(
        packages['Common']['python'], 'pAlarmHandler.py'),
    'compareDFm': os.path.join(
        packages['Common']['python'], 'pRootDiffer.py'),
    'digi': gleam,
    'digiEor': packages['Monitor']['app'],
    'errorMerger': os.path.join(L1ProcROOT, 'errorParser.py'),
    'fastMonHist': os.path.join(
        packages['FastMon']['python'], 'pFastMonTreeProcessor.py'),
    'fastMonTuple': packages['FastMon']['app'],
    'fastMon': packages['FastMon']['app'],
    'makeFT1': os.path.join(stBinDir, 'makeFT1'),
    'makeFT2': packages['ft2Util']['app'],
    'makeLS3': os.path.join(stBinDir, 'gtltcube'),
    'mergeFT2': os.path.join(
        packages['ft2Util']['bin'], 'mergeFT2Entries.exe'),
    'recon': gleam,
    'reportMerge': packages['Monitor']['mergeApp'],
    'svacTuple': packages['EngineeringModelRoot']['app'],
    'trendMerge': packages['Monitor']['trendMerge'],
    'runVerify': os.path.join(
        packages['TestReport']['bin'], 'RunVerify.exe'),
    }


monitorOptions = {
    'calEor': os.path.join(
        packages['DigiReconCalMeritCfg']['root'],
        'monconfig_digi_long_histos.xml'),
    'calTrend': os.path.join(
        packages['DigiReconCalMeritCfg']['root'],
        'monconfig_digi_long_trending.xml'),
    'digiEor': os.path.join(
        packages['DigiReconCalMeritCfg']['root'],
        'monconfig_digi_histos.xml'),
    'digiTrend': os.path.join(
        packages['DigiReconCalMeritCfg']['root'],
        'monconfig_digi_trending.xml'),
    'fastMon': os.path.join(
        packages['FastMon']['configDir'],
        'config.xml'),
    'fastMonLci': os.path.join(
        packages['FastMon']['configDir'],
        'configLCI.xml'),
    'fastMonTrend': os.path.join(
        packages['DigiReconCalMeritCfg']['root'],
        'monconfig_fastmon_trending.xml'),
    'meritEor': os.path.join(
        packages['DigiReconCalMeritCfg']['root'],
        'monconfig_merit_histos.xml'),
    'meritTrend': os.path.join(
        packages['DigiReconCalMeritCfg']['root'],
        'monconfig_merit_trending.xml'),
    'reconEor': os.path.join(
        packages['DigiReconCalMeritCfg']['root'],
        'monconfig_recon_histos.xml'),
    'reconTrend': os.path.join(
        packages['DigiReconCalMeritCfg']['root'],
        'monconfig_recon_trending.xml'),
    }

mergeConfigs = {
    'calEor': os.path.join(
        packages['DigiReconCalMeritCfg']['root'], 'MergeHistos_digi_long.txt'),
    'digiEor': os.path.join(
        packages['DigiReconCalMeritCfg']['root'], 'MergeHistos_digi.txt'),
    'fastMonHist': os.path.join(
        packages['FastMonCfg']['root'], 'xml', 'MergeHistos_FastMon.txt'),
    'meritEor': os.path.join(
        packages['DigiReconCalMeritCfg']['root'], 'MergeHistos_merit.txt'),
    'reconEor': os.path.join(
        packages['DigiReconCalMeritCfg']['root'], 'MergeHistos_recon.txt'),
    }

alarmConfigs = {
    'digiEor': os.path.join(
        packages['AlarmsCfg']['root'], 'xml', 'digi_eor_alarms.xml'),
    'digiTrend': os.path.join(
        packages['AlarmsCfg']['root'], 'xml', 'digi_trend_alarms.xml'),
    'fastMonHist': os.path.join(
        packages['AlarmsCfg']['root'], 'xml', 'fastmon_eor_alarms.xml'),
    'fastMonTrend': os.path.join(
        packages['AlarmsCfg']['root'], 'xml', 'fastmon_trend_alarms.xml'),
    'reconEor': os.path.join(
        packages['AlarmsCfg']['root'], 'xml', 'recon_eor_alarms.xml'),
    'reconTrend': os.path.join(
        packages['AlarmsCfg']['root'], 'xml', 'recon_trend_alarms.xml'),
    }

alarmExceptions = {
    'digiEor': os.path.join(
        packages['AlarmsCfg']['root'], 'xml',
        'digi_eor_alarms_exceptions.xml'),
    'digiTrend': os.path.join(
        packages['AlarmsCfg']['root'], 'xml',
        'digi_trend_alarms_exceptions.xml'),
    'fastMonHist': os.path.join(
        packages['AlarmsCfg']['root'], 'xml',
        'fastmon_eor_alarms_exceptions.xml'),
    'fastMonTrend': os.path.join(
        packages['AlarmsCfg']['root'], 'xml',
        'fastmon_trend_alarms_exceptions.xml'),
    'reconEor': os.path.join(
        packages['AlarmsCfg']['root'], 'xml',
        'recon_eor_alarms_exceptions.xml'),
    'reconTrend': os.path.join(
        packages['AlarmsCfg']['root'], 'xml',
        'recon_trend_alarms_exceptions.xml'),
    }

tdBin = {
    'calEor': 30000000,
    'calTrend': 300,
    'digiEor': 15,
    'digiTrend': 15,
    'fastMonTrend': 15,
    'meritEor': 15,
    'meritTrend': 15,
    'reconEor': 15,
    'reconTrend': 15,
    }


#ft1Cuts = 'DEFAULT'
ft1Cuts = os.path.join(packages['evtClassDefs']['data'], 'pass5_cuts')
ft1Classifier = 'Pass5_Classifier'
ft1Dicts = {
    'ft1': os.path.join(packages['evtClassDefs']['data'], 'FT1variables'),
    'ls1': os.path.join(packages['evtClassDefs']['data'], 'LS1variables'),
    }


ft2Pad = 1.0


if testMode:
    trendMode = 'dev'
else:
    trendMode = 'prod'
    pass
trendIngestor = '/afs/slac.stanford.edu/g/glast/ground/dataQualityMonitoring/%s/bin/ingestTrendingFile' % trendMode

rootPath = os.path.join(rootSys, 'lib')
xercesPath = os.path.join(glastExt, 'xerces/2.7.0/lib')
mysqlPath = os.path.join(glastExt, 'MYSQL/4.1.18/lib/mysql')
clhepPath = os.path.join(glastExt, 'CLHEP/1.9.2.2/lib')
cppunitPath = os.path.join(glastExt, 'cppunit/1.10.2/lib')
gaudiPath = os.path.join(glastExt, 'gaudi/v18r1-gl4/lib')
oraclePath = '/afs/slac/package/oracle/new/lib'

libraryPath = ':'.join(
    [os.path.join(L1Cmt, 'lib'), 
     os.path.join(glastLocation, 'lib'), 
     rootPath, clhepPath, cppunitPath, oraclePath,
     xercesPath,
     gaudiPath,
     mysqlPath])

# #GPL2 = '/nfs/slac/g/svac/focke/builds/GPLtools/dev'
# gplBase = '/afs/slac.stanford.edu/g/glast/ground/PipelineConfig/GPLtools'
# if testMode:
#     gplType = 'L1test'
# else:
#     gplType = 'L1prod'
#     pass
# # gplType = 'L1prod'
# GPL2 = os.path.join(gplBase, gplType)
# gplPath = os.path.join(GPL2, 'python')
GPL2 = packages['GPLtools']['root']

ppComponents = [
    L1ProcROOT,
    rootPath,
    packages['GPLtools']['python'],
    packages['Common']['python'],
    packages['IGRF']['python']
    ]
pythonPath = ':'.join(ppComponents)
sys.path.extend(ppComponents)

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
# expressQ = 'express'
# mediumQ = 'medium'
# shortQ = 'short'
# longQ = 'long'
expressQ = 'glastdataq'
mediumQ = 'glastdataq'
shortQ = 'glastdataq'
longQ = 'glastdataq'
#
highPriority = 75
#
reconMergeScratch = " -R &quot;select[scratch&gt;70]&quot; "
reconCrumbCpuf = " -R &quot;select[cpuf&gt;%s]&quot; " % minCrumbCpuf

# default option for stageFiles.stageSet.finish()
finishOption = ''

python = sys.executable


os.environ['CMTCONFIG'] = cmtConfig
os.environ['CMTPATH'] = cmtPath
os.environ['GLAST_EXT'] = glastExt
os.environ['GPL2'] = GPL2
os.environ['LATCalibRoot'] = LATCalibRoot
os.environ['MALLOC_CHECK_'] = '0'
os.environ['PFILES'] = PFILES
os.environ['PYTHONPATH'] = pythonPath
os.environ['ROOTSYS'] = rootSys


if __name__ == "__main__":
    print L1ProcROOT
