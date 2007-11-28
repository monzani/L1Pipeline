#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import GPLinit

import fileNames
import registerPrep
import runner
import stageFiles

dlId = os.environ['DOWNLINK_ID']
runId = os.environ['RUNID']
files = fileNames.setup(dlId, runId)

staged = stageFiles.StageSet()
finishOption = config.finishOption

if staged.setupOK:
#Local Copy of NFS dir	
    workDir = staged.stageDir
else:
    workDir = files['dirs']['run']
    pass

app = config.apps['mergeFT2']

# input
txtFt2File = files['run']['ft2Txt']
stagedFt2TxtFile = staged.stageIn(txtFt2File)

# output
fitsFt2File = files['run']['ft2Fits']
stagedFt2FitsFile = staged.stageOut(fitsFt2File)

setupScript = config.packages['ft2Util']['setup']

cmd = '''
cd %(workDir)s
source %(setupScript)s
%(app)s -FT2_txt_File %(stagedFt2TxtFile)s -FT2_fits_File %(stagedFt2FitsFile)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

fileType = 'FT2'
registerPrep.prep(fileType, fitsFt2File)

sys.exit(status)
