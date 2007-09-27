#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""Should merge this with ft2Entries.
"""

import os
import sys

import config

import GPLinit

import fileNames
import runner
import stageFiles
import pipeline
import registerPrep

files = fileNames.setup(os.environ['DOWNLINK_ID'], os.environ['RUNID'], os.environ['CHUNK_ID'])

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
#for fake FT2 M7
stagedM7File=  staged.stageIn(files['run']['m7'])

#output
stagedFt2TxtFile = os.path.join(workDir, 'junkFT2.txt')
fakeFt2File = files['chunk']['ft2Fake']
stagedFt2FitsFile = staged.stageOut(fakeFt2File)


setupScript = config.packages['ft2Util']['setup']

cmd = '''
cd %(workDir)s
source %(setupScript)s
%(app)s -M7File %(stagedM7File)s -FT2_txt_File %(stagedFt2TxtFile)s -FT2_fits_File %(stagedFt2FitsFile)s --Gleam
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
