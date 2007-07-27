#!/afs/slac/g/glast/isoc/flightOps/rhel3_gcc32/ISOC_PROD/bin/shisoc python2.5

"""@brief Launch ASP.

@author W. Focke <focke@slac.stanford.edu>
"""

import bisect
import time

import glastTime


"""
children = select CHILD_TASK from TASKLAUNCH where \
    PARENT_TASK == os.environ['PIPELINE_TASK'] and \
    time() > LAST_LAUNCH + MINIMUM_ELAPSED
for child in children:
        os.system('pipeline createStream %s' % child)
        update TASKLAUNCH set LAST_LAUNCH = time() where CHILD_TASK = child
"""

## chunks = [(cStart, cStop, nEvents), ...]

# sort chunks by time
chunks.sort()

chunks = num.array(chunks)
startTimes, stopTimes, nEvents = num.transpose(chunks)

# get newly delivered time
deliveredTime = num.sum(stopTimes - startTimes)
# and events
deliveredEvents = num.sum(nEvents)

lastDeliveredEvent = stopTimes[-1]

# children = select CHILD_TASK from TASKLAUNCH where \
#     PARENT_TASK == os.environ['PIPELINE_TASK'] and \
#     time() > LAST_LAUNCH + MINIMUM_ELAPSED


"""
children contain:

lastProcessedEvent = trigger time of last event that was fed to the
child the last time it ran

lastNewEvent = trigger time of the last event that has been delivered since
the last time the child ran

newDEvents = number of events delivered since the last time it ran

newAEvents = number of events acquired since the last time it ran

newDTime = science obs time delivered since the last time it ran

newATime = science obs time acquired since the last time it ran

"""


for child in children:

    # figure out which chunks were acquired after the last event that
    # was passed to the child the last time it was run
    newIndex = num.searchsorted(startTimes, child.lastProcessedEvent)
    newStarts, newStops, newEvents = num.transpose(chunks[newIndex:])

    # get time and events contained in those chunks
    acquiredTime = num.sum(newStops - newStarts)
    acquiredEvents = num.sum(newEvents)
    

    if launchChild:
        # update child records one way
        child.lastLaunchTime = glastTime.met()
        child.lastProcessedEvent = lastDeliveredEvent
        child.newDEvents = 0
        child.newAEvents = 0
        child.newDTime = 0
        child.newATime = 0
    else:
        # update child records another way
        child.lastNewEvent = lastDeliveredEvent
        child.newDEvents += deliveredEvents
        child.newAEvents += acquiredEvents
        child.newDTime += deliveredTime
        child.newATime += acquiredTime
        pass

    continue
