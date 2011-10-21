
import os

import config

import pipeline
import runner


def drawOrbit(files, **extra):
    status = 0
    package = config.packages['FastMon']
    python = config.python
    app = config.apps['drawOrbit']
    saaDef = package['saaDefinition']
    # this relies on {in,out}FileTypes having one element each
    # but means we don't have to keep this in sync with the xml
    inFile = files[os.environ['inFileTypes']]
    outFile = files[os.environ['outFileTypes']]
    workDir = os.path.dirname(outFile)
    cmd = '''
    cd %(workDir)s
    %(python)s %(app)s -s %(saaDef)s -o %(outFile)s %(inFile)s
    ''' % locals()
    status |= runner.run(cmd)
    return status
