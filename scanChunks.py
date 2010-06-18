

def getChunkPis():
    """Examine chunk-level PIs to see what files we expect to find for merging
    and their versions.
    """
    ## figure out which deliveries have data for this run
    # by looking for $runDir/*.chunkList.txt
    deliveryIds = getDeliveryIds()
    print deliveryIds
    # get run-level streams
    rdlStreams = getStreams(deliveryIds)

    pis = []

    for rdl in rdlStreams:
        rdlChunks = rdl.getSubstreams('doChunk')
        rdlPis = [(chunk.getStream(), chunk.getProcessInstance(subProcess)) for chunk in rdlChunks]
        pis.extend(rdlPis)
        continue
    return pis


def getDeliveryIds():
    import os
    # import re
    # chunkListRe = re.compile('^[^_]+_([0-9]+)_chunkList.txt$')
    runFiles = os.listdir(runDir)
    ids = []
    for runFile in runFiles:
        # mob = chunkListRe.match()
        # if mob: ids.append(mob.group(1))
        if runFile.endswith('_chunkList.txt'):
            ids.append(runFile.split('_')[1])
            pass
        continue
    return ids


def getStreams(deliveryIds):
    """This is really only meant to find the doRun* streams corresponding to
    the current run in a supplied list of deliveries.
    It's probably overgeneral, it could find streams of anything where the
    id path matches below the delivery. But the chunk ids from the same run
    never match, so it couldn't be used to find chunk or crumb streams
    (but I guess it could fins cleanupCompleteRun).
    """
    thisTask = pipeline.getTask()
    print 'this task: %s' % thisTask
    # walk up the task chain to find our top-level task and the chain of
    # subtask names we will need to walk back down the stream chain
    nameChain = []
    topTask = thisTask
    while topTask.getHasParent():
        nameChain.append(topTask.getName())
        topTask = topTask.getParent()
        continue
    nameChain.reverse()
    print 'top task: %s' % topTask
    print 'name chain: %s' % nameChain
    # now walk back down the stream chain for each delivery
    streamPath = pipeline.getStreamPath().split('.')
    assert streamPath[0] in deliveryIds
    del streamPath[0]
    assert len(streamPath) == len(namePath)
    streams = []
    for deliveryId in deliveryIds:
        stream = topTask.getStream(deliveryId)
        for subTaskName, subStreamId in zip(namePath, streamPath):
            stream = stream.getSubStream(subTaskName, subStreamId)
            continue
        streams.append(stream)
        continue
    return streams


finalOrRunning = ['SUCCESS', 'FAILED', 'TERMINATED', 'CANCELED', 'RUNNING']
def getStreams2():
    thisStream = getCurrentStream()
    id = thisStream.getStreamId()
    thisTask = thisStream.getTask()
    print 'this task: %s' % thisTask
    rdlStreams = []
    allstreams = thisTask.getStreams(id)
    for stream in allStreams:
        status = stream.getStreamStatus()
        if status in finalOrRunning: rdlStreams.append(stream)
        continue
    return rdlStreams


def getCrumbPis():
    substreams = pipeline.getSubstreams(subTask)
    pis = [(stream.getStream(), stream.getProcessInstance(subProcess)) for stream in substreams]
    return pis


getPis = {'doChunk': getChunkPis, 'doCrumb': getCrumbPis}[subTask]

pis = getPis()

pis.sort()
versionTags = []
print 'Exit codes for subprocesses %s.%s:' % (subTask, subProcess)
for streamId, subPi in pis:
    ec = subPi.getExitCode()
    statStr = subPi.getStatus()
    print streamId, ec, statStr
    if ec or statStr != 'SUCCESS':
        continue
    varNames = ['L1_PI_ID', 'L1_PI_version']
    tup = tuple([subPi.getVariable(name) for name in varNames])
    print tup
    if None in tup:
        continue
    tag = '%s:%s' % tup
    versionTags.append(tag)
    continue
if not versionTags: raise SystemExit, "No successful jobs, failing."
goodPis = ','.join(versionTags)
pipeline.setVariable('goodPis', goodPis)
