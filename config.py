"""@brief Configuration.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
from os import path, environ

L1Version = "0.82"
installRoot = "/afs/slac.stanford.edu/g/glast/ground/PipelineConfig/SC/L1Pipeline"
L1ProcROOT = path.join(installRoot, L1Version)
#L1ProcROOT = '/nfs/farm/g/glast/u33/wai/pipeline_tests/svac/L1Pipeline'
#L1ProcROOT = '/nfs/slac/g/svac/focke/cvs/L1Pipeline'
LATCalibRoot = '/afs/slac/g/glast/ground/releases/calibrations'
L1Cmt = path.join(installRoot, 'builds')

#L1Disk = '/nfs/slac/g/svac/focke/L1'
L1Disk = '/nfs/farm/g/glast/u33/wai/pipeline_tests/L1'
L1Dir = path.join(L1Disk, 'rootData')

maxCpu = 1000

maxCrumbSize = 6353
#maxCrumbSize = 250

cmtConfig = 'rh9_gcc32opt'
glastExt = path.join('/afs/slac.stanford.edu/g/glast/ground/GLAST_EXT',
                     cmtConfig)
#
releaseDir = '/afs/slac.stanford.edu/g/glast/ground/releases/volume07'
glastVersion = 'v6r070329p29em1'
#glastVersion = 'v7r0913p10'
releaseName = 'EngineeringModel'
gleamPackage = 'LatIntegration'
#
glastName = '-'.join((releaseName, glastVersion))
glastLocation = path.join(releaseDir, glastName)
gleam = path.join(glastLocation, 'bin', gleamPackage)
cmtScript = path.join(glastLocation, releaseName, glastVersion, 'cmt',
                         'setup.sh') # do we need this?
cmtPath = ':'.join((glastLocation, L1Cmt))
environ['CMTPATH'] = cmtPath
environ['CMTCONFIG'] = cmtConfig
#
digiApp = gleam
reconApp = gleam
#
digiOptions = path.join(L1ProcROOT, 'digi.jobOpt')
reconOptions = path.join(L1ProcROOT, 'recon.jobOpt')

rootSys = path.join(glastExt, 'ROOT/v4.02.00/root')
haddRootSys = path.join(glastExt, 'ROOT/v5.10.00/root')
hadd = path.join(glastExt, haddRootSys, 'bin', 'hadd')

testReportVersion = 'v3r6p36'
testReportDir = path.join(L1Cmt, 'TestReport', testReportVersion)
testReportCmt = path.join(testReportDir, 'cmt', 'setup.sh')
testReportApp = path.join(testReportDir, cmtConfig, 'TestReport.exe')
reportMergeApp = path.join(testReportDir, cmtConfig, 'MergeHistFiles.exe')
#
digiMonCmt = testReportCmt
digiMonApp = testReportApp
digiMonVersion = testReportVersion
#
reconMonCmt = testReportCmt
reconMonApp = testReportApp
reconMonVersion = testReportVersion

svacTupleVersion = 'v3r0p3'
svacTupleDir = path.join(L1Cmt, 'EngineeringModelRoot', svacTupleVersion)
svacTupleCmt = path.join(svacTupleDir, 'cmt', 'setup.sh')
svacTupleApp = path.join(svacTupleDir, cmtConfig, 'RunRootAnalyzer.exe')

ST="/nfs/farm/g/glast/u09/builds/rh9_gcc32opt/ScienceTools/ScienceTools-v7r6p1"
PFILES="."

joiner = '*'

rootPath = os.path.join(rootSys, 'lib')
pythonPath = rootPath
libraryPath = ':'.join((os.path.join(glastLocation, 'lib'), \
                        rootPath))

# LSF stuff
allocationGroup = 'glastdata'
#
quickQueue = 'express'
reconQueue = 'long'
standardQueue = 'glastdataq'

if __name__ == "__main__":
    print L1Dir
    print reconApp
    
