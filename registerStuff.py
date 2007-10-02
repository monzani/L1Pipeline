"""@brief Register output data with the data server.
@author W. Focke <focke@slac.stanford.edu>
"""
# This script is automagically pasted into the XML at install time
parentPI = pipeline.getProcessInstance(parentProcess)
logicalPath = parentPI.getVariable("REGISTER_LOGIPATH")
filePath = parentPI.getVariable("REGISTER_FILEPATH")
attributes = ':'.join([
    "nMetStart=%f" % tStart,
    "nMetStop=%f" % tStop,
    'sDataSource=%s' % DATASOURCE,
    'nRun=%d' % int(RUNID[1:]),
    'nDownlink=%d' % DOWNLINK_ID,
    'sRunStatus=%s' % RUNSTATUS,
    ])
datacatalog.registerDataset(dataType, logicalPath, filePath, attributes)
