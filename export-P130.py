#!/afs/slac/g/glast/isoc/flightOps/rhel5_gcc41/ISOC_PROD/bin/shisoc python2.6

"""@brief Set a time stamp in a pipeline variable.

flagFT2.wrapupQuality expects to get a timestamp of when the ft2 file
was exported. But flagFT2-P130 doesn't export. So this just makes a
timestamp for it to use.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import sys
import time

import config

import GPLinit

import pipeline

status = 0

exportTime = time.time()
pipeline.setVariable("exportTime", exportTime)

sys.exit(status)
