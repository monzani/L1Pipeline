
import PipelineNetlogger

import config

log = PipelineNetlogger.Netlogger(config.netlogDest, config.netlogLevel)
log.info(
    "logging.test",
    "From a pipeline batch job",
    "Anything",
    lattime(0, 0),
    config.scid,
    )
