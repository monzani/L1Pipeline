#!/sdf/data/fermi/a/isoc/flightOps/rhel6_gcc44/ISOC_PROD/bin/shisoc python2.6

"""@brief Configuration.

@author W. Focke <focke@slac.stanford.edu>, M.E. Monzani <monzani@slac.stanford.edu>
"""

import os
import sys

L1Name = os.environ.get('L1_TASK_NAME') or "L1Proc"
L1Version = os.environ.get('PIPELINE_TASKVERSION') or os.environ.get('L1_TASK_VERSION') or "6.0"
fullTaskName = '-'.join([L1Name, L1Version])
installRoot = os.environ.get('L1_INSTALL_DIR') or "/sdf/group/fermi/ground/PipelineConfig/L1Proc"

creator = '-'.join([L1Name, L1Version])
    
L1BuildBase = os.environ.get('L1_BUILD_DIR') or "/sdf/group/fermi/ground/PipelineBuilds/L1Proc"
L1Build = os.path.join(L1BuildBase, L1Version)

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

LATCalibRoot = '/sdf/group/fermi/ground/releases/calibrations/'

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


L1Output = '/sdf/data/fermi/ground/PipelineOutput/L1'
if testMode: L1Output += 'Test'

dlStorage = os.path.join(L1Output, 'deliveries')
saveDl = True

logRoot = '/sdf/data/fermi/ground/PipelineOutput/L1/logs'

# normal
dataCatBase = '/Data/Flight/Level1'
dataSource = os.environ.get('DATASOURCE', 'LPA')
dataCatDir = '/'.join([dataCatBase, dataSource])
dataCatDir = os.environ.get('dataCatDir', dataCatDir)
# reprocess
#dataCatDir = '/Data/Flight/Reprocess/P100'
#dataCatBase = dataCatDir

xrootGlast = 'root://glast-rdr.slac.stanford.edu//glast'
xrootSubDir = '%s/%s/%s' % (dataCatDir, mode, L1Version)
xrootBase = xrootGlast + xrootSubDir

# optional override for versions looked up from datacat
# actual version will be max of the normal version and this. 
baseVersion = 0

#throttle parameters
throttleDir =  os.path.join(L1Output, 'throttle')
throttleLimit = 6

if testMode:
    stageBase = 'l1Test'
else:
    stageBase = 'l1Stage'
    pass

xrootStage = os.path.join(xrootGlast, 'Scratch', stageBase)

maxCrumbs = 25 # Maximum number of crumbs/chunk.
crumbSize = 1500 # minimum average crumb size (chunkEvents/nCrumbs)
crumbMmr = 1.3 # largestCrumb / smallestCrumb

maxChunks = 1000 # We can't handle too many chunks. Fail if more.

defaultRunStatus = 'WAITING'
defaultDataSource = 'LPA'
defaultMootKey = '0'
defaultMootAlias = 'None'

runSubTask = {
    'COMPLETE': {
        'LCI': 'doLci',
        'LPA': 'doRun',
        'MC': 'doRun',
        },
    'INCOMPLETE': {
        'LCI': 'doIncLci',
        'LPA': 'doInc',
        'MC': 'doInc',
        },
    'WAITING': {
        'LCI': 'doLci',
        'LPA': 'doRun',
        'MC': 'doRun',
        },
    }
runSubTask['INPROGRESS'] = runSubTask['WAITING']

chunkSubTask = {
    'LCI': 'doChunkLci',
    'LPA': 'doChunk',
    'MC': 'doChunk',
    }

cleanupSubTask = {
    'doInc': {
        'LPA': 'cleanupIncompleteRun',
        'MC': 'cleanupIncompleteRun',
        },
    'doIncLci': {
        'LCI': 'cleanupIncompleteRunLci',
        },
    'doLci': {
        'LCI': 'cleanupCompleteRunLci',
        },
    'doRun': {
        'LPA': 'cleanupCompleteRun',
        'MC': 'cleanupCompleteRun',
        },
    }

groundRootNew = '/sdf/group/fermi/ground'
groundRootOld = '/sdf/group/fermi/a/ground'
scons = '/sdf/group/fermi/a/applications/SCons/2.1.0/bin/scons'

