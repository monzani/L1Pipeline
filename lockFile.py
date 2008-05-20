#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Functions for dealing with lockfiles.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import socket
import sys
import time

class LockedError(EnvironmentError):
    pass

def lockFileName(base):
    """Make up a name for a lockfile."""
    lockName = '.'.join((base, 'lock'))
    return lockName


def uniqName():
    """Make up a filename that is likely to be unique."""
    uniq = '@'.join((`os.getpid()`, socket.gethostname(), `int(time.time())`))
    return uniq


def lockData(id):
    data = {
        'id': id,
        'host': socket.gethostname(),
        'pid': os.getpid(),
        'time': time.time(),
        }
    return data


def lockDir(directory, base, id):

    if not os.path.isdir(directory): os.system('mkdir -p %s' % directory)

    # Make a hopefully unique file name.
    uniqFile = os.path.join(directory, uniqName())

    lockFile = os.path.join(directory, lockFileName(base))
    
    # This should fail if the file already exists.  It should be atomic for a
    # local file, but not if the file is on NFS.  So if this fails, we know
    # there's a problem, but if it succeeds, things still might not be okay.
    try:
        fd = os.open(uniqFile, os.O_EXCL | os.O_RDWR | os.O_CREAT)
    except OSError:
        raise LockedError, "%s already exists.  This should NOT happen!"

    f = os.fdopen(fd, "w")
    f.write('%r\n' % lockData(id))
    f.close()

    # # Apparently closing f also closes fd
    # os.close(fd)

    # Here is the actual locking operation.  This is advertized as atomic even
    # on NFS.
    try:
        os.link(uniqFile, lockFile)
    except OSError:
        os.unlink(uniqFile)
        raise LockedError, "Already locked."

    # It is possible that the previous operation reported failure, but was
    # actually successful.  The man pages for open(2) and link(2) suggest a
    # way to detect this (stat(uniqFile) and see that its link count has gone
    # from 1 to 2), but I am reluctant to jump through hoops to try to
    # automatically recover a situation where we know that something is
    # broken.  Let the operator deal with it.  If it turns out to be a
    # problem, we can add that check later.

    # Don't need unigFile anymore.
    os.unlink(uniqFile)

    return

def unlockDir(directory, base, id):

    lockFile = os.path.join(directory, lockFileName(base))

    # Open and read lock file.  Die if it isn't there, or other wierdness.
    try:
        data = readLock(directory, base, id)
    except IOError:
        # This is probably bad.  What if we don't have permission?
        # Nor should the file be missing.
        # On prod, we should fail here.
        print >> sys.stderr, "Can't open lockfile %s.  Very odd, but we'll continue." % lockFile
        return

    # Die if lock was not written by this stream.
    if data['id'] != id:
        raise LockedError, "Directory %s was locked by %s, but I'm %s!" % \
              (directory, data['id'], id)

    os.unlink(lockFile)

    return

def readLock(directory, base, id):
    lockFile = os.path.join(directory, lockFileName(base))
    data = eval(open(lockFile).read())
    return data


if __name__ == "__main__":
    import config
    import fileNames
    head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
    if not dlId: head, dlId = os.path.split(head)
    runId = os.environ['RUNID']
    runDir = os.path.dirname(fileNames.fileName('chunkList', dlId, runId)) #bleh
    print >> sys.stderr, "Attempting to lock directory [%s] at [%s]" % \
          (runDir, time.ctime())
    lockDir(runDir, runId, dlId)
    pass
