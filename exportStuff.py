#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Export completed runs to SSC.

This should run after the FT1 files from all runs in a downlink have been
registered with the data server.  It will export FT1 files for all runs which
are done to the SSC.  "Done," in this context, means:

either

We have recieved and processed all data from the run.

or

We know that we will not receive any more data for the run (probably because
the run is missing data and it has been over a week since it was taken).

This will require keeping track either of which runs have been sent or
(probably more efficient) which ones are "in process."

@todo Write the code.

@author W. Focke <focke@slac.stanford.edu>
"""

import glob
import os
import re
import sys

import config

# import pyfits

import GPLinit

import fileNames
import runner
import stageFiles

# template = 'gll_%(tag)s_%(run)s_v%(ver)s.fit'
# rex = re.compile('gll_[^_]+_[^_]+_v([0-9]+)\.fit')

# vForm = '%.3d'


head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']
fileType = os.environ['fileType']

# Where do we send the data?
if config.testMode:
    # send = ""             # noop
    send = "--send LISOC" # loopback test
else:
    #send = "--send GSSC"  # the real deal
    send = "--send LISOC" # always test mode for now
pass

# tags = {
#     'ft1': 'ph',
#     'ft2': 'pt',
#     'ls1': 'ev',
#     'ls3': 'lt',
#     }

staged = stageFiles.StageSet()
finishOption = config.finishOption

inputFile = fileNames.fileName(fileType, dlId, runId)
# inputDir, inputBase = os.path.split(inputFile)

# # figure out the version number
# values = {
#     'run': runId,
#     'tag': tags[fileType],
#     'ver': '*',
#     }

# oldTemplate = os.path.join(inputDir, template % values)
# print >> sys.stderr, 'Looking for %s' % oldTemplate
# oldFiles = glob.glob(oldTemplate)
# print >> sys.stderr, 'Found %s' % oldFiles
# if oldFiles:
#     oldFiles.sort()
#     last = oldFiles[-1]
#     mob = rex.search(last)
#     if mob:
#         version = int(mob.group(1)) + 1
#     else:
#         raise OSError, "Can't parse version from %s" % last, last
# else:
#     version = 0
#     pass
# values['ver'] = vForm % version
# exportBase = template % values
# exportFile = os.path.join(inputDir, exportBase)
# print >> sys.stderr, 'Input name is %s' % inputBase
# print >> sys.stderr, 'Output name is %s' % exportFile

stagedInFile = staged.stageIn(inputFile)
# stagedOutFile = staged.stageOut(exportFile)

# hduList = pyfits.open(stagedInFile)
# hduList[0].header.update('filename', exportBase)
# hduList.writeto(stagedOutFile)

# args = stagedOutFile
args = stagedInFile

isocBin = config.isocBin

cmd = """eval `%(isocBin)s/isoc env --add-env=flightops`
FASTCopy.py %(send)s %(args)s
""" % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
