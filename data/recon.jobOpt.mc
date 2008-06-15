#include "$GLEAMROOT/src/jobOptions/pipeline/readigi_runrecon.txt"
digiRootReaderAlg.digiRootFileList = { "$digiChunkFile" } ;
//RootIoSvc.StartingIndex = $crumbStart;
//ApplicationMgr.EvtMax = $crumbEvents;
reconRootWriterAlg.reconRootFile = "$reconCrumbFile";
RootTupleSvc.filename = "$meritCrumbFile";
CalTupleAlg.tupleFilename = "$calCrumbFile";
gcrSelectRootWriterAlg.gcrSelectRootFile = "$gcrCrumbFile";
PtValsAlg.PointingHistory = {"$fakeFT2File","", ""};
GlastDetSvc.xmlfile = "$(XMLGEODBSROOT)/xml/$(gleamGeometry)";

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
OnboardFilter.FileNamePeds        = "cal_db_pedestals_flight";
OnboardFilter.FileNameGains       = "cal_db_gains_flight";
OnboardFilter.DgnConfig           = "DGN_gem";

GcrReconAlg.HFC_Or_TriggerEng4 = "TriggerEng4";

CalibDataSvc.CalibFlavorList = {"vanilla","ideal","MC_OktoberFest07"};

// New Cal calib:
CalTupleAlg.NeighborXtalkToolName   = "NeighborXtalkTool";
CalXtalRecAlg.NeighborXtalkToolName= "NeighborXtalkTool";
ToolSvc.NeighborXtalkTool.txtFile="$(LATCalibRoot)/CAL/LAT-flight_gain/pre_launch_calib_0608/digitization-licos-v3r9p12_077015240_digi_DIGI.neighborXtalk.txt";
