substreams = pipeline.getSubstreams(subTask)
pis = [(stream.getStream(), stream.getProcessInstance(subProcess)) for stream in substreams]
pis.sort()
ecTags = []
statusTags = []
for streamId, subPi in pis:
    ec = subPi.getExitCode()
    ecTags.append('%d: %d' % (streamId, ec))
    if ec:
        continue
    pipk = subPi.getPrimaryKey()
    tag = '%d:%d' % (streamId, pipk)
    statusTags.append(tag)
    continue
print '\n'.join(['Exit codes for subprocesses %s.%s:' % (subTask, subProcess)] + ecTags)
versions = ','.join(statusTags)
pipeline.setVariable('goodPis', versions)
