#include "$GLEAMROOT/src/jobOptions/pipeline/ldf2digi.txt"
EventSelector.StorageType = "CCSDSFILE";
EventSelector.FileName = "$EVTFILE";
digiRootWriterAlg.digiRootFile = "$digiChunkFile";
GlastDetSvc.xmlfile = "$(XMLGEODBSROOT)/xml/$(gleamGeometry)";

TrgConfigSvc.configureFrom = "$trigConfig";

OnboardFilter.FilterList = {0,1,2,3};

CalibMySQLCnvSvc.DbName           = "calib";
CalibMySQLCnvSvc.QualityList      = {"PROD"};
AcdCalibSvc.DefaultFlavor         = "MC_OktoberFest07";
AcdCalibSvc.FlavorHighRange       = "ideal";
AcdCalibSvc.FlavorCoherentNoise   = "ideal";
TkrCalibAlg.calibFlavor           = "MC_OktoberFest07";
TkrCalibAlg.deadStripsCalibFlavor = "MC_OktoberFest07";
TkrSplitsSvc.defaultMaxStrips     = "14";
CalibDataSvc.CalibFlavorList      = {"ideal", "MC_OktoberFest07"};
CalCalibSvc.DefaultFlavor         = "MC_OktoberFest07";
OnboardFilter.FileNamePeds        = "cal_db_pedestals_flight";
OnboardFilter.FileNameGains       = "cal_db_gains_flight";
OnboardFilter.DgnConfig           = "DGN_gem";