#this is for rhel6:
optConfig = 'redhat6-x86_64-64bit-gcc44-Optimized'
glastExt = os.path.join(groundRootOld, 'GLAST_EXT', 'redhat6-x86_64-64bit-gcc44')
releaseDir = os.path.join(groundRootNew, 'PipelineBuilds', 'GlastRelease')
#
glastVersion = '20-10-04-gr07'
releaseName = 'GlastRelease'
#
glastName = '-'.join((releaseName, glastVersion))
glastLocation = os.path.join(releaseDir, glastName) 

grBinDir = os.path.join(glastLocation, 'bin', optConfig)
grExeDir = os.path.join(glastLocation, 'exe', optConfig)
grPath = os.path.join(glastLocation, 'lib', optConfig)
grSetup = os.path.join(grBinDir, '_setup.sh')
gleam = os.path.join(grBinDir,  'Gleam')  ### bin or exe???

digiOptions = {
    'LCI': os.path.join(L1Data, 'digi.jobOpt'),
    'LPA': os.path.join(L1Data, 'digi.jobOpt'),
    'MC': os.path.join(L1Data, 'digi.jobOpt.mc'),
    }
reconOptions = {
    'LPA': os.path.join(L1Data, 'recon.jobOpt'),
    'MC': os.path.join(L1Data, 'recon.jobOpt.mc'),
}

rootSys = os.path.join(glastExt, 'ROOT/v5.34.03-gr01')
haddRootSys = rootSys
hadd = os.path.join(glastExt, haddRootSys, 'bin', 'hadd')

stDir = os.path.join(groundRootNew, 'PipelineBuilds', 'ScienceTools')
stVersion = '11-05-01'
stName = 'ScienceTools'

ST = os.path.join(stDir, "ScienceTools-%s" % stVersion)
PFILES = ".;/dev/null"
stBinDir = os.path.join(ST, 'bin', optConfig)
stExeDir = os.path.join(ST, 'exe', optConfig)
stSetup = os.path.join(stBinDir, '_setup.sh')

l1BinDir = os.path.join(L1Build, 'bin', optConfig)
l1ExeDir = os.path.join(L1Build, 'exe', optConfig)
l1Setup = os.path.join(l1BinDir, '_setup.sh')

isoc = '/sdf/group/fermi/a/isoc/flightOps'
isocPlatform = 'rhel6_gcc44'
isocMode = os.environ.get('isocMode', 'ISOC_PROD')
isocBin = os.path.join(isoc, isocPlatform, isocMode, 'bin')
isocRun = os.path.join(isoc, isocPlatform, '${isocMode}', 'bin', 'isoc run')
python27 = '/sdf/group/fermi/a/ground/GLAST_EXT/redhat6-x86_64-64bit-gcc44/python/2.7.2-gl4/bin/python'

isocScript = os.path.join(isocBin, 'isoc')
isocEnv = 'eval `%s isoc_env --add-env=flightops`' % isocScript
fastCopyOut = '/sdf/group/fermi/ground/FASTCopyOutdir'
fastCopyCfg = os.path.join(fastCopyOut, 'outgoing.ini')

# DB for acqsummary
if mode == 'prod':
    connectString = '/@isocflight'
else:
    # connectString = '/@isocnightly'
    connectString = '/@isocflight'
    pass
acqTable = 'GLASTOPS_ACQSUMMARY'

# parameters for retrying failed DB connections
dbRetries = 5
minDbWait = 30
maxDbWait = 120

scid = 77
hpTaskBase = '/afs/slac/g/glast/isoc/flightOps/offline/halfPipe/prod'

l0Archive = '/sdf/group/fermi/n/u23/ISOC-flight/Archive/level0'

if testMode:
    aspLauncher = '/bin/true'
else:
    aspLauncher = '/afs/slac/g/glast/ground/links/data/ASP/aspLauncher.sh'
    pass
aspAlreadyLaunched = 160

elFt1ProcVer = 305
exFt1ProcVer = 305
exLs1ProcVer = 305
ft1ProcVer = 305
ft2ProcVer = 310
ft2SecondsProcVer = 310
ls1ProcVer = 305

procVer = {
    'electronFT1BadGti': elFt1ProcVer,
    'ft1NoDiffRsp': ft1ProcVer,
    'ls1BadGti': ls1ProcVer,
    }
    
githubMain = 'https://github.com/fermi-lat'

