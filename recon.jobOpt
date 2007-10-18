#include "$GLEAMROOT/src/jobOptions/pipeline/readigi_runrecon.txt"
digiRootReaderAlg.digiRootFileList = { "$digiChunkFile" } ;
RootIoSvc.StartingIndex = $crumbStart;
ApplicationMgr.EvtMax = $crumbEvents;
reconRootWriterAlg.reconRootFile = "$reconCrumbFile";
RootTupleSvc.filename = "$meritCrumbFile";
CalTupleAlg.tupleFilename = "$calCrumbFile";
gcrSelectRootWriterAlg.gcrSelectRootFile = "$gcrCrumbFile";
PtValsAlg.PointingHistory = {"$fakeFT2File","", ""};
GlastDetSvc.xmlfile = "$(XMLGEODBSROOT)/xml/$(gleamGeometry)";

TkrCalibAlg.calibFlavor   = "MC_OktoberFest07";
CalCalibSvc.DefaultFlavor = "MC_OktoberFest07";
AcdCalibSvc.DefaultFlavor = "MC_OktoberFest07-L1Proc-recon";
CalibDataSvc.CalibFlavorList = {"MC_OktoberFest07","MC_OktoberFest07-L1Proc-recon"};
