#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import GPLinit

import fileNames
import runner
import stageFiles

head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
if not dlId: head, dlId = os.path.split(head)
runId = os.environ['RUNID']
chunkId = os.environ['CHUNK_ID']

staged = stageFiles.StageSet()
finishOption = config.finishOption

os.environ['EVTFILE'] = staged.stageIn(os.environ['EVTFILE'])
realDigiFile = fileNames.fileName('digi', dlId, runId, chunkId)
stagedDigiFile = staged.stageOut(realDigiFile)
os.environ['digiChunkFile'] = stagedDigiFile

workDir = os.path.dirname(stagedDigiFile)

#setupScript = config.cmtScript
app = config.apps['digi']
options =  config.digiOptions

dataSource = os.environ['DATASOURCE']
# if dataSource == 'LCI':
#     trigConfig = 'Default'
# else:
#     trigConfig = 'Moot'
#     pass
trigConfig = 'Default'
os.environ['trigConfig'] = trigConfig
if dataSource == 'LPA':
    geometry = 'latAssembly/latAssemblySegVols.xml'
elif dataSource == 'MC':
    geometry = 'flight/flightSegVols.xml'
    pass
os.environ['gleamGeometry'] = geometry
options = config.digiOptions[dataSource]

cmd = '''
cd %(workDir)s
%(app)s %(options)s
''' % locals()

status = runner.run(cmd)
if status: finishOption = 'wipe'

status |= staged.finish(finishOption)

sys.exit(status)
