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
#staged.setupOK = False # debugging

if staged.setupOK:
#Local Copy of NFS dir	
    workDir = staged.stageDir
else:
    workDir = files['dirs']['run']
    pass

#? where do I find the dictionary?
app = config.apps['makeFT2']

#input file
#for FT2 digi merit M7
#digi
stagedDigiFile = staged.stageIn(files['run']['digi'])
#this merit is the same of the FT1?
stagedMeritFile = staged.stageIn(files['run']['merit'])
#M7 is m7 ok as dictionary word?
stagedM7File=  staged.stageIn(files['run']['m7'])

#output
txtFt2File = files['run']['ft2Txt']
stagedFt2TxtFile = staged.stageOut(txtFt2File)
fitsFt2File = files['run']['ft2Fits']
stagedFt2FitsFile = staged.stageOut(fitsFt2File)

cmd = '''
cd %(workDir)s
%(app)s -DigiFile %(stagedDigiFile)s -MeritFile %(stagedMeritFile)s -M7File %(stagedM7File)s -FT2_txt_File %(stagedFt2TxtFile)s -FT2_fits_File %(stagedFt2FitsFile)s
''' % locals()

status = runner.run(cmd)

staged.finish()

os.symlink(os.path.basename(fitsFt2File), files['run']['ft2Export'])

fileType = 'FT2'
registerPrep.prep(fileType, fitsFt2File)

sys.exit(status)
