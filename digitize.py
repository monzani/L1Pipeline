#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

import config

import rootFiles
import runner

def digitize(**args):
    status = 0

    staged = args['staged']
    os.environ['EVTFILE'] = staged.stageIn(os.environ['EVTFILE'])
    stagedDigiFile = args['files']['digi']
    os.environ['digiChunkFile'] = stagedDigiFile

    workDir = args['workDir']

    app = config.apps['digi']
    options =  config.digiOptions

    dataSource = os.environ['DATASOURCE']
    if dataSource == 'LCI':
        trigConfig = 'Default'
    else:
        trigConfig = 'Moot'
        pass
    # trigConfig = 'Default'
    os.environ['trigConfig'] = trigConfig
    if dataSource in ['LPA', 'LCI']:
        geometry = 'latAssembly/latAssemblySegVols.xml'
    elif dataSource in ['MC']:
        geometry = 'flight/flightSegVols.xml'
    else:
        print >> sys.stderr, 'Bad DATASOURCE %s' % dataSource
        status = 1
        pass
    os.environ['gleamGeometry'] = geometry
    options = config.digiOptions[dataSource]

    cmd = '''
    cd %(workDir)s
    %(app)s %(options)s
    ''' % locals()

    if not status: status |= runner.run(cmd)

    chunkEvents = rootFiles.getFileEvents(stagedDigiFile)
    print >> sys.stderr, "Chunk has %d events." % chunkEvents
    if chunkEvents < 1: status |= 1

    return status
