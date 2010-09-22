

finalOrRunning = ['SUCCESS', 'FAILED', 'TERMINATED', 'CANCELED', 'RUNNING']
def getStreams():
    thisStream = pipeline.getCurrentStream()
    id = thisStream.getId()
    print 'stream id: %s' % id
    thisTask = thisStream.getTask()
    print 'this task: %s' % thisTask
    rdlStreams = []
    allStreams = thisTask.getStreams(id)
    for stream in allStreams:
        status = stream.getStatus()
        print stream, status
        if status in finalOrRunning: rdlStreams.append(stream)
        continue
    return rdlStreams


def getChunkPis():
    """Examine chunk-level PIs to see what files we expect to find for merging
    and their versions.
    """
    rdlStreams = getStreams()

    pis = []

    for rdl in rdlStreams:
        rdlChunks = rdl.getSubStreams(subTask)
        rdlPis = [(chunk.getId(), chunk.getProcessInstance(subProcess)) for chunk in rdlChunks]
        pis.extend(rdlPis)
        continue
    return pis


def getCrumbPis():
    thisStream = pipeline.getCurrentStream()
    subStreams = thisStream.getSubStreams(subTask)
    pis = []
    for stream in subStreams:
        print 'subStream: %s' % stream
        sId = stream.getId()
        print 'subId: %s' % sId
        sPi = stream.getProcessInstance(subProcess)
        print 'subPi: %s' % sPi
        pis.append((sId, sPi))
    return pis


getPis = {
    'doChunk': getChunkPis,
    'doChunkLci': getChunkPis,
    'doCrumb': getCrumbPis
    }[subTask]

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
    # tup = tuple([subPi.getVariable(name) for name in varNames])
    tup = []
    varMap = subPi.getVariables()
    print 'varMap: %s' % varMap
    #raise SystemExit, 'quit here'
    for name in varNames:
        print 'key: %s' % name
        value = subPi.getVariable(name)
        print 'value: %s' % value
        tup.append(value)
    tup = tuple(tup)
    print tup
    if None in tup:
        continue
    tag = '%s:%s' % tup
    versionTags.append(tag)
    continue
if not versionTags: raise SystemExit, "No successful jobs, failing."
goodPis = ','.join(versionTags)
pipeline.setVariable('goodPis', goodPis)
