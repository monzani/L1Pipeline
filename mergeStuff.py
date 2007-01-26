#!/usr/bin/env python

"""@brief Merge results of chunk or crumb processing.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
env = os.environ
import sys

#import runner

import config

#env['outFile']="larry_recon.root"
#env['inFiles']="larry_recon_1.root larry_recon_2.root larry_recon_3.root"

os.system(config.hadd+" "+env['outFile']+" "+env['inFiles'])

#cmd = config.hadd + (' %s' % outFile) + ((' %s' * len(inFiles)) % tuple(inFiles))
#status = runner.run(cmd)

#sys.exit(status)
