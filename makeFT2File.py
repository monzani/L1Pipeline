#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import GPLinit

import fileNames
import registerPrep
import runner
import stageFiles

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']

staged = stageFiles.StageSet()
finishOption = config.finishOption

app = config.apps['mergeFT2']

# input
txtFt2File = fileNames.fileName('ft2Txt', dlId, runId)
stagedFt2TxtFile = staged.stageIn(txtFt2File)

# output
fitsFt2File = fileNames.fileName('ft2', dlId, runId, next=True)
stagedFt2FitsFile = staged.stageOut(fitsFt2File)

workDir = os.path.dirname(stagedFt2FitsFile)

setupScript = config.packages['ft2Util']['setup']

version = fileNames.version(fitsFt2File)

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
