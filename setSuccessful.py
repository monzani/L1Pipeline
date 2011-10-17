def good():
    l1RunStatus = parentPi.getVariable('l1RunStatus')
    print 'Setting L1RunStatus for run', runNumber, ' to ', l1RunStatus
    runQuality.setL1RunStatus(runNumber, l1RunStatus)
    reviewStatus = "Waiting review"
    print 'Setting ReviewStatus for run', runNumber, ' to ', reviewStatus
    runQuality.setReviewStatus(runNumber, reviewStatus)
    return

def bad():
    l1RunStatus = 'Failed'
    print 'Setting L1RunStatus for run', runNumber, ' to ', l1RunStatus
    runQuality.setL1RunStatus(runNumber, l1RunStatus)
    return

currentStream = pipeline.getCurrentStream()
parentPi = currentStream.getProcessInstance(parentProcess)
parentStatus = parentPi.getStatus()
if parentStatus in ['SUCCESS']:
    good()
else:
    bad()
    pass
