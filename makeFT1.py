#!/usr/bin/env python

import os
import sys

import config

import fileNames
import runner
import stageFiles
#import pipeline
import registerPrep

files = fileNames.setup(os.environ['DOWNLINK_ID'], os.environ['RUNID'])

staged = stageFiles.StageSet()

if staged.staged:
    workDir = staged.stageDir
else:
    workDir = files['dirs']['run']
    pass

app = config.apps['makeFT1']

stagedMeritFile = staged.stageIn(files['run']['merit'])
realFt1File = files['run']['ft1']
stagedFt1File = staged.stageOut(realFt1File)

cmd = '''
cd %(workDir)s
%(app)s rootFile=%(stagedMeritFile)s fitsFile=%(stagedFt1File)s event_classifier=Pass4_Classifier
''' % locals()

status = runner.run(cmd)

staged.finish()

os.symlink(os.path.basename(realFt1File), files['run']['ft1Export'])

fileType = 'FT1'
registerPrep.prep(fileType, realFt1File)

sys.exit(status)
