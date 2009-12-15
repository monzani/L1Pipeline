substreams = pipeline.getSubstreams(subTask)

lSubs = {}
for stream in substreams:
    id = stream.getStream()
    pi = stream.getProcessInstance(subProcess)
    pk = pi.getPrimaryKey()
    tup = (pk, pi)
    if not lSubs.has_key(id) or lSubs[id] < tup: lSubs[id] = tup
    continue
pis = lSubs.items()
pis.sort()

versionTags = []
print 'Exit codes for subprocesses %s.%s:' % (subTask, subProcess)
for streamId, (pk, subPi) in pis:
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
