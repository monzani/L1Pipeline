#!/usr/bin/env python

import os
import sys

import config

import fileNames
import runner
import stageFiles

staged = stageFiles.StageSet()

reportType = os.environ(reportType)
app = config.ingestor[reportType]

cmd = ''

status = runner.run(cmd)

staged.finish()

sys.exit(status)
