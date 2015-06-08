import os
import sys

if __name__ == "__main__":
    print >> sys.stderr, "This module is not supported as main script"
    sys.exit(1)

import config

import fileNames
import meritFiles
import runner
import pyfits

def fixGTI(files, inFileTypes, outFileTypes, workDir, **args):
    status = 0

    inFileType = inFileTypes[0]
    ft2FileType = inFileTypes[1]

    assert len(outFileTypes) == 1
    outFileType = outFileTypes[0]

    stSetup = config.stSetup
    app = config.apps['fixGTI']

    stagedInFile = files[inFileType]
    stagedFt2File = files[ft2FileType]
    stagedOutFile = files[outFileType]

    version = fileNames.version(stagedOutFile)
    print >> sys.stderr, "Updating the header version in %s to %d" % (stagedInFile, version)
    fixVer = pyfits.open(stagedInFile,mode='update')
    fixVer[0].header.update('VERSION',version)
    fixVer.close()

    filter = 'LIVETIME>0'

    instDir = config.ST
    glastExt = config.glastExt
    igrfExport = config.igrfExport

    cmd = '''
    cd %(workDir)s
    export INST_DIR=%(instDir)s
    export GLAST_EXT=%(glastExt)s
    %(igrfExport)s
    source %(stSetup)s
    %(app)s overwrite=yes roicut=no scfile=%(stagedFt2File)s filter="%(filter)s" evfile=%(stagedInFile)s outFile=%(stagedOutFile)s
    ''' % locals()

    status = runner.run(cmd)
    return status
