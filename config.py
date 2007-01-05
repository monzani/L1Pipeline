"""@brief Configuration.

@author W. Focke <focke@slac.stanford.edu>
"""

import os

L1Version = "0.0"

# nevermind these, Bryson will tell us where to find the data
#L0Disk = '/nfs/slac/g/svac/focke/L1'
#L0Dir = os.path.join(L0Disk, 'rawData')

L1Disk = '/nfs/slac/g/svac/focke/L1'
L1Dir = os.path.join(L1Disk, 'rootData')

maxCpu = 1000
