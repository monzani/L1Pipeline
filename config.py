"""@brief Configuration.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
env = os.environ

L1Version = "0.1"

# nevermind these, Bryson will tell us where to find the data
#L0Disk = '/nfs/slac/g/svac/focke/L1'
#L0Dir = os.path.join(L0Disk, 'rawData')

L1Disk = '/nfs/slac/g/svac/focke/L1'
L1Dir = os.path.join(L1Disk, 'rootData')

maxCpu = 1000

maxCrumbSize = 6353

cmtConfig = 'rh9_gcc32opt'
glastExt = os.path.join('/afs/slac.stanford.edu/g/glast/ground/GLAST_EXT',
                        cmtConfig)
env['GLAST_EXT'] = glastExt
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
#
digiApp = gleam
reconApp = gleam
#
digiOptions = os.path.join(env['L1ProcROOT'], 'digi.jobOpt')
reconOptions = os.path.join(env['L1ProcROOT'], 'recon.jobOpt')

if __name__ == "__main__":
    print L1Dir
    print reconApp
    
