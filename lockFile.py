#!/sdf/data/fermi/a/isoc/flightOps/rhel6_gcc44/ISOC_PROD/bin/shisoc python2.6

"""@brief Functions for dealing with lockfiles.

@author W. Focke <focke@slac.stanford.edu>
"""

import os
import socket
import sys
import time

import l1Logger
import config

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


def lockData(id,base):
    data = {
        'id': id,
        'run': base,
        'host': socket.gethostname(),
        'pid': os.getpid(),
        'time': time.time(),
        }
    return data


# Probably most of these routines should return a status.


def lockDir(directory, base, id):

    if not os.path.isdir(directory): os.system('mkdir -p %s' % directory)

    # Make a hopefully unique file name.
    uniqFile = os.path.join(directory, uniqName())
    uniqThr = os.path.join(config.throttleDir, uniqName())

    lockFile = os.path.join(directory, lockFileName(base))
    
    while os.path.exists(lockFile):
        print >> sys.stderr, 'File %s already exists at [%s]' % (lockFile,time.ctime())
        time.sleep(300)

    # This should fail if the file already exists.  It should be atomic for a
    # local file, but not if the file is on NFS.  So if this fails, we know
    # there's a problem, but if it succeeds, things still might not be okay.
    print >> sys.stderr, 'Trying to create %s' % uniqFile
    try:
        fd = os.open(uniqFile, os.O_EXCL | os.O_RDWR | os.O_CREAT)
    except OSError:
        raise LockedError, "%s already exists.  This should NOT happen!" % uniqFile

    f = os.fdopen(fd, "w")
    f.write('%r\n' % lockData(id,base))
    f.close()

    # # Apparently closing f also closes fd
    # os.close(fd)

    # Here is the actual locking operation.  This is advertized as atomic even
    # on NFS.
    print >> sys.stderr, 'Trying to link %s' % lockFile
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


def lockAndThrottle(directory, base, id):

    if not os.path.isdir(directory): os.system('mkdir -p %s' % directory)

    # Make a hopefully unique file name.
    uniqFile = os.path.join(directory, uniqName())
    uniqThr = os.path.join(config.throttleDir, uniqName())

    lockFile = os.path.join(directory, lockFileName(base))
    
    while os.path.exists(lockFile):
        print >> sys.stderr, 'File %s already exists at [%s]' % (lockFile,time.ctime())
        time.sleep(300)
 
    # This should fail if the file already exists.  It should be atomic for a
    # local file, but not if the file is on NFS.  So if this fails, we know
    # there's a problem, but if it succeeds, things still might not be okay.
    print >> sys.stderr, 'Trying to create %s' % uniqFile
    try:
        fd = os.open(uniqFile, os.O_EXCL | os.O_RDWR | os.O_CREAT)
    except OSError:
        raise LockedError, "%s already exists.  This should NOT happen!" % uniqFile

    f = os.fdopen(fd, "w")
    f.write('%r\n' % lockData(id,base))
    f.close()

    # # Apparently closing f also closes fd
    # os.close(fd)

    # Here is the actual locking operation.  This is advertized as atomic even
    # on NFS.
    print >> sys.stderr, 'Trying to link %s' % lockFile
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

    # Now I try to get a throttling lock
    while len(os.listdir(config.throttleDir)) >= config.throttleLimit:
        print >> sys.stderr, 'No available throttle locks at [%s]' % (time.ctime())
        time.sleep(300)
 
    print >> sys.stderr, 'Trying to create %s' % uniqThr
    try:
        fd = os.open(uniqThr, os.O_EXCL | os.O_RDWR | os.O_CREAT)
    except OSError:
        unlockDir(directory, base, id) 
        raise LockedError, "%s already exists.  This should NOT happen!" % uniqThr

    f = os.fdopen(fd, "w")
    f.write('%r\n' % lockData(id,base))
    f.close()
    
    for idx in range(config.throttleLimit):
        thrLockFile = os.path.join(config.throttleDir, lockFileName(str(idx)))

        print >> sys.stderr, 'Trying to link %s' % thrLockFile
        try:
            os.link(uniqThr, thrLockFile)
            os.unlink(uniqThr)
            return
        except OSError:
            pass
            
    os.unlink(uniqThr)
    unlockDir(directory, base, id) 
    raise LockedError, "Couldn't get a throttling lock."
    return


def unlockDir(directory, base, id):

    lockFile = os.path.join(directory, lockFileName(base))

    # Open and read lock file.
    try:
        data = readLock(directory, base, id)
    except IOError:
        # This is probably bad.  What if we don't have permission?
        # Nor should the file be missing.
        # On prod, we should fail here.
        #
        # Or at least send a message to the log watcher.
        msg = "Can't open lockfile %s." % lockFile
        print >> sys.stderr, msg
        l1Logger.warn(msg)
        return

    # Die if lock was not written by this stream.
    if data['id'] != id:
        raise LockedError, "Directory %s was locked by %s, but I'm %s!" % \
              (directory, data['id'], id)

    os.unlink(lockFile)

    return


def unlockThrottle(id,run):

    for idx in range(config.throttleLimit):
        thrLockFile = os.path.join(config.throttleDir, lockFileName(str(idx)))

        # Open and read lock file.
        try:
            data = readLock(config.throttleDir, str(idx), id)
        except IOError:
            msg = "Can't open throttle lock %s." % thrLockFile
            print >> sys.stderr, msg
            continue

        # If lock was written by this stream, remove it
        if data['id'] == id and data['run'] == run:
            os.unlink(thrLockFile)
            print >> sys.stderr, "Lock %s successfully removed" % thrLockFile
            return
            
    # If lock wasn't found, generate a warning
    msg = "Couldn't find any throttle lock for %s,%s (probably it was already removed?)" %(id,run)
    print >> sys.stderr, msg
    l1Logger.warn(msg)
    return

def readLock(directory, base, id):
    lockFile = os.path.join(directory, lockFileName(base))
    data = eval(open(lockFile).read())
    return data


if __name__ == "__main__":
    import fileNames
    head, dlId = os.path.split(os.environ['DOWNLINK_RAWDIR'])
    if not dlId: head, dlId = os.path.split(head)
    runId = os.environ['RUNID']
    runDir = os.path.dirname(fileNames.fileName('chunkList', dlId, runId)) #bleh
    action = os.environ.get('l1LockAction', 'LockDirOnly')
    if action == 'LockDirOnly':
        print >> sys.stderr, "Attempting to lock directory [%s] at [%s]" % \
              (runDir, time.ctime())
        lockDir(runDir, runId, dlId)
    elif action == 'LockAndThrottle':
        print >> sys.stderr, "Attempting to lock directory [%s] and to obtain a throttle lock at [%s]" % \
              (runDir, time.ctime())
        lockAndThrottle(runDir, runId, dlId)
    elif action == 'UnLock':
        print >> sys.stderr, "Attempting to unlock directory [%s] at [%s]" % \
              (runDir, time.ctime())
        unlockDir(runDir, runId, dlId)
    elif action == 'UnThrottle':
        print >> sys.stderr, "Attempting to remove throttle lock at [%s]" % \
              (time.ctime())
        unlockThrottle(dlId,runId)
    else:
        print >> sys.stderr, "Bad lock action [%s]" % action
        sys.exit(1)
        pass
    pass
