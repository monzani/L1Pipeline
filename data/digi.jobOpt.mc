#include "$GLEAMJOBOPTIONSPATH/jobOptions/pipeline/ldf2digi.txt"
EventSelector.StorageType = "CCSDSFILE";
EventSelector.FileName = "$EVTFILE";
digiRootWriterAlg.digiRootFile = "$digiChunkFile";
GlastDetSvc.xmlfile = "$(XMLGEODBSXMLPATH)/$(gleamGeometry)";

CalibMySQLCnvSvc.DbName           = "calib";
CalibMySQLCnvSvc.QualityList      = {"PROD"};
AcdCalibSvc.DefaultFlavor         = "MC_OktoberFest07";
AcdCalibSvc.FlavorHighRange       = "ideal";
AcdCalibSvc.FlavorCoherentNoise   = "ideal";
TkrCalibAlg.calibFlavor           = "MC_OktoberFest07";
TkrCalibAlg.deadStripsCalibFlavor = "MC_OktoberFest07";
TkrSplitsSvc.defaultMaxStrips     = "14";
CalCalibSvc.DefaultFlavor         = "MC_OktoberFest07";
ToolSvc.FSWAuxLibsTool.FileNamePeds="cal_db_pedestals";
ToolSvc.FSWAuxLibsTool.FileNameGains="cal_db_gains";

CalibDataSvc.CalibFlavorList      = {"ideal", "MC_OktoberFest07"};

//MootSvc.ExitOnFatal = false;  // Allow MootSvc to continue if the MOOT key isn't found
