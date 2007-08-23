#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import GPLinit

import fileNames
import runner
import stageFiles


dlId = os.environ['DOWNLINK_ID']
runId = os.environ['RUNID']
chunkId = os.environ['CHUNK_ID']
files = fileNames.setup(dlId, runId, chunkId)
realInFile = files['chunk']['event']
realOutFile = files['chunk']['fastMon']
tmpOutFile = files['chunk']['fastMonTmp']

staged = stageFiles.StageSet()
inFile = staged.stageIn(realInFile)
outFile = staged.stageOut(tmpOutFile)

brokenName = outFile.replace('.processed', '')

if staged.setupOK:
    workDir = staged.stageDir
else:
    workDir = files['chunk']['dirs']['fastMon']
    pass

package = config.packages['FastMon']

common = config.packages['Common']
commonPy = os.path.join(common['root'], 'python')

os.environ.update(package['env'])

dmRoot = config.L1Cmt
fastMonDir = files['dirs']['fastMon']
os.environ['FAST_MON_DIR'] = fastMonDir

extra = package['extraSetup']
setup = package['setup']
app = config.apps['fastMon']

newLatexDir = config.installBin

cmd = '''
cd %(workDir)s
export DATAMONITORING_ROOT=%(dmRoot)s
export PATH=%(newLatexDir)s:${PATH}
%(extra)s
source %(setup)s
export PYTHONPATH=${PYTHONPATH}:%(fastMonDir)s:%(commonPy)s
%(app)s -v -o %(brokenName)s -d %(workDir)s -p %(inFile)s
ls -lahR
''' % locals()

status = runner.run(cmd)
status |= staged.finish()

status |= runner.run('mv %s %s' % (tmpOutFile, realOutFile))

sys.exit(status)
