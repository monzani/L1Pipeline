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
txtFt2File = files['run']['ft2']
stagedFt1File = staged.stageOut(txtFt2File)

cmd = '''
cd %(workDir)s
%(app)s %(stagedDigiFile)s %(stagedMeritFile)s %(stagedM7File)
''' % locals()

status = runner.run(cmd)

staged.finish()

os.symlink(os.path.basename(txtFt2File), files['run']['ft2Export'])

fileType = 'FT2'
registerPrep.prep(fileType, realFt2File)

sys.exit(status)
