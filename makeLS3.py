#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import GPLinit

import fileNames
import runner
import stageFiles
#import pipeline
import registerPrep

files = fileNames.setup(os.environ['DOWNLINK_ID'], os.environ['RUNID'])

staged = stageFiles.StageSet()
finishOption = config.finishOption

if staged.setupOK:
    workDir = staged.stageDir
else:
    workDir = files['dirs']['run']
    pass

app = config.apps['makeLS3']

realFt1File = files['run']['ft1']
stagedFt1File = staged.stageIn(realFt1File)
realFt2File = files['run']['ft2']
stagedFt2File = staged.stageIn(realFt2File)

realLs3File = files['run']['ls3']
stagedLs3File = staged.stageOut(realLs3File)

stSetup = config.stSetup
makeLS3Setup = os.path.join('$FITSGENROOT', 'cmt', 'setup.sh')

cmd = '''
cd %(workDir)s
#source %(stSetup)s
#source %(makeLS3Setup)s
%(app)s evfile=%(stagedFt1File)s scfile=%(stagedFt2File)s outfile=%(stagedLs3File)s dcostheta=0.025 binsize=1
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

fileType = 'LS3'
registerPrep.prep(fileType, realLs3File)

sys.exit(status)
