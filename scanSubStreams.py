substreams = pipeline.getSubstreams(subTask)
pis = [(stream.getStream(), stream.getProcessInstance(subProcess)) for stream in substreams]
pis.sort()
versionTags = []
print 'Exit codes for subprocesses %s.%s:' % (subTask, subProcess)
for streamId, subPi in pis:
    ec = subPi.getExitCode()
    print streamId, ec
    if ec:
        continue
    l1Id = subPi.getVariable('L1_PI_ID')
    version = subPi.getVariable('L1_PI_version')
    tag = '%s:%s' % (l1Id, version)
    versionTags.append(tag)
    continue
goodPis = ','.join(versionTags)
pipeline.setVariable('goodPis', goodPis)