githubPlain = {
    'Common': {
        'version': 'Common-07-00-01',
        },
    'DigiReconCalMeritCfg': {
        'version': 'DigiReconCalMeritCfg-02-01-08',
        },
    'evtClassDefs': {
        'version': 'evtClassDefs-01-01-05',
        },
    'FastMon': {
        'version': 'FastMon-05-03-05',
        },
    'FastMonCfg': {
        'version': 'FastMonCfg-02-02-03',
        },
    'GPLtools': {
        'version': 'GPLtools-03-00-00',
        },
    'IGRF': {
        'version': 'IGRF-03-04-02',
        },
    }

githubSCons = {
    'calibTkrUtil': {
        'version': 'calibTkrUtil-03-00-00',
        },
    'findGaps': {
        'version': 'findGaps-02-03-00',
        },
    'fitsGen': {
        'version': 'fermitools-11-07-01',
        },
    'ft2Util': {
        'version': 'ft2Util-02-05-04',
        },
    'Monitor': {
        'version': 'Monitor-03-14-03',
        },
    'pipelineDatasets': {
        'version': 'pipelineDatasets-01-00-00',
        },
    'TestReport': {
        'version': 'TestReport-12-03-02',
        },
    }

packages = dict(githubPlain)
packages.update(githubSCons)

# fill in standard values for standard packages
for packName in packages:
    package = packages[packName]
    package['root'] = os.path.join(L1Build, packName)
    package['python'] = os.path.join(package['root'], 'python')
    continue

# add nonstandard package info

packages['evtClassDefs']['data'] = os.path.join(
    packages['evtClassDefs']['root'], 'data')

packages['evtClassDefs']['xml'] = os.path.join(
    packages['evtClassDefs']['root'], 'xml')

packages['ft2Util']['app'] = os.path.join(l1ExeDir, 'makeFT2')

packages['FastMon']['app'] = os.path.join(
    packages['FastMon']['python'], 'pDataProcessor.py')
packages['FastMon']['configDir'] = os.path.join(
    packages['FastMonCfg']['root'], 'xml')
packages['FastMon']['env'] = {
    'XML_CONFIG_DIR': packages['FastMon']['configDir']
    }
packages['FastMon']['extraSetup'] = isocEnv
packages['FastMon']['saaDefinition'] = os.path.join(
    packages['FastMon']['configDir'], 'saaDefinition.xml')

packages['Monitor']['app'] = os.path.join(l1ExeDir, 'runStrip_t')
packages['Monitor']['trendMerge'] = os.path.join(l1ExeDir, 'treemerge')
packages['Monitor']['mergeApp'] = os.path.join(l1ExeDir, 'MergeHistFiles')

apps = {
    'acdPedsAnalyzer': os.path.join(
        packages['Common']['python'], 'pAcdPedsAnalyzer.py'),
    'acdPlots': os.path.join(l1ExeDir, 'MakeACDNicePlots'),
    'alarmHandler': os.path.join(
        packages['Common']['python'], 'pAlarmHandler.py'),
    'alarmPostProcessor': os.path.join(
        packages['Common']['python'], 'pAlarmPostProcessor.py'),
    'calGainsAnalyzer': os.path.join(
        packages['Common']['python'], 'pCalGainsAnalyzer.py'),
    'calPedsAnalyzer': os.path.join(
        packages['Common']['python'], 'pCalPedsAnalyzer.py'),
    'compareDFm': os.path.join(
        packages['Common']['python'], 'pRootDiffer.py'),
    'diffRsp': os.path.join(stExeDir, 'gtdiffrsp'),
    'digi': gleam,
    'digiHist': packages['Monitor']['app'],
    'drawOrbit': os.path.join(
        packages['FastMon']['python'], 'drawOrbit2d.py'),
    'errorHandler': os.path.join(
        packages['Common']['python'], 'pErrorLogger.py'),
    'errorMerger': os.path.join(
        packages['FastMon']['python'], 'pXmlErrorMerger.py'),
    'fastMonTuple': packages['FastMon']['app'],
    'fastMonHist': os.path.join(
        packages['FastMon']['python'], 'pFastMonTreeProcessor.py'),
    'fastMonTuple': packages['FastMon']['app'],
    'fastMon': packages['FastMon']['app'],
    'findGaps': os.path.join(l1ExeDir, 'findGaps'),
    'fixGTI': os.path.join(stExeDir, 'gtmktime'),
    'ft1Verify': os.path.join(l1ExeDir, 'ft1Verify'),
    'ft2Verify': os.path.join(l1ExeDir, 'ft2Verify'),
    'gtSelect': os.path.join(stExeDir, 'gtselect'),
    'makeFT1': os.path.join(stExeDir, 'makeFT1'),
    'makeFT2': packages['ft2Util']['app'],
    'mergeFT2': os.path.join(l1ExeDir, 'mergeFT2'),
    'meritVerify': os.path.join(l1ExeDir, 'meritVerify'),
    'recon': gleam,
    'reportMerge': packages['Monitor']['mergeApp'],
    'runVerify': os.path.join(l1ExeDir, 'RunVerify'),
    'solarFlares': os.path.join(
        packages['Common']['python'], 'pBadTimeIntervalLogger.py'),
    'tkrAnalysis': os.path.join(l1ExeDir, 'tkrRootAnalysis'),
    'tkrMerger': os.path.join(
        packages['calibTkrUtil']['python'], 'mergeTkrRootFiles.py'),
    'tkrMonitor': os.path.join(
        packages['calibTkrUtil']['python'], 'tkrMonitor.py'),
    'trendMerge': packages['Monitor']['trendMerge'],
    }


