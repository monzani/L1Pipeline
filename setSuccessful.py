l1RunStatus = pipeline.getProcessInstance(parentProcess).getVariable('l1RunStatus')
print 'Setting L1RunStatus for run', runNumber, ' to ', l1RunStatus
runQuality.setL1RunStatus(runNumber, l1RunStatus)
reviewStatus = "Waiting review"
print 'Setting ReviewStatus for run', runNumber, ' to ', reviewStatus
runQuality.setReviewStatus(runNumber, reviewStatus)
