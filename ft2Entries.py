#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import GPLinit

import fileNames
import runner
import stageFiles
import pipeline
import registerPrep

files = fileNames.setup(os.environ['DOWNLINK_ID'], os.environ['RUNID'])

staged = stageFiles.StageSet()
finishOption = config.finishOption

if staged.setupOK:
#Local Copy of NFS dir	
    workDir = staged.stageDir
else:
    workDir = files['dirs']['run']
    pass

app = config.apps['makeFT2']

#input file
#for FT2 digi merit M7
stagedDigiFile = staged.stageIn(files['run']['digi'])
stagedMeritFile = staged.stageIn(files['run']['merit'])
stagedM7File=  staged.stageIn(files['run']['m7'])

#output
txtFt2File = files['run']['ft2Txt']
stagedFt2TxtFile = staged.stageOut(txtFt2File)
stagedFt2FitsFile = os.path.join(workDir, 'junkFT2.fits')

setupScript = config.packages['ft2Util']['setup']

cmd = '''
cd %(workDir)s
source %(setupScript)s
%(app)s -DigiFile %(stagedDigiFile)s -MeritFile %(stagedMeritFile)s -M7File %(stagedM7File)s -FT2_txt_File %(stagedFt2TxtFile)s -FT2_fits_File %(stagedFt2FitsFile)s --MC
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