monitorOptions = {
    'calHist': os.path.join(
        packages['DigiReconCalMeritCfg']['root'],
        'monconfig_digi_long_histos.xml'),
    'calTrend': os.path.join(
        packages['DigiReconCalMeritCfg']['root'],
        'monconfig_digi_long_trending.xml'),
    'digiHist': os.path.join(
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
    'meritHist': os.path.join(
        packages['DigiReconCalMeritCfg']['root'],
        'monconfig_merit_histos.xml'),
    'meritTrend': os.path.join(
        packages['DigiReconCalMeritCfg']['root'],
        'monconfig_merit_trending.xml'),
    'tkrTrend': os.path.join(
        packages['DigiReconCalMeritCfg']['root'],
        'monconfig_trackermon_trending.xml'),
    'reconHist': os.path.join(
        packages['DigiReconCalMeritCfg']['root'],
        'monconfig_recon_histos.xml'),
    'reconTrend': os.path.join(
        packages['DigiReconCalMeritCfg']['root'],
        'monconfig_recon_trending.xml'),
    }

mergeConfigs = {
    'calHist': os.path.join(
        packages['DigiReconCalMeritCfg']['root'], 'MergeHistos_digi_long.txt'),
    'digiHist': os.path.join(
        packages['DigiReconCalMeritCfg']['root'], 'MergeHistos_digi.txt'),
    'fastMonHist': os.path.join(
        packages['FastMonCfg']['root'], 'xml', 'MergeHistos_FastMon.txt'),
    'meritHist': os.path.join(
        packages['DigiReconCalMeritCfg']['root'], 'MergeHistos_merit.txt'),
    'reconHist': os.path.join(
        packages['DigiReconCalMeritCfg']['root'], 'MergeHistos_recon.txt'),
    }


alarmBase = os.path.join(groundRootNew, 'PipelineConfig', 'Monitoring')
alarmRefDir = os.path.join(alarmBase, 'ReferHist',  mode)
alarmBase = os.path.join(alarmBase, 'AlarmsCfg', mode)
alarmConfigs = {
    'acdPedsAnalyzer': os.path.join(alarmBase, 'xml', 'acdpeds_eor_alarms.xml'),
    'calGainsAnalyzer': os.path.join(
        alarmBase, 'xml', 'calgains_eor_alarms.xml'),
    'calHist': os.path.join(alarmBase, 'xml', 'calhist_alarms.xml'),
    'calPedsAnalyzer': os.path.join(alarmBase, 'xml', 'calpeds_eor_alarms.xml'),
    'digiHist': os.path.join(alarmBase, 'xml', 'digi_eor_alarms.xml'),
    'digiTrend': os.path.join(alarmBase, 'xml', 'digi_trend_alarms.xml'),
    'fastMonError': os.path.join(alarmBase, 'xml', 'fastmon_errors_alarms.xml'),
    'fastMonHist': os.path.join(alarmBase, 'xml', 'fastmon_eor_alarms.xml'),
    'fastMonTrend': os.path.join(alarmBase, 'xml', 'fastmon_trend_alarms.xml'),
    'meritHist': os.path.join(alarmBase, 'xml', 'merit_eor_alarms.xml'),
    'meritTrend': os.path.join(alarmBase, 'xml', 'merit_trend_alarms.xml'),
    'reconHist': os.path.join(alarmBase, 'xml', 'recon_eor_alarms.xml'),
    'reconTrend': os.path.join(alarmBase, 'xml', 'recon_trend_alarms.xml'),
    'tkrTrend': os.path.join(alarmBase, 'xml', 'trackermon_trend_alarms.xml'),
    'verifyLog': os.path.join(alarmBase, 'xml', 'verify_errors_alarms.xml'),
    'verifyFt2Error': os.path.join(alarmBase, 'xml', 'verify_ft2_errors_alarms.xml'),
    'verifyFt1Error': os.path.join(alarmBase, 'xml', 'verify_ft1_errors_alarms.xml'),
    'verifyMeritError': os.path.join(alarmBase, 'xml', 'verify_merit_errors_alarms.xml'),
    }

alarmExceptions = {
    'acdPedsAnalyzer': os.path.join(
        alarmBase, 'xml', 'acdpeds_eor_alarms_exceptions.xml'),
    'calGainsAnalyzer': os.path.join(
        alarmBase, 'xml', 'calgains_eor_alarms_exceptions.xml'),
    'calHist': os.path.join(
        alarmBase, 'xml', 'calhist_alarms_exceptions.xml'),
    'calPedsAnalyzer': os.path.join(
        alarmBase, 'xml', 'calpeds_eor_alarms_exceptions.xml'),
    'digiHist': os.path.join(
        alarmBase, 'xml', 'digi_eor_alarms_exceptions.xml'),
    'digiTrend': os.path.join(
        alarmBase, 'xml', 'digi_trend_alarms_exceptions.xml'),
    'fastMonHist': os.path.join(
        alarmBase, 'xml', 'fastmon_eor_alarms_exceptions.xml'),
    'fastMonTrend': os.path.join(
        alarmBase, 'xml', 'fastmon_trend_alarms_exceptions.xml'),
    'meritHist': os.path.join(
        alarmBase, 'xml', 'merit_eor_alarms_exceptions.xml'),
    'meritTrend': os.path.join(
        alarmBase, 'xml', 'merit_trend_alarms_exceptions.xml'),
    'reconHist': os.path.join(
        alarmBase, 'xml', 'recon_eor_alarms_exceptions.xml'),
    'reconTrend': os.path.join(
        alarmBase, 'xml', 'recon_trend_alarms_exceptions.xml'),
    'tkrTrend': os.path.join(
        alarmBase, 'xml', 'trackermon_trend_alarms_exceptions.xml'),
    }
alarmPostProcessorConfigs = {
    'reconHistAlarm': os.path.join(
        alarmBase, 'xml', 'recon_eor_alarms_postprocess.xml'),
    }

normalizedRateConfigs = {
    'meritHist': os.path.join(
        packages['DigiReconCalMeritCfg']['root'],
        'FactorsToNormRates_EarthLimb.txt'),
    'meritTrend': os.path.join(
        packages['DigiReconCalMeritCfg']['root'],
        'FactorsToNormRates_EarthLimb.txt'),
    }

tdBin = {
    'calHist': 1000000000,
    'calTrend': 300,
    'digiHist': 15,
    'digiTrend': 15,
    'fastMonTrend': 15,
    'meritHist': 15,
    'meritTrend': 15,
    'reconHist': 15,
    'reconTrend': 15,
    'tkrTrend': 1000000000,
    }


evclData = packages['evtClassDefs']['data']
evclXml = packages['evtClassDefs']['xml']
electronCuts = os.path.join(evclData, 'pass8.3_Electrons_cuts_L1')
extendedCuts = os.path.join(evclData, 'pass8.3_Extended_cuts_L1')
ft1Vars = os.path.join(evclData, 'pass8_FT1variables')
ls1Vars = os.path.join(evclData, 'pass8_LS1variables')
photonClass = 'FT1EventClass'
#electronClass = 'EvtCREventClass'
electronClass = 'FT1EventClass'
#transientCuts = os.path.join(evclData, 'pass7.6_Transient_cuts_L1')
#sourceCuts = os.path.join(evclData, 'pass7.6_Source_cuts_L1')
xmlClassifier =  os.path.join(evclXml, 'EvtClassDefs_P8R3.xml')
filterClassifyMap = {
    'electronMerit': {
        'cutFile': electronCuts,
        },
    'filteredMerit': {
        'cutFile': extendedCuts,
        },
    'electronFT1BadGti': {
        'cutFile': electronCuts,
        'classifier': electronClass,
        'ft1Dict': ft1Vars,
        },
    'ft1NoDiffRsp': {
        'cutFile': extendedCuts,
        'classifier': photonClass,
        'ft1Dict': ft1Vars,
        },
    'ls1BadGti': {
        'cutFile': extendedCuts,
        'classifier': photonClass,
        'ft1Dict': ls1Vars,
        },
    }
gtSelectClass = {
    'ft1': 128,
    'ls1': 65544,
}

verifyOptions = {
    'InProgress': '',
    'Complete': '-c',
    'Incomplete': '-c',
    'Truncation': '100',
    }

ft2Pad = 1.0 # pad time range with this on either end when making fakeFT2
ft2Template = os.path.join(L1Build, 'fitsGen', 'data', 'ft2.tpl')
ft2liveTimeTolerance = '1e-12'

m7Pad = 10 # pad time range with this on either end whan making m7

# not used # ft1Pad = 1.0 # pad time range with this on either end whan making ft1 and ls1
ft1Digits = 1 # round times given to makeFT1 OUT (round start down, end up) to this many digits past the decimal point - i.e. 1 makes numbers like 254760591.0


if testMode:
    trendMode = 'dev'
else:
    trendMode = 'prod'
    pass
trendIngestor = '/sdf/group/fermi/a/ground/dataQualityMonitoring/%s/bin/ingestTrendingFile' % trendMode
runIngestor = '/sdf/group/fermi/a/ground/dataQualityMonitoring/%s/bin/ingestRunFile' % trendMode

rootPath = os.path.join(rootSys, 'lib')
libraryPath = ':'.join(
    [
        os.path.join(L1Build, 'lib', optConfig), 
        rootPath,
        ])

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

# make directories world-writeable when testing
if testMode:
    try:
        import fileOps
        fileOps.dirMode = 0777
    except ImportError:
        pass
    pass
try:
    import stageFiles
    stageFiles.defaultStrictSetup = True
except ImportError:
    pass

# SLURM parameters 
#
jobsite = 'S3DFDATA'
slurm_extras = '--partition milano --account fermi:L1'

# LSF/slurm pre-exec option for run & throttle locking
#lockOption = " -E &quot;${isocRun} ${L1ProcROOT}/lockFile.py&quot; "
lockScript = "${L1ProcROOT}/lockFile.py"

# number of autoretries for processes that do that
defaultRetries = 1
retries = os.environ.get('L1Retries', defaultRetries)

# container settings parameters 
#
container_image = '/sdf/group/fermi/sw/containers/fermi-rhel6.sif'
bind_mounts = '-B /sdf:/sdf -B /sdf/group/fermi/a:/afs/slac/g/glast'
bind_afs_twice = '-B /sdf/group/fermi/a:/afs/slac.stanford.edu/g/glast'
bind_package = '-B /sdf/group/fermi/sw/package:/afs/slac/package'
bind_pkg_twice = '-B /sdf/group/fermi/sw/package:/afs/slac.stanford.edu/package'
bind_TWW_mysql = '-B /sdf/group/fermi/sw/containers/rhel6/opt/TWWfsw:/opt/TWWfsw'
container_volumes = ' '.join([bind_mounts, bind_afs_twice, bind_package, bind_pkg_twice, bind_TWW_mysql])
container_exec = 'singularity exec --env LD_LIBRARY_PATH=${LD_LIBRARY_PATH}'

# default option for stageSet input exclusion filter
excludeIn = None
# default option for stageFiles.stageSet.finish()
finishOption = ''

python = sys.executable

# values for L1RunStatus in run quality table
runningStatus = 'Running'
crashedStatus = 'Failed'
doneStatus = 'Complete'
incompleteStatus = 'Incomplete'
waitingStatus = 'InProgress'

solarFlareFlag = -1

ignoreIgrfBoundary = False
igrfExport = {
    True: 'IGNORE_IGRF_BOUNDARY=yesPlease ; export IGNORE_IGRF_BOUNDARY',
    False: ''
    }[ignoreIgrfBoundary]

astroTools = '/sdf/group/fermi/a/applications/astroTools/astrotools_setup_s3df.sh'

os.environ['GLAST_EXT'] = glastExt
os.environ['GPL2'] = GPL2
os.environ['LATCalibRoot'] = LATCalibRoot
os.environ['MALLOC_CHECK_'] = '0'
os.environ['PFILES'] = PFILES
os.environ['PYTHONPATH'] = pythonPath
os.environ['ROOTSYS'] = rootSys

# Used to distinguish our variable names from the hoi polloi
nameManglingPrefix = 'L1'


if __name__ == "__main__":
    print L1ProcROOT
