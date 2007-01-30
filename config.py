"""@brief Configuration.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
env = os.environ

L1Version = "0.1"
installRoot = "/afs/slac.stanford.edu/g/glast/ground/PipelineConfig/SC/L1Pipeline"
L1ProcROOT = os.path.join(installRoot, L1Version)
L1Cmt = os.path.join(L1ProcROOT, 'builds')

L1Disk = '/nfs/slac/g/svac/focke/L1'
L1Dir = os.path.join(L1Disk, 'rootData')

maxCpu = 1000

maxCrumbSize = 6353

cmtConfig = 'rh9_gcc32opt'
glastExt = os.path.join('/afs/slac.stanford.edu/g/glast/ground/GLAST_EXT',
                        cmtConfig)
#
releaseDir = '/afs/slac.stanford.edu/g/glast/ground/releases/volume07'
glastVersion = 'v6r070329p29em1'
releaseName = 'EngineeringModel'
gleamPackage = 'LatIntegration'
#
glastName = '-'.join((releaseName, glastVersion))
glastLocation = os.path.join(releaseDir, glastName)
gleam = os.path.join(glastLocation, 'bin', gleamPackage)
cmtScript = os.path.join(glastLocation, releaseName, glastVersion, 'cmt',
                         'setup.sh') # do we need this?
cmtPath = ':'.join((glastLocation, L1Cmt))
env['CMTPATH'] = cmtPath
env['CMTCONFIG'] = cmtConfig
#
digiApp = gleam
reconApp = gleam
#
digiOptions = os.path.join(L1ProcROOT, 'digi.jobOpt')
reconOptions = os.path.join(L1ProcROOT, 'recon.jobOpt')

rootSys = os.path.join(glastExt, 'ROOT/v4.02.00/root')
haddRootSys = os.path.join(glastExt, 'ROOT/v5.10.00/root')
hadd = os.path.join(glastExt, haddRootSys, 'bin', 'hadd')

testReportVersion = 'v3r6p33'
testReportDir = os.path.join(L1Cmt, 'TestReport', testReportVersion)
testReportCmt = os.path.join(testReportDir, 'cmt', 'setup.sh')
testReportApp = os.path.join(testReportDir, cmtConfig, 'TestReport.exe')
reportMergeApp = os.path.join(testReportDir, cmtConfig, 'MergeHistFiles.exe')
#
digiMonCmt = testReportCmt
digiMonApp = testReportApp
digiMonVersion = testReportVersion
#
reconMonCmt = testReportCmt
reconMonApp = testReportApp
reconMonVersion = testReportVersion

svacTupleVersion = 'v3r0p3'
svacTupleDir = os.path.join(L1Cmt, 'EngineeringModelRoot', svacTupleVersion)
svacTupleCmt = os.path.join(svacTupleDir, 'cmt')
svacTupleApp = os.path.join(svacTupleDir, cmtConfig, 'RunRootAnalyzer.exe')


if __name__ == "__main__":
    print L1Dir
    print reconApp
    
