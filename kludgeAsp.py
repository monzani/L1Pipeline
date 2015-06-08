#!/afs/slac/g/glast/isoc/flightOps/rhel5_gcc41/ISOC_PROD/bin/shisoc python2.6

"""@brief Find new run directories.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

import config

import GPLinit

import glastTime
import runner

status = 0

dlRawDir = os.environ['DOWNLINK_RAWDIR']
head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)

os.environ['nDownlink'] = os.environ['DOWNLINK_ID']
os.environ['folder'] = config.dataCatDir
cmd = config.aspLauncher

status = runner.run(cmd)

if status == config.aspAlreadyLaunched:
    print >> sys.stderr, 'ASP already launched for delivery %s' % dlId
    status = 0
    pass

sys.exit(status)
