"""@brief Register output data with the data server.

@author W. Focke <focke@slac.stanford.edu>
"""

# This script is automagically pasted into the XML at install time

parentPI = pipeline.getProcessInstance(parentProcess)
logicalPath = parentPI.getVariable("REGISTER_LOGIPATH")
filePath = parentPI.getVariable("REGISTER_FILEPATH")
attributes = "tstart=0:tstop=120"
datacatalog.registerDataset(dataType, logicalPath, filePath, attributes)
