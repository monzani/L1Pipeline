#!/usr/bin/env python

"""@brief Find new event files.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys

import config

downLinkId = os.environ['DOWNLINK_ID']

# get list of all directories with data from this downlink
L0Dir = config.L0Dir
finder = 'find %(L0Dir)s -type d -name %(downLinkId)s -print' % locals()
downLinkDirs = [dlDir.strip() for dlDir in os.popen(finder)]

# Figure out which runs have data in this dl

