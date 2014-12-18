#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

import os
import sys

if __name__ == "__main__":
    print >> sys.stderr, "This module is not supported as main script"
    sys.exit(1)

import config

import rootFiles
import runner

def digitize(files, idArgs, workDir, staged, **args):
    status = 0

    os.environ['EVTFILE'] = files['event']
    stagedDigiFile = files['digi']
    os.environ['digiChunkFile'] = stagedDigiFile

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

    instDir = config.glastLocation
    glastExt = config.glastExt
    igrfExport = config.igrfExport
    
    cmd = '''
    export INST_DIR=%(instDir)s 
    export GLAST_EXT=%(glastExt)s
    %(igrfExport)s
    cd %(workDir)s
    %(app)s %(options)s
    ''' % locals()

    if not status: status |= runner.run(cmd)

    chunkEvents = rootFiles.getFileEvents(stagedDigiFile)
    print >> sys.stderr, "Chunk has %d events." % chunkEvents
    if chunkEvents < 1: status |= 1

    return status
