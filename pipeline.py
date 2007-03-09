#!/usr/bin/env python

"""@brief interface to pipeline functions.
"""

import os

def setVariable(varName, value):
    # use bash function
    cmd = 'pipelineSet %s %s' % (varName, value)
    status = os.system(cmd)
    return status

def createSubStream(subTask, stream=0, args=''):
    cmd = 'pipelineCreateStream %s %s %s' % (subTask, stream, args)
    status = os.system(cmd)
    return status
