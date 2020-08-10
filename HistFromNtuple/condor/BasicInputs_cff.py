#-----------------------------------------------------------------
condorHistDir = "/home/rverma/t3store/TTGammaSemiLep13TeV/Output"
#-----------------------------------------------------------------
#Year 	      =	["2016", "2017", "2018"]
Year 	      =	["2016"]
#Channel 	  =	["Mu", "Ele"]
#Decay 	  =	["SemiLep", "DiLep"]
Decay 	  =	["SemiLep"]
Channel 	  =	["Mu"]
SampleList    =	["TTGamma", "TTbar", "TGJets", "WJets", "ZJets", "WGamma", "ZGamma", "Diboson", "SingleTop", "TTV","GJets"]
#SampleList    =	["TTGamma", "TTbar"]
SampleListEle = SampleList + ["QCDEle", "DataEle", "QCD_DD"]
SampleListMu  = SampleList + ["QCDMu", "DataMu", "QCD_DD"]
Systematics   =	["PU","MuEff","PhoEff","BTagSF_b","BTagSF_l","EleEff","Q2","Pdf","isr","fsr"]
#Systematics   =	["PU","MuEff","PhoEff"]
SystLevel     = ["Up", "Down"]
ControlRegion = ["tight_a4j_a1b", "looseCR_a2j_e1b",]
#ControlRegion=["tight_a4j_a1b", "veryTight_a4j_a2b", "tight_a4j_e0b", "looseCR_a2j_e1b", "looseCR_a2j_a0b", "looseCR_a2j_e0b", "looseCR_e3j_a2b", "looseCR_e3j_e0b", "looseCR_e2j_e1b", "looseCR_e2j_e0j", "looseCR_e2j_e2b", "looseCR_e3j_e1b"]
