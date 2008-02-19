#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Configuration.

@author W. Focke <focke@slac.stanford.edu>
"""

L1Version = "1.34"
doCleanup = True

import os
import sys

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

installRoot = os.environ.get('L1_INSTALL_DIR') or "/afs/slac.stanford.edu/g/glast/ground/PipelineConfig/SC/L1Pipeline"
L1ProcROOT = os.path.join(installRoot, L1Version)
L1Xml = os.path.join(L1ProcROOT, 'xml')

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

L1Cmt = os.path.join(installRoot, 'builds')

L1Disk = '/nfs/farm/g/glast/u52/L1'
L1Dir = os.path.join(L1Disk, 'rootData')

dataCatDir = '/Data/OpsSim2/Level1'

xrootGlast = 'root://glast-rdr.slac.stanford.edu//glast'
xrootSubDir = '%s/%s/%s' % (dataCatDir, mode, L1Version)
xrootBase = xrootGlast + xrootSubDir

if testMode: L1Dir = os.path.join(L1Dir, 'test')

stageDisks = ["/afs/slac/g/glast/ground/PipelineStaging",
              "/afs/slac/g/glast/ground/PipelineStaging2"]
stageBase = 'l1Stage'
stageDirs = [os.path.join(disk, stageBase) for disk in stageDisks]

#maxCrumbSize = 48000 # SVAC pipeline uses this
#maxCrumbSize = 250   # tiny
#maxCrumbSize = 6353   # ~.5Hr on tori (muons).  Also about half of (old) medium q limit
maxCrumbSize = 17000   # ~.5Hr on cob (skymodel).
minCrumbCpuf = 7

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
#
cmtConfig = 'rh9_gcc32opt'
installArea = os.path.join(L1Cmt, 'InstallArea', cmtConfig)
installBin = os.path.join(installArea, 'bin')
#
glastExt = os.path.join(groundRoot, 'GLAST_EXT', cmtConfig)
#
releaseDir = os.path.join(groundRoot, 'releases', 'volume12')
glastVersion = 'v13r11p1'
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
    'LPA': os.path.join(L1ProcROOT, 'digi.jobOpt'),
    'MC': os.path.join(L1ProcROOT, 'digi.jobOpt.mc'),
    }
reconOptions = {
    'LPA': os.path.join(L1ProcROOT, 'recon.jobOpt'),
    'MC': os.path.join(L1ProcROOT, 'recon.jobOpt.mc'),
}

rootSys = os.path.join(glastExt, 'ROOT/v5.16.00-gl1/root')
haddRootSys = rootSys
hadd = os.path.join(glastExt, haddRootSys, 'bin', 'hadd')


isoc = '/afs/slac/g/glast/isoc/flightOps'
isocPlatform = os.popen(os.path.join(isoc, 'isoc-platform')).readline().strip()
isocBin = os.path.join(isoc, isocPlatform, 'ISOC_PROD', 'bin')

# ISOC logger
scid = 99
#netLoggerFlight = 'x-netlog://glastlnx06.slac.stanford.edu:15502'
netLoggerFlight = None
#netloggerIAndT = 'x-netlog://glastlnx06.slac.stanford.edu:15501'
netLoggerTest = 'x-netlog://glastlnx25.slac.stanford.edu:15502'
if testMode:
    netloggerDest = netLoggerTest
else:
    netloggerDest = netLoggerFlight
    pass
netloggerLevel = 'info'

stVersion = 'v9r4p1'
ST="/nfs/farm/g/glast/u30/builds/rh9_gcc32opt/ScienceTools/ScienceTools-%s" % stVersion
stSetup = os.path.join(ST, 'ScienceTools', stVersion, 'cmt', 'setup.sh')
PFILES = ".;"
stBinDir = os.path.join(ST, 'bin')

cmtPath = ':'.join((L1Cmt, glastLocation, glastExt, ST))

packages = {
    'Common': {
        'repository': 'dataMonitoring',
        'version': 'v2r10p0',
        },
    'FastMon': {
        'repository': 'dataMonitoring',
        'version': 'v2r8p0',
        },
    'Monitor': {
        'repository': 'svac',
        'version': 'dp20080207_v2',
        },
    'EngineeringModelRoot': {
        'repository': 'svac',
        'version': 'v3r10p1',
        },
    'TestReport': {
        'repository': 'svac',
        'version': 'v5r0',
        },
    'pipelineDatasets': {
        'repository': 'users/richard',
        'version': 'v0r4',
        },
    'ft2Util': {
        'repository': '',
        'version': 'v1r1p35',
        },
    }

# fill in standard values for standard packages
for packName in packages:
    package = packages[packName]
    packages[packName]['root'] = os.path.join(
        L1Cmt, packName, package['version'])
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

packages['ft2Util']['app'] = os.path.join(
    packages['ft2Util']['bin'], 'makeFT2Entries.exe')

packages['FastMon']['app'] = os.path.join(
    packages['FastMon']['root'], 'python', 'pDataProcessor.py')
packages['FastMon']['env'] = {
    'XML_CONFIG_DIR': os.path.join(packages['FastMon']['root'], 'xml'),
    }
packages['FastMon']['extraSetup'] = 'eval `/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/isoc isoc_env --add-env=flightops --add-env=root`'

packages['Monitor']['app'] = os.path.join(
    packages['Monitor']['bin'], 'runStrip_t.exe')
packages['Monitor']['configDir'] = os.path.join(
    packages['Monitor']['root'], 'src')
packages['Monitor']['trendMerge'] = os.path.join(
    packages['Monitor']['bin'], 'treemerge.exe')
packages['Monitor']['mergeApp'] = os.path.join(
    packages['Monitor']['bin'], 'MergeHistFiles.exe')



apps = {
    'alarmHandler': os.path.join(
        packages['Common']['python'], 'pAlarmHandler.py'),
    'digi': gleam,
    'digiEor': packages['Monitor']['app'],
    'errorMerger': os.path.join(L1ProcROOT, 'errorParser.py'),
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
        packages['Monitor']['configDir'], 'monconfig_digi_CalLongTime_v2_histos.xml'),
    'calTrend': os.path.join(
        packages['Monitor']['configDir'], 'monconfig_digi_CalLongTime_v2_Trending.xml'),
    'digiEor': os.path.join(
        packages['Monitor']['configDir'], 'monconfig_digi_v27_histos.xml'),
    'digiTrend': os.path.join(
        packages['Monitor']['configDir'], 'monconfig_digi_v27_trending.xml'),
    'reconEor': os.path.join(
        packages['Monitor']['configDir'], 'monconfig_recon_v5_histos.xml'),
    'reconTrend': os.path.join(
        packages['Monitor']['configDir'], 'monconfig_recon_v5_trending.xml'),
    }

mergeConfigs = {
    'calEor': os.path.join(
        packages['Monitor']['configDir'], 'MergeHistos_digi_CalLongTime_v2.txt'),
    'digiEor': os.path.join(
        packages['Monitor']['configDir'], 'MergeHistos_digi_v27.txt'),
    'fastMonHist': os.path.join(
        L1ProcROOT, 'MergeHistos_FastMon.txt'),
    'reconEor': os.path.join(
        packages['Monitor']['configDir'], 'MergeHistos_recon_v5.txt'),
    }

alarmConfigs = {
    'digiEor': os.path.join(
        packages['Common']['root'], 'xml', 'digi_eor_alarms.xml'),
    'fastMonHist': os.path.join(
        packages['Common']['root'], 'xml', 'fastmon_eor_alarms.xml'),
    'reconEor': os.path.join(
        packages['Common']['root'], 'xml', 'recon_eor_alarms.xml'),
    }

tdBin = {
    'calEor': 30000000,
    'calTrend': 300,
    'digiEor': 15,
    'digiTrend': 15,
    'reconEor': 15,
    'reconTrend': 15,
    }

trendIngestor = '/afs/slac.stanford.edu/g/glast/ground/dataQualityMonitoring/bin/ingestTrendingFile'

rootPath = os.path.join(rootSys, 'lib')
#xercesPath = ':'.join([glastExt, 'xerces/2.7.0/lib'])
#mysqlPath = ':'.join([glastExt, 'MYSQL/4.1.18/lib/mysql'])
clhepPath = os.path.join(glastExt, 'CLHEP/1.9.2.2/lib')
cppunitPath = os.path.join(glastExt, 'cppunit/1.10.2/lib')
oraclePath = '/afs/slac/package/oracle/new/lib'

libraryPath = ':'.join(
    (os.path.join(L1Cmt, 'lib'), 
     os.path.join(glastLocation, 'lib'), 
     rootPath, clhepPath, cppunitPath, oraclePath))

#GPL2 = '/nfs/slac/g/svac/focke/builds/GPLtools/dev'
gplBase = '/afs/slac.stanford.edu/g/glast/ground/PipelineConfig/GPLtools'
if testMode:
    gplType = 'L1test'
else:
    gplType = 'L1prod'
    pass
# gplType = 'L1prod'
GPL2 = os.path.join(gplBase, gplType)
gplPath = os.path.join(GPL2, 'python')

ppComponents = [L1ProcROOT, rootPath, gplPath, packages['Common']['python']]
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
