
import os
import sys

import config

import fileNames
import variables

dlId = os.environ.get('DOWNLINK_ID')
runId = os.environ.get('RUNID')
  
def prep(fileType, fileName):
    """
    Deal with batch-side prep to register a file with the data catalog.
    Actual registration is done by a scriptlet (in registerStuff.py).
    This sets up some pipeline variables so the scriptlet knows what to do.
    """

    taskName = os.environ['L1_TASK_NAME']
    taskVersion =  os.environ['PIPELINE_TASKVERSION']
    creator = '-'.join([taskName, taskVersion])

    variables.setVar(fileType, 'format', fileNames.fileTypes[fileType])
    # variables.setVar(fileType, 'path', config.dataCatDir) # remove me!
    variables.setVar(fileType, 'group', fileNames.dataCatGroup(fileType))
    variables.setVar(fileType, 'site', fileNames.getSite(fileName))
    variables.setVar(fileType, 'fileName', fileName)
    # variables.setVar(fileType, 'creator', creator) # remove me!

    return
