#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Make monitoring histograms for a digi chunk.

@author W. Focke <focke@slac.stanford.edu>
"""
from os import environ
import os

import sys

import GPLinit

import fileNames
import runner
import stageFiles

import config


files = fileNames.setup(environ['DOWNLINK_ID'], environ['RUNID'], \
                        environ['CHUNK_ID'])

staged = stageFiles.StageSet()

nameBase = files['chunk']['head']

if environ['reportType'] == 'recon':
    stagedDigiFile = 'noSuchFile'
    stagedReconFile = staged.stageIn(files['chunk']['recon'])
    outDir = files['dirs']['reconMon']
else:
    stagedDigiFile = staged.stageIn(files['chunk']['digi'])
    stagedReconFile = 'noSuchFile'
    outDir = files['dirs']['digiMon']
    pass


glastVersion = config.glastVersion
testReportVersion = config.packages['TestReport']['version']

tkrCalibSerNo = '-9999'
calCalibSerNo = '-9999'

# contents of JO file
options = \
"""%(stagedDigiFile)s
%(stagedReconFile)s
%(outDir)s
%(nameBase)s
%(testReportVersion)s
%(glastVersion)s
%(tkrCalibSerNo)s
%(calCalibSerNo)s
""" \
% locals()

# write JO file
optionFile = os.path.join(outDir, 'jobOptions.txt')
open(optionFile, 'w').write(options)


# do the work
digiMonApp = config.apps['digiMon']
digiMonCmt = config.packages['TestReport']['setup']
environ['LD_LIBRARY_PATH']=config.glastLocation+"/lib:"+config.rootSys+"/lib:"+config.glastExt+"/xerces/2.6.0/lib:"+environ['LD_LIBRARY_PATH']
environ['ROOTSYS']=config.rootSys
cmd = 'cd %(outDir)s ; printenv CMTPATH; source %(digiMonCmt)s ; printenv LD_LIBRARY_PATH; %(digiMonApp)s %(optionFile)s' % locals()
status = runner.run(cmd)

staged.finish()

sys.exit(status)
