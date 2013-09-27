#include "$GLEAMJOBOPTIONSPATH/jobOptions/pipeline/readigi_runrecon.txt"
digiRootReaderAlg.digiRootFileList = { "$digiChunkFile" } ;
//RootIoSvc.StartingIndex = $crumbStart;
//ApplicationMgr.EvtMax = $crumbEvents;
reconRootWriterAlg.reconRootFile = "$reconCrumbFile";
RootTupleSvc.filename = "$meritCrumbFile";
CalTupleAlg.tupleFilename = "$calCrumbFile";
gcrSelectRootWriterAlg.gcrSelectRootFile = "$gcrCrumbFile";
PtValsAlg.PointingHistory = {"$fakeFT2File","", ""};

AcdCalibSvc.DefaultFlavor = "MC_OktoberFest07";

CalibMySQLCnvSvc.DbName           = "calib";
CalibMySQLCnvSvc.QualityList      = {"PROD"};
AcdCalibSvc.DefaultFlavor         = "MC_OktoberFest07";
AcdCalibSvc.FlavorHighRange       = "ideal";
AcdCalibSvc.FlavorCoherentNoise   = "ideal";
TkrCalibAlg.calibFlavor           = "MC_OktoberFest07";
TkrCalibAlg.deadStripsCalibFlavor = "MC_OktoberFest07";
TkrSplitsSvc.defaultMaxStrips     = "14";
CalCalibSvc.DefaultFlavor         = "MC_OktoberFest07";

CalibDataSvc.CalibFlavorList = {"vanilla","ideal","MC_OktoberFest07"};
