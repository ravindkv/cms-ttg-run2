from ROOT import TH1F, TFile, TChain, TCanvas, gDirectory 
import sys
import os
from optparse import OptionParser
from SampleInfo_cff import *
from HistListDict_cff import *

#-----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016",type='str',
                     help="Specifyi the year of the data taking" )
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
                     help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-s", "--sample", dest="sample", default="",type='str',
                     help="Specify which sample to run on" )
parser.add_option("--level", "--level", dest="level", default="",type='str',
                     help="Specify up/down of systematic")
parser.add_option("--syst", "--systematic", dest="systematic", default="Base",type='str',
		     help="Specify which systematic to run on")
parser.add_option("--Tight","--tight", dest="isTightSelection", default=False,action="store_true",
                     help="Use 4j1t selection" )
parser.add_option("--VeryTight","--verytight", dest="isVeryTightSelection", default=False,action="store_true",
                     help="Use 4j2t selection" )
parser.add_option("--Tight0b","--tight0b", dest="isTightSelection0b", default=False,action="store_true",
                     help="Use 4j0t selection" )
parser.add_option("--LooseCR2e1","--looseCR2e1", dest="isLooseCR2e1Selection",default=False,action="store_true",
		  help="Use 2j exactly 1t control region selection" )
parser.add_option("--LooseCRe2g1","--looseCRe2g1", dest="isLooseCRe2g1Selection",default=False,action="store_true",
                  help="Use exactly 2j >= 1t control region selection" )
parser.add_option("--LooseCR3g0","--looseCR3g0", dest="isLooseCR3g0Selection",default=False,action="store_true",
		  help="Use >=3j and 0btag control region selection" )
parser.add_option("--LooseCR2g1","--looseCR2g1", dest="isLooseCR2g1Selection",default=False,action="store_true",
                  help="Use 2j at least 1t control region selection")
parser.add_option("--LooseCRe3g1","--looseCRe3g1", dest="isLooseCRe3g1Selection",default=False,action="store_true",
		  help="Use exactly 3j >= 1t control region selection" )
parser.add_option("--addPlots","--addOnly", dest="onlyAddPlots", default=False,action="store_true",
                     help="Use only if you want to add a couple of plots to the file, does not remove other plots" )
parser.add_option("--plot", dest="plotList",action="append",
                     help="Add plots" )
parser.add_option("--multiPlots", "--multiplots", dest="multiPlotList",action="append",
                     help="Add plots" )
parser.add_option("--testPlot", "--testPlot", dest="testPlot",action="store_true",default=False,
                     help="test one plot without replacing it in the original one" )
parser.add_option("--allPlots","--AllPlots", dest="makeAllPlots",action="store_true",default=False,
                     help="Make full list of plots in histogramDict" )
parser.add_option("--morePlots","--MorePlots","--makeMorePlots", dest="makeMorePlots",action="store_true",default=False,
                     help="Make larger list of plots in histogramDict (mostly object kinematics)" )
parser.add_option("--EgammaPlots","--EgammaPlots", dest="makeEGammaPlots",action="store_true",default=False,
                     help="Make only plots for e-gamma mass fits" )
parser.add_option("--dRPlots","--dRPlots", dest="makedRPlots",action="store_true",default=False,
                     help="Make only plots for dR" )
parser.add_option("--genPlots","--genPlots", dest="makegenPlots",action="store_true",default=False,
                     help="Make only plots for 2D histograms" )
parser.add_option("--jetsonly","--jetsonly", dest="makeJetsplots",action="store_true",default=False,
                     help="Extra jets" )
parser.add_option("--dilepmassPlots","--dilepmassPlots", dest="Dilepmass",action="store_true",default=False,
                     help="Make only plots for ZJetsSF fits" )
parser.add_option("--quiet", "-q", dest="quiet",default=False,action="store_true",
                     help="Quiet outputs" )
parser.add_option("--fwdjets","--fwdjets", dest="FwdJets",action="store_true",default=False,
                     help="include fwd jets" )

(options, args) = parser.parse_args()
level =options.level
Dilepmass=options.Dilepmass
year = options.year
channel = options.channel
sample = options.sample
testPlot=options.testPlot
isVeryTightSelection=options.isVeryTightSelection
isTightSelection = options.isTightSelection
isTightSelection0b = options.isTightSelection0b
#isLooseCRe2g1Selection=options.isLooseCRe2g1Selection
isLooseCR2e1Selection = options.isLooseCR2e1Selection
isLooseCRe2g1Selection = options.isLooseCRe2g1Selection
isLooseCR3g0Selection=options.isLooseCR3g0Selection
isLooseCRe2g1Selection = options.isLooseCRe2g1Selection
isLooseCRe3g1Selection = options.isLooseCRe3g1Selection
onlyAddPlots = options.onlyAddPlots
FwdJets=options.FwdJets
makedRPlots=options.makedRPlots
makeAllPlots = options.makeAllPlots
makeMorePlots = options.makeMorePlots
makeEGammaPlots = options.makeEGammaPlots
makeJetsplots = options.makeJetsplots
makegenPlots=options.makegenPlots
runQuiet = options.quiet
toPrint("Runing for Year, Channel, Sample", "%s, %s, %s"%(year, channel, sample))
print parser.parse_args()

#-----------------------------------------
#INPUT AnalysisNtuples Directory
#----------------------------------------
ntupleDirBase = "root://cmseos.fnal.gov//store/user/lpctop/TTGamma_FullRun2/AnalysisNtuples/%s/"%year
ntupleDirBaseDiLep = "root://cmseos.fnal.gov//store/user/lpctop/TTGamma_FullRun2/AnalysisNtuples/Dilepton/%s/"%year
ntupleDirBaseCR = "root://cmseos.fnal.gov//store/user/lpctop/TTGamma_FullRun2/AnalysisNtuples/QCD_controlRegion/%s/"%year
ntupleDirSyst = "root://cmseos.fnal.gov//store/user/lpctop/TTGamma_FullRun2/AnalysisNtuples/Systematics/%s/"%year
ntupleDirSystCR = "root://cmseos.fnal.gov//store/user/lpctop/TTGamma_FullRun2/AnalysisNtuples/QCD_controlRegion/Systematics/%s/"%year

#-----------------------------------------
#OUTPUT Histogram Directory
#----------------------------------------
#outputPath = "/home/rverma/t3store/TTGammaSemiLep13TeV/CMSSW_10_2_5/src/TTGamma/Plotting" 
outputPath = "."

#-----------------------------------------
#----------------------------------------
gROOT.SetBatch(True)
dir2=""
if FwdJets:
	dir2="_fwd"
nJets = 3
nBJets = 1
isQCD = False
dir_=""
Q2 = 1.
Pdf = 1.
Pileup ="PUweight"
MuEff = "muEffWeight"
EleEff= "eleEffWeight"
PhoEff= "phoEffWeight"
loosePhoEff= "loosePhoEffWeight"
evtWeight ="evtWeight"
btagWeightCategory = ["1","(1-btagWeight[0])","(btagWeight[2])","(btagWeight[1])"]
ttbarDecayMode = "SemiLep"
if testPlot:
	ttbarDecayMode="Test"
histDirInFile = "Base"

#-----------------------------------------
#For Systematics
#----------------------------------------
syst = options.systematic
if (syst=="isr" or syst=="fsr") and sample=="TTbar":
		samples={"TTbar"     : [["TTbarPowheg_Semilept_2016_AnalysisNtuple_1of5.root", 
			"TTbarPowheg_Semilept_2016_AnalysisNtuple_2of5.root",
			"TTbarPowheg_Semilept_2016_AnalysisNtuple_3of5.root", 
			"TTbarPowheg_Semilept_2016_AnalysisNtuple_4of5.root", 
			"TTbarPowheg_Semilept_2016_AnalysisNtuple_5of5.root"],
                          kRed+1,"t#bar{t}",isMC],
			}
levelUp = False
if level in ["up", "UP", "uP", "Up"]: 
	levelUp = True
	level= "Up"
else:
	level = "Down"
if not syst=="Base":
    histDirInFile = "%s%s"%(syst,level) 
    toPrint("Running for systematics", syst+level)
    if syst=="PU":
        if levelUp:
                Pileup = "PUweight_Up"
        else:
                    Pileup = "PUweight_Do"
    elif 'Q2' in syst:
        if levelUp:
                Q2="q2weight_Up"
        else:
                Q2="q2weight_Do"
    elif 'Pdf' in syst:
    	if syst=="Pdf":

    	    if levelUp:
    	    	Pdf="pdfweight_Up"
    	    else:
    	    	Pdf="pdfweight_Do"
    	else:
    	    if type(eval(syst[3:]))==type(int()):
    	    	pdfNumber = eval(syst[3:])
    	    	Pdf="pdfSystWeight[%i]/pdfWeight"%(pdfNumber-1)
    elif 'MuEff' in syst:
        if levelUp:
            MuEff = "muEffWeight_Up"
        else:
            MuEff = "muEffWeight_Do"
    elif 'EleEff' in syst:
        if levelUp:
            EleEff = "eleEffWeight_Up"
        else:
            EleEff = "eleEffWeight_Do"
    elif 'PhoEff' in syst:
       if levelUp:
           PhoEff = "phoEffWeight_Up"
           loosePhoEff = "loosePhoEffWeight_Up"
       else:
           PhoEff = "phoEffWeight_Do"
           loosePhoEff = "loosePhoEffWeight_Do"
    elif 'BTagSF_b' in syst:
        if levelUp:
            btagWeightCategory = ["1","(1-btagWeight_b_Up[0])","(btagWeight_b_Up[2])","(btagWeight_b_Up[1])"]
        else:
            btagWeightCategory = ["1","(1-btagWeight_b_Do[0])","(btagWeight_b_Do[2])","(btagWeight_b_Do[1])"]
    elif 'BTagSF_l' in syst:
        if levelUp:
            btagWeightCategory = ["1","(1-btagWeight_l_Up[0])","(btagWeight_l_Up[2])","(btagWeight_l_Up[1])"]
        else:
            btagWeightCategory = ["1","(1-btagWeight_l_Do[0])","(btagWeight_l_Do[2])","(btagWeight_l_Do[1])"]
    else:
    	if  levelUp:
            analysisNtupleLocation = ntupleDirSyst+"/%s_up_"%(syst)
    	else:
            analysisNtupleLocation = ntupleDirSyst+"/%s_down_"%(syst)

if channel=="Mu":
    sampleList[-1] = "DataMu"
    sampleList[-2] = "QCDMu"
    if sample=="Data":
        sample = "DataMu"
    if sample=="QCD":
        sample = "QCDMu"
    analysisNtupleLocation = ntupleDirBase
    outputhistName = outputPath+"/hists/%s/%s/Mu"%(year,ttbarDecayMode)
    extraCuts            = "(passPresel_Mu && nJet>=3 && nBJet>=1)*"
    extraPhotonCuts      = "(passPresel_Mu && nJet>=3 && nBJet>=1 && %s)*"

    extraCutsTight       = "(passPresel_Mu && nJet>=4 && nBJet>=1)*"
    extraPhotonCutsTight = "(passPresel_Mu && nJet>=4 && nBJet>=1 && %s)*"
    
    extraCutsVeryTight       = "(passPresel_Mu && nJet>=4 && nBJet>=2)*"
    extraPhotonCutsVeryTight = "(passPresel_Mu && nJet>=4 && nBJet>=2 && %s)*"
    
    extraCutsTight0b       = "(passPresel_Mu && nJet>=4 && nBJet==0)*"
    extraPhotonCutsTight0b = "(passPresel_Mu && nJet>=4 && nBJet==0 && %s)*"

    extraCutsLooseCR2e1       = "(passPresel_Mu && nJet>=2 && nBJet==1)*"
    extraPhotonCutsLooseCR2e1 = "(passPresel_Mu && nJet>=2 && nBJet==1 && %s)*"

    extraCutsLooseCR2g1       = "(passPresel_Mu && nJet==2 && nBJet>=1)*"
    extraPhotonCutsLooseCR2g1 = "(passPresel_Mu && nJet==2 && nBJet>=1 && %s)*"

    extraCutsLooseCR2e0       = "(passPresel_Mu && nJet>=2)*"
    extraPhotonCutsLooseCR2e0 = "(passPresel_Mu && nJet>=2 && %s)*"

    extraCutsLooseCRe3g1       = "(passPresel_Mu && nJet==3 && nBJet>=1)*"
    extraPhotonCutsLooseCRe3g1 = "(passPresel_Mu && nJet==3 && nBJet>=1 && %s)*"


    extraCutsLooseCRe3g0       = "(passPresel_Mu && nJet>=3 && nBJet==0)*"
    extraPhotonCutsLooseCRe3g0 = "(passPresel_Mu && nJet>=3 && nBJet==0 && %s)*"

elif channel=="Ele":
    sampleList[-1] = "DataEle"
    sampleList[-2] = "QCDEle"
    if sample=="Data":
        sample = "DataEle"
    if sample=="QCD":
        sample = "QCDEle"
    analysisNtupleLocation = ntupleDirBase 
    outputhistName = outputPath+"/hists/%s/%s/Ele"%(year,ttbarDecayMode)
    extraCuts            = "(passPresel_Ele && nJet>=3 && nBJet>=1)*"
    extraPhotonCuts      = "(passPresel_Ele && nJet>=3 && nBJet>=1 && %s)*"

    extraCutsTight       = "(passPresel_Ele && nJet>=4 && nBJet>=1)*"
    extraPhotonCutsTight = "(passPresel_Ele && nJet>=4 && nBJet>=1 && %s)*"
    
    extraCutsVeryTight       = "(passPresel_Ele && nJet>=4 && nBJet>=2)*"
    extraPhotonCutsVeryTight = "(passPresel_Ele && nJet>=4 && nBJet>=2 && %s)*"

    
    extraCutsTight0b       = "(passPresel_Ele && nJet>=4 && nBJet==0)*"
    extraPhotonCutsTight0b = "(passPresel_Ele && nJet>=4 && nBJet==0 && %s)*"

    extraCutsLooseCR2e1       = "(passPresel_Ele && nJet>=2 && nBJet==1)*"
    extraPhotonCutsLooseCR2e1 = "(passPresel_Ele && nJet>=2 && nBJet==1 && %s)*"

    extraCutsLooseCR2g0       = "(passPresel_Ele && nJet==2)*"
    extraPhotonCutsLooseCR2g0 = "(passPresel_Ele && nJet==2 && %s)*"

    extraCutsLooseCR2g1       = "(passPresel_Ele && nJet==2 && nBJet>=1)*"
    extraPhotonCutsLooseCR2g1 = "(passPresel_Ele && nJet==2 && nBJet>=1 && %s)*"

    extraCutsLooseCR2e0       = "(passPresel_Ele && nJet>=2)*"
    extraPhotonCutsLooseCR2e0 = "(passPresel_Ele && nJet>=2 && %s)*"

    extraCutsLooseCRe3g1       = "(passPresel_Ele && nJet==3 && nBJet>=1)*"
    extraPhotonCutsLooseCRe3g1 = "(passPresel_Ele && nJet==3 && nBJet>=1 && %s)*"

    
    extraCutsLooseCRe3g0       = "(passPresel_Ele && nJet>=3 && nBJet==0)*"
    extraPhotonCutsLooseCRe3g0 = "(passPresel_Ele && nJet>=3 && nBJet==0 && %s)*"

elif channel=="DiMu":
    sampleList[-1] = "DataMu"
    sampleList[-2] = "QCDMu"

    if sample=="Data":
        sample = "DataMu"
    if sample=="QCD":
        sample = "QCDMu"
    analysisNtupleLocation = ntupleDirBaseDiLep
    ttbarDecayMode = "DiLep"
    outputhistName = outputPath+"/hists/%s/%s/Mu"%(year,ttbarDecayMode)

    extraCuts            = "(passPresel_Mu && nJet>=3 && nBJet>=1)*"
    extraPhotonCuts      = "(passPresel_Mu && nJet>=3 && nBJet>=1 && %s)*"

    extraCutsTight       = "(passPresel_Mu && nJet>=4 && nBJet>=1)*"
    extraPhotonCutsTight = "(passPresel_Mu && nJet>=4 && nBJet>=1 && %s)*"

    extraCutsTight0b       = "(passPresel_Mu && nJet>=4 && nBJet==0)*"
    extraPhotonCutsTight0b = "(passPresel_Mu && nJet>=4 && nBJet==0 && %s)*"


    extraCutsLooseCR2e1       = "(passPresel_Mu && nJet>=2 && nBJet==1)*"
    extraPhotonCutsLooseCR2e1 = "(passPresel_Mu && nJet>=2 && nBJet==1 && %s)*"

    extraCutsLooseCR2e0       = "(passPresel_Mu && nJet==2)*"
    extraPhotonCutsLooseCR2e0 = "(passPresel_Mu && nJet==2 && %s)*"

    extraCutsLooseCR2g0       = "(passPresel_Mu && nJet>=2)*"
    extraPhotonCutsLooseCR2g0 = "(passPresel_Mu && nJet>=2 && %s)*"

    extraCutsLooseCR2g1       = "(passPresel_Mu && nJet==2 && nBJet>=1)*"
    extraPhotonCutsLooseCR2g1 = "(passPresel_Mu && nJet==2 && nBJet>=1 && %s)*"

    extraCutsLooseCR3g0       = "(passPresel_Mu && nJet>=3 && nBJet>=0)*"
    extraPhotonCutsLooseCR3g0 = "(passPresel_Mu && nJet>=3 && nBJet>=0 && %s)*"
 
    extraCutsLooseCRe3g1       = "(passPresel_Mu && nJet==3 && nBJet>=1)*"
    extraPhotonCutsLooseCRe3g1 = "(passPresel_Mu && nJet==3 && nBJet>=1 && %s)*"


    extraCutsLooseCRe3g0       = "(passPresel_Mu && nJet>=3 && nBJet==0)*"
    extraPhotonCutsLooseCRe3g0 = "(passPresel_Mu && nJet>=3 && nBJet==0 && %s)*"

elif channel=="DiEle":
    sampleList[-1] = "DataEle"
    sampleList[-2] = "QCDEle"
    if sample=="Data":
        sample = "DataEle"
    if sample=="QCD":
        sample = "QCDEle"
    analysisNtupleLocation = ntupleDirBaseDiLep 
    outputhistName = outputPath+"/hists/%s/%s/Ele"%(year,ttbarDecayMode)

    extraCuts            = "(passPresel_Ele && nJet>=3 && nBJet>=1)*"
    extraPhotonCuts      = "(passPresel_Ele && nJet>=3 && nBJet>=1 && %s)*"

    extraCutsTight       = "(passPresel_Ele && nJet>=4 && nBJet>=1)*"
    extraPhotonCutsTight = "(passPresel_Ele && nJet>=4 && nBJet>=1 && %s)*"

    extraCutsTight0b       = "(passPresel_Ele && nJet>=4 && nBJet==0)*"
    extraPhotonCutsTight0b = "(passPresel_Ele && nJet>=4 && nBJet==0 && %s)*"

    extraCutsLooseCR2e1       = "(passPresel_Ele && nJet>=2 && nBJet==1)*"
    extraPhotonCutsLooseCR2e1 = "(passPresel_Ele && nJet>=2 && nBJet==1 &&%s)*"

    extraCutsLooseCR2g1       = "(passPresel_Ele && nJet==2 && nBJet>=1)*"
    extraPhotonCutsLooseCR2g1 = "(passPresel_Ele && nJet==2 && nBJet>=1 && %s)*"

    extraCutsLooseCR2g0       = "(passPresel_Ele && nJet>=2)*"
    extraPhotonCutsLooseCR2g0 = "(passPresel_Ele && nJet>=2 && %s)*"

    extraCutsLooseCRe3g1       = "(passPresel_Ele && nJet==3 && nBJet>=1)*"
    extraPhotonCutsLooseCRe3g1 = "(passPresel_Ele && nJet==3 && nBJet>=1 && %s)*"


    extraCutsLooseCRe3g0       = "(passPresel_Ele && nJet>=3 && nBJet==0)*"
    extraPhotonCutsLooseCRe3g0 = "(passPresel_Ele && nJet>=3 && nBJet==0 && %s)*"

elif channel=="QCDMu":
    sampleList[-1] = "DataMu"
    sampleList[-2] = "QCDMu"
    if sample=="Data":
        sample = "DataMu"
    if sample=="QCD":
        sample = "QCDMu"
    isQCD = True
    analysisNtupleLocation = ntupleDirBaseCR 
    outputhistName = outputPath+"/hists/%s/%s/Mu/CR/"%(year,ttbarDecayMode)

    nBJets = 0
    extraCuts            = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=3 && nBJet==0)*"
    extraPhotonCuts      = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=3 && nBJet==0 && %s)*"

    extraCutsTight            = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=4 && nBJet==0)*"
    extraPhotonCutsTight      = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=4 && nBJet==0 && %s)*"

    extraCutsVeryTight       = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=4 && nBJet==0)*"
    extraPhotonCutsVeryTight = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=4 && nBJet==0 && %s)*"

    extraCutsTight0b            = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=4 && nBJet==0)*"
    extraPhotonCutsTight0b      = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=4 && nBJet==0 && %s)*"

    extraCutsLooseCR2e1       = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=2 && nBJet==0)*"
    extraPhotonCutsLooseCR2e1 = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=2 && nBJet==0 && %s)*"

    extraCutsLooseCR2e0       = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=2 && nBJet==0)*"
    extraPhotonCutsLooseCR2e0 = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=2 && nBJet==0 && %s)*"

    extraCutsLooseCR2g0       = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=2 && nBJet==0)*"
    extraPhotonCutsLooseCR2g0 = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=2 && nBJet==0 && %s)*"
    
    extraCutsLooseCR2g1       = "(passPresel_Mu && muPFRelIso<0.3 && nJet==2 && nBJet==0)*"
    extraPhotonCutsLooseCR2g1 = "(passPresel_Mu && muPFRelIso<0.3 && nJet==2 && nBJet==0 && %s)*"

    extraCutsLooseCRe3g1       = "(passPresel_Mu && muPFRelIso<0.3 && nJet==3 && nBJet==0)*"
    extraPhotonCutsLooseCRe3g1 = "(passPresel_Mu && muPFRelIso<0.3 && nJet==3 && nBJet==0 && %s)*"

    extraCutsLooseCRe3g0       = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=3 && nBJet==0)*"
    extraPhotonCutsLooseCRe3g0 = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=3 && nBJet==0 && %s)*"


elif channel=="QCDMu2":
    sampleList[-1] = "DataMu"
    sampleList[-2] = "QCDMu"
    if sample=="Data":
        sample = "DataMu"
    if sample=="QCD":
        sample = "QCDMu"
    isQCD = True
    analysisNtupleLocation = ntupleDirBaseCR
    outputhistName = outputPath+"/hists/%s/%s/Mu/CR2"%(year,ttbarDecayMode)

    nBJets = 0
    extraCuts            = "(passPresel_Mu && muPFRelIso>0.3 && nJet>=3 && nBJet==0)*"
    extraPhotonCuts      = "(passPresel_Mu && muPFRelIso>0.3 && nJet>=3 && nBJet==0 && %s)*"

    extraCutsTight            = "(passPresel_Mu && muPFRelIso>0.3 && nJet>=4 && nBJet==0)*"
    extraPhotonCutsTight      = "(passPresel_Mu && muPFRelIso>0.3 && nJet>=4 && nBJet==0 && %s)*"

    extraCutsTight0b            = "(passPresel_Mu && muPFRelIso>0.3 && nJet>=4 && nBJet==0)*"
    extraPhotonCutsTight0b      = "(passPresel_Mu && muPFRelIso>0.3 && nJet>=4 && nBJet==0 && %s)*"

    extraCutsLoose            = "(passPresel_Mu && muPFRelIso>0.3 && nJet>=2 && nBJet==0)*"
    extraPhotonCutsLoose      = "(passPresel_Mu && muPFRelIso>0.3 && nJet>=2 && nBJet==0 && %s)*"

    extraCutsLooseCR          = "(passPresel_Mu && muPFRelIso>0.3 && nJet>=2 && nBJet==0)*"
    extraPhotonCutsLooseCR    = "(passPresel_Mu && muPFRelIso>0.3 && nJet>=2 && nBJet==0 && %s)*"

elif channel=="QCDEle":
    sampleList[-1] = "DataEle"
    sampleList[-2] = "QCDEle"
    if sample=="Data":
        sample = "DataEle"
    if sample=="QCD":
        sample = "QCDEle"
    analysisNtupleLocation = ntupleDirBaseCR 
    outputhistName = outputPath+"/hists/%s/%s/Ele/CR"%(year,ttbarDecayMode)
    toPrint("Full Path of Hist", outputhistName)

    isQCD = True

    nBJets = 0

    extraCuts                 = "(passPresel_Ele && elePFRelIso>0.01 && nJet>=3 && nBJet==0)*"
    extraPhotonCuts           = "(passPresel_Ele && elePFRelIso>0.01 && nJet>=3 && nBJet==0 && %s)*"

    extraCutsTight            = "(passPresel_Ele && elePFRelIso>0.01 && nJet>=4 && nBJet==0)*"
    extraPhotonCutsTight      = "(passPresel_Ele && elePFRelIso>0.01 && nJet>=4 && nBJet==0 && %s)*"

    extraCutsVeryTight       = "(passPresel_Ele && elePFRelIso>0.01 && nJet>=4 && nBJet==0)*"
    extraPhotonCutsVeryTight = "(passPresel_Ele && elePFRelIso>0.01 && nJet>=4 && nBJet==0 && %s)*"

    extraCutsTight0b            = "(passPresel_Ele && elePFRelIso>0.01 && nJet>=4 && nBJet==0)*"
    extraPhotonCutsTight0b      = "(passPresel_Ele && elePFRelIso>0.01 && nJet>=4 && nBJet==0 && %s)*"

    extraCutsLoose            = "(passPresel_Ele && elePFRelIso>0.01 && nJet>=2 && nBJet==0)*"
    extraPhotonCutsLoose      = "(passPresel_Ele && elePFRelIso>0.01 && nJet>=2 && nBJet==0 && %s)*"

    extraCutsLooseCR2e1       = "(passPresel_Ele && elePFRelIso>0.01 && nJet>=2 && nBJet==0)*"
    extraPhotonCutsLooseCR2e1 = "(passPresel_Ele && elePFRelIso>0.01 && nJet>=2 && nBJet==0 && %s)*"

    extraCutsLooseCR2g1       = "(passPresel_Ele && elePFRelIso>0.01 && nJet==2 && nBJet==0)*"
    extraPhotonCutsLooseCR2g1 = "(passPresel_Ele && elePFRelIso>0.01 && nJet==2 && nBJet==0 && %s)*"

    extraCutsLooseCR          = "(passPresel_Ele && elePFRelIso>0.01 && nJet>=2 && nBJet==0)*"
    extraPhotonCutsLooseCR    = "(passPresel_Ele && elePFRelIso>0.01 && nJet>=2 && nBJet==0 && %s)*"


    extraCutsLooseCRe3g1       = "(passPresel_Ele && elePFRelIso>0.01 && nJet==3 && nBJet==0)*"
    extraPhotonCutsLooseCRe3g1 = "(passPresel_Ele && elePFRelIso>0.01 && nJet==3 && nBJet==0 && %s)*"

    extraCutsLooseCRe3g0       = "(passPresel_Ele && elePFRelIso>0.01 && nJet>=3 && nBJet==0)*"
    extraPhotonCutsLooseCRe3g0 = "(passPresel_Ele && elePFRelIso>0.01 && nJet>=3 && nBJet==0 && %s)*"

else:
    print "Unknown final state, options are Mu and Ele"
    sys.exit()

if not os.path.exists(outputhistName):
    os.makedirs(outputhistName)
outputFile = TFile("%s/%s.root"%(outputhistName,sample),"update")
fullPath = "%s/%s.root"%(outputhistName,sample)


btagWeight = btagWeightCategory[nBJets]
signalOrCR = "SignalRegion"
if isTightSelection:
    if not runQuiet: toPrint("Control Region", "Tight")
    nJets = 4
    nBJets = 1
    btagWeight = btagWeightCategory[nBJets]
    # weights = "evtWeight*PUweight*muEffWeight*eleEffWeight*btagWeight[2]"
    extraCuts = extraCutsTight 
    extraPhotonCuts = extraPhotonCutsTight 
    signalOrCR = "ControlRegion/Tight"
    dir_="_tight"

if isVeryTightSelection:
    if not runQuiet: toPrint("Control Region", "Very Tight")
    nJets = 4
    nBJets = 2
    btagWeight = btagWeightCategory[nBJets]
   
    extraCuts = extraCutsVeryTight
    extraPhotonCuts = extraPhotonCutsVeryTight
    signalOrCR = "ControlRegion/VerytTight"
    dir_=""



if isTightSelection0b:
    if not runQuiet: toPrint("Control Region", "Very Tight")
    nJets = 4
    nBJets = 0
    btagWeight = btagWeightCategory[nBJets]
    # weights = "evtWeight*PUweight*muEffWeight*eleEffWeight*btagWeight[2]"
    extraCuts = extraCutsTight0b
    extraPhotonCuts = extraPhotonCutsTight0b
    signalOrCR = "ControlRegion/Tight0b"
    dir_="_tight0b"


if isLooseCR2e1Selection:
    if not runQuiet: print "Loose Control Region Select"
    nJets = 2
    nBJets = 1
    btagWeight = "(btagWeight[1])"
    #    weights = "evtWeight*PUweight*muEffWeight*eleEffWeight*btagWeight[1]"
    extraCuts = extraCutsLooseCR2e1
    extraPhotonCuts = extraPhotonCutsLooseCR2e1
    signalOrCR = "ControlRegion/LooseCR2e1"
    dir_="_looseCR2e1"

if isLooseCRe2g1Selection:
    if not runQuiet: print "Loose Control Region1 Select"
    nJets = 2
    nBJets = 1
    btagWeight = btagWeightCategory[nBJets]
    if 'QCD' in channel:
        btagWeight="1"
    # weights = "evtWeight*PUweight*muEffWeight*eleEffWeight*(1-btagWeight[0])"
    # if 'QCD' in channel:
    #     weights = "evtWeight*PUweight*muEffWeight*eleEffWeight"
    extraCuts = extraCutsLooseCR2g1
    extraPhotonCuts = extraPhotonCutsLooseCR2g1    
    signalOrCR = "ControlRegion/LooseCR2g1"
    dir_="_looseCRe2g1"

if isLooseCR3g0Selection:
    if not runQuiet: print "Loose Control Region for EGamma"
    nJets = 3
    nBJets = 0
    btagWeight = "btagWeight[0]" 
    if 'QCD' in channel:
       	btagWeight="1"
    extraCuts = extraCutsLooseCRe3g0
    extraPhotonCuts = extraPhotonCutsLooseCRe3g0
    signalOrCR = "ControlRegion/LooseCRe3g0"
    dir_="_looseCRe3g0"




if isLooseCRe3g1Selection:
    if not runQuiet: print "Loose Control Region Select"
    nJets = 3
    nBJets = 1
    btagWeight = btagWeightCategory[nBJets]
    #weights = "evtWeight*PUweight*muEffWeight*eleEffWeight*(btagWeight[0])"
    extraCuts = extraCutsLooseCRe3g1
    extraPhotonCuts = extraPhotonCutsLooseCRe3g1
    signalOrCR = "ControlRegion/LooseCRe3g1"
    dir_="_looseCRe3g1"

if "QCD" in channel:
	nBJets = 0
        btagWeight="btagWeight[0]"
weights = "%s*%s*%s*%s*%s*%s*%s"%(evtWeight,Pileup,MuEff,EleEff,Q2,Pdf,btagWeight)
toPrint("Extra cuts ", extraCuts)
toPrint("Extra photon cuts ", extraPhotonCuts)
toPrint("Final event weight ", weights)

histogramInfo = GetHistogramInfo(extraCuts,extraPhotonCuts,nBJets)
multiPlotList = options.multiPlotList
plotList = options.plotList
if plotList is None:
    if makeAllPlots:
        plotList = histogramInfo.keys()
        if not runQuiet: print "Making full list of plots"
    elif makeJetsplots:
	plotList = ["presel_jet2Pt","presel_jet3Pt", "presel_jet4Pt"]
    elif makeMorePlots:
        plotList = ["presel_Njet","phosel_SIEIE_barrel","phosel_SIEIE_GenuinePhoton_barrel","phosel_SIEIE_MisIDEle_barrel","phosel_SIEIE_NonPrompt_barrel","phosel_R9_barrel","phosel_elePt_barrel","phosel_elePt_GenuinePhoton_barrel","phosel_elePt_MisIDEle_barrel","phosel_elePt_NonPrompt_barrel","presel_elePt","phosel_muPt_barrel","phosel_muPt_GenuinePhoton_barrel","phosel_muPt_MisIDEle_barrel","phosel_muPt_NonPrompt_barrel","presel_muPt","phosel_eleSCEta_barrel","phosel_eleSCEta_GenuinePhoton_barrel","phosel_eleSCEta_MisIDEle_barrel","phosel_eleSCEta_NonPrompt_barrel","presel_eleSCEta","phosel_muEta_barrel","phosel_muEta_GenuinePhoton_barrel","phosel_muEta_MisIDEle_barrel","phosel_muEta_NonPrompt_barrel","presel_muEta","phosel_PhotonCategory_barrel","phosel_Njet_barrel","phosel_Njet_GenuinePhoton_barrel","phosel_Njet_MisIDEle_barrel","phosel_Njet_NonPrompt_barrel","presel_jet1Pt","phosel_jet1Pt_barrel","phosel_jet1Pt_GenuinePhoton_barrel","phosel_jet1Pt_MisIDEle_barrel","phosel_jet1Pt_NonPrompt_barrel","phosel_LeadingPhotonEt_barrel","phosel_LeadingPhotonEt_GenuinePhoton_barrel","phosel_LeadingPhotonEt_MisIDEle_barrel","phosel_LeadingPhotonEt_NonPrompt_barrel","phosel_LeadingPhotonEta_barrel","presel_M3_control","phosel_noCut_ChIso_barrel","phosel_noCut_SIEIE_barrel","phosel_noCut_SIEIE_GenuinePhoton_barrel","phosel_noCut_SIEIE_MisIDEle_barrel","phosel_noCut_SIEIE_NonPrompt_barrel","presel_nVtx","phosel_nVtx_barrel","presel_nVtxdo","presel_nVtxup","phosel_nVtxdo_barrel","phosel_nVtxup_barrel","presel_nVtxNoPU","phosel_nVtxNoPU_barrel","phosel_ChIso_barrel","phosel_ChIso_GenuinePhoton_barrel","phosel_ChIso_MisIDEle_barrel","phosel_ChIso_NonPrompt_barrel","phosel_NeuIso_barrel","phosel_NeuIso_GenuinePhoton_barrel","phosel_NeuIso_MisIDEle_barrel","phosel_NeuIso_NonPrompt_barrel","phosel_PhoIso_barrel","phosel_PhoIso_GenuinePhoton_barrel","phosel_PhoIso_MisIDEle_barrel","phosel_PhoIso_NonPrompt_barrel","phosel_HoverE_barrel","phosel_Nphotons_barrel","phosel_Nphotons_GenuinePhoton_barrel","phosel_Nphotons_MisIDEle_barrel","phosel_Nphotons_NonPrompt_barrel","phosel_LeadingPhotonSCEta_barrel", "phosel_LeadingPhotonSCEta_GenuinePhoton_barrel","phosel_LeadingPhotonSCEta_MisIDEle_barrel","phosel_LeadingPhotonSCEta_NonPrompt_barrel","phosel_noCut_SIEIE_noChIso_barrel","phosel_noCut_SIEIE_noChIso_GenuinePhoton_barrel","phosel_noCut_SIEIE_noChIso_MisIDEle_barrel","phosel_noCut_SIEIE_noChIso_NonPrompt_barrel","presel_HT","phosel_HT_barrel","phosel_HT_GenuinePhoton_barrel","phosel_HT_MisIDEle_barrel","phosel_HT_NonPrompt_barrel","presel_M3","phosel_noCut_ChIso_GenuinePhoton_barrel","phosel_noCut_ChIso_MisIDEle_barrel","phosel_noCut_ChIso_HadronicPhoton_barrel","phosel_noCut_ChIso_HadronicFake_barrel","phosel_M3","phosel_M3_barrel","phosel_M3_GenuinePhoton_barrel","phosel_M3_MisIDEle_barrel","phosel_M3_HadronicPhoton_barrel","phosel_M3_HadronicFake_barrel","phosel_M3_NonPrompt_barrel","phosel_AntiSIEIE_ChIso",
			"phosel_AntiSIEIE_ChIso_barrel","phosel_AntiSIEIE_ChIso_GenuinePhoton_barrel","phosel_AntiSIEIE_ChIso_HadronicPhoton_barrel","phosel_AntiSIEIE_ChIso_HadronicFake_barrel","phosel_AntiSIEIE_ChIso_MisIDEle_barrel","phosel_MassEGamma","phosel_MassEGammaMisIDEle","phosel_MassEGammaOthers","phosel_MassEGamma_barrel","phosel_MassEGamma_NonPrompt_barrel","phosel_MassEGamma_GenuinePhoton_barrel","phosel_MassEGamma_MisIDEle_barrel","phosel_MassEGammaOthers_barrel", "phosel_LeadingPhotonabsSCEta_barrel", "phosel_LeadingPhotonabsSCEta_GenuinePhoton_barrel","phosel_LeadingPhotonabsSCEta_MisIDEle_barrel","phosel_LeadingPhotonabsSCEta_NonPrompt_barrel", "phosel_dRLeadingPhotonLepton_GenuinePhoton_barrel", "phosel_dRLeadingPhotonLepton_MisIDEle_barrel", "phosel_dRLeadingPhotonLepton_NonPrompt_barrel", "phosel_dRLeadingPhotonLepton_barrel","phosel_dRLeadingPhotonJet_GenuinePhoton_barrel", "phosel_dRLeadingPhotonJet_MisIDEle_barrel", "phosel_dRLeadingPhotonJet_NonPrompt_barrel", "phosel_dRLeadingPhotonJet_barrel"]
        if not runQuiet: print "Making subset of kinematic plots"
    elif makeEGammaPlots:
        plotList = ["phosel_MassEGamma","phosel_MassEGammaMisIDEle","phosel_MassEGammaOthers","phosel_MassEGamma_barrel","phosel_MassEGamma_MisIDEle_barrel","phosel_MassEGammaOthers_barrel"]
        if not runQuiet: print "Making only plots for e-gamma fits"
    elif makedRPlots:
	 plotList=["phosel_dRLeadingPhotonLepton_GenuinePhoton_barrel", "phosel_dRLeadingPhotonLepton_MisIDEle_barrel", "phosel_dRLeadingPhotonLepton_NonPrompt_barrel", "phosel_dRLeadingPhotonLepton_barrel","phosel_dRLeadingPhotonJet_GenuinePhoton_barrel", "phosel_dRLeadingPhotonJet_MisIDEle_barrel", "phosel_dRLeadingPhotonJet_NonPrompt_barrel", "phosel_dRLeadingPhotonJet_barrel"]
    
	 if not runQuiet: print "Making only dR photon plots"
    elif makegenPlots:
	 plotList=["phosel_LeadingPhotonabsSCEta_barrel", "phosel_LeadingPhotonabsSCEta_GenuinePhoton_barrel","phosel_LeadingPhotonabsSCEta_MisIDEle_barrel","phosel_LeadingPhotonabsSCEta_NonPrompt_barrel","phosel_LeadingPhotonEt_barrel","phosel_LeadingPhotonEt_GenuinePhoton_barrel","phosel_LeadingPhotonEt_MisIDEle_barrel","phosel_LeadingPhotonEt_NonPrompt_barrel", "phosel_GenPhoPt","phosel_GenPhoEta"]
         if not runQuiet: print "Making only 2D photon plots"
    elif Dilepmass:
	plotList = ["presel_DilepMass"]
        if not runQuiet: print "Making only plots for ZJetsSF fits"
    elif not multiPlotList is None:
        plotList = []
        for plotNameTemplate in multiPlotList:
            thisPlotList = []
            for plotName in histogramInfo.keys():
                if plotNameTemplate in plotName:
                    thisPlotList.append(plotName)
            thisPlotList.sort()
            if not runQuiet: 
                print '---'
                print '  Found the following plots matching the name key %s'%plotNameTemplate
                print '    ',thisPlotList
            plotList += thisPlotList

        #take the set to avoid duplicates (if multiple plot name templates are used, and match the same plot)
        plotList = list(set(plotList))


    else:
        # plotList = ["presel_M3_control","phosel_noCut_ChIso","phosel_noCut_ChIso_GenuinePhoton","phosel_noCut_ChIso_MisIDEle","phosel_noCut_ChIso_HadronicPhoton","phosel_noCut_ChIso_HadronicFake","phosel_M3","phosel_M3_GenuinePhoton","phosel_M3_MisIDEle","phosel_M3_HadronicPhoton","phosel_M3_HadronicFake","phosel_AntiSIEIE_ChIso","phosel_AntiSIEIE_ChIso_barrel","phosel_AntiSIEIE_ChIso_endcap","phosel_PhotonCategory"]
        plotList = ["presel_M3_control","presel_M3","phosel_noCut_ChIso","phosel_noCut_ChIso_barrel","phosel_noCut_ChIso_endcap","phosel_noCut_ChIso_GenuinePhoton","phosel_noCut_ChIso_MisIDEle","phosel_noCut_ChIso_HadronicPhoton","phosel_noCut_ChIso_HadronicFake","phosel_noCut_ChIso_GenuinePhoton_barrel","phosel_noCut_ChIso_GenuinePhoton_endcap","phosel_noCut_ChIso_MisIDEle_barrel","phosel_noCut_ChIso_MisIDEle_endcap","phosel_noCut_ChIso_HadronicPhoton_barrel","phosel_noCut_ChIso_HadronicPhoton_endcap","phosel_noCut_ChIso_HadronicFake_barrel","phosel_noCut_ChIso_HadronicFake_endcap","phosel_M3","phosel_M3_GenuinePhoton","phosel_M3_MisIDEle","phosel_M3_HadronicPhoton","phosel_M3_HadronicFake","phosel_M3_barrel","phosel_M3_endcap","phosel_M3_GenuinePhoton_barrel","phosel_M3_GenuinePhoton_endcap","phosel_M3_MisIDEle_barrel","phosel_M3_MisIDEle_endcap","phosel_M3_HadronicPhoton_barrel","phosel_M3_HadronicPhoton_endcap","phosel_M3_HadronicFake_barrel","phosel_M3_HadronicFake_endcap","phosel_AntiSIEIE_ChIso","phosel_AntiSIEIE_ChIso_barrel","phosel_AntiSIEIE_ChIso_endcap","phosel_AntiSIEIE_ChIso_GenuinePhoton_barrel","phosel_AntiSIEIE_ChIso_GenuinePhoton_endcap","phosel_AntiSIEIE_ChIso_HadronicPhoton_barrel","phosel_AntiSIEIE_ChIso_HadronicPhoton_endcap","phosel_AntiSIEIE_ChIso_HadronicFake_barrel","phosel_AntiSIEIE_ChIso_HadronicFake_endcap","phosel_AntiSIEIE_ChIso_MisIDEle_barrel","phosel_AntiSIEIE_ChIso_MisIDEle_endcap","phosel_MassEGamma","phosel_MassEGammaMisIDEle","phosel_MassEGammaOthers","phosel_MassEGamma_barrel","phosel_MassEGamma_MisIDEle_barrel","phosel_MassEGammaOthers_barrel","phosel_MassEGamma_endcap","phosel_MassEGammaMisIDEle_endcap","phosel_MassEGammaOthers_endcap"]
	'''
        if isLooseCR2g1Selection or isLooseCR2e1Selection:
		plotList.append("presel_WtransMass")
		plotList.append("phosel_WtransMass_barrel")
		plotList.append("phosel_WtransMass_GenuinePhoton_barrel")
		plotList.append("phosel_WtransMass_HadronicPhoton_barrel")
		plotList.append("phosel_WtransMass_MisIDEle_barrel")
		plotList.append("phosel_WtransMass_HadronicFake_barrel")
	elif isTightSelection0b:
		plotList=["phosel_Njet", "phosel_Njet_barrel","phosel_Njet_GenuinePhoton_barrel", "phosel_Njet_MisIDEle_barrel","phosel_Njet_HadronicPhoton_barrel","phosel_Njet_HadronicFake_barrel"]
	'''
	if not runQuiet: print "Making only plots for simultaneous fits"

plotList.sort()
if not runQuiet: toPrint( "Making the following histogram(s)", "")
if not runQuiet: 
    for p in plotList: print "%s,"%p,
histogramsToMake = plotList
allHistsDefined = True
for hist in histogramsToMake:
    if not hist in histogramInfo:
        print "Histogram %s is not defined in HistListDict_cff.py"%hist
        allHistsDefined = False
if not allHistsDefined:
    sys.exit()

#-----------------------------------
'''
The QCD transfer scale factors (TF)
are determined from MC QCD background.
The TF is ratio of event yields from
high isolation and a different number
of b jet control regions.
'''
#-----------------------------------
def getQCDTransFact(channel, outputFile):
    if channel in ["Mu","mu"]:
    	sample = "QCDMu"
    	preselCut = "passPresel_Mu"
    	qcdRelIsoCut = "muPFRelIso>0.15 && muPFRelIso<0.3 && "
    elif channel in ["Ele","ele","e"]:
    	sample = "QCDEle"
    	preselCut = "passPresel_Ele"
    	qcdRelIsoCut = "elePFRelIso>0.01 &&"
    
    #-----------------------------------------
    #QCD histogram from: 
    #high rel iso, nJets ==2, nBJets = 0
    #----------------------------------------
    tree = TChain("AnalysisTree")
    fileList = samples[sample][0]
    for fileName in fileList:
    	tree.Add("%s/QCDcr_%s"%(ntupleDirBaseCR,fileName))
    nJets  = 2
    nBJets = 0
    extraCuts       = "(%s && %s nJet>=%i && nBJet==%i)*"%(preselCut, qcdRelIsoCut, nJets, nBJets)
    extraCutsPhoton = "(%s && %s nJet>=%i && nBJet==%i && phoMediumID)*"%(preselCut, qcdRelIsoCut, nJets, nBJets)
    weights = "evtWeight*PUweight*muEffWeight*eleEffWeight*btagWeight[%i]"%nBJets
    histCR    = TH1F("Njet_HighIso_0b","Njet_HighIso_0b",15,0,15)
    histCRPho = TH1F("Njet_HighIso_0b_1Photon","Njet_HighIso_0b_1Photon",15,0,15)
    tree.Draw("nJet>>Njet_HighIso_0b",extraCuts+weights)
    tree.Draw("nJet>>Njet_HighIso_0b_1Photon",extraCutsPhoton+weights)
    outputFile.cd()
    histCR.Write()
    
    #-----------------------------------------
    #QCD histogram from: 
    #low rel iso, nJets ==2, nBJets = 0
    #----------------------------------------
    tree = TChain("AnalysisTree")
    fileList = samples[sample][0]
    for fileName in fileList:
    	tree.Add("%s/%s"%(ntupleDirBase,fileName))
    fileList = samples["GJets"][0]
    for fileName in fileList:
    	tree.Add("%s/%s"%(ntupleDirBase,fileName))
    nJets  = 2
    nBJets = 0
    extraCuts       = "(%s && nJet>=%i && nBJet==%i)*"%(preselCut, nJets, nBJets)
    extraCutsPhoton = "(%s && nJet>=%i && nBJet==%i && phoMediumID)*"%(preselCut, nJets, nBJets)
    weights = "evtWeight*PUweight*muEffWeight*eleEffWeight*btagWeight[%i]"%nBJets
    hist0 = TH1F("Njet_LowIso_0b","Njet_LowIso_0b",15,0,15)
    hist0Pho = TH1F("Njet_LowIso_0b_1Photon","Njet_LowIso_0b_1Photon",15,0,15)
    tree.Draw("nJet>>Njet_LowIso_0b",extraCuts+weights)
    tree.Draw("nJet>>Njet_LowIso_0b_1Photon",extraCutsPhoton+weights)
    outputFile.cd()
    hist0.Write()
    
    #-----------------------------------------
    #QCD histogram from: 
    #low rel iso, nJets ==2, nBJets = 1
    #----------------------------------------
    nJets  = 2
    nBJets = 1
    extraCuts       = "(%s && nJet>=%i && nBJet==%i)*"%(preselCut, nJets, nBJets)
    extraCutsPhoton = "(%s && nJet>=%i && nBJet==%i && phoMediumID)*"%(preselCut, nJets, nBJets)
    weights = "evtWeight*PUweight*muEffWeight*eleEffWeight*btagWeight[%i]"%nBJets
    hist1 = TH1F("Njet_LowIso_1b","Njet_LowIso_1b",15,0,15)
    hist1Pho = TH1F("Njet_LowIso_1b_1Photon","Njet_LowIso_1b_1Photon",15,0,15)
    tree.Draw("nJet>>Njet_LowIso_1b",extraCuts+weights)
    tree.Draw("nJet>>Njet_LowIso_1b_1Photon",extraCutsPhoton+weights)
    outputFile.cd()
    hist1.Write()
    
    #-----------------------------------------
    #QCD histogram from: 
    #low rel iso, nJets ==2, nBJets = 2
    #----------------------------------------
    nJets  = 2
    nBJets = 2
    extraCuts       = "(%s && nJet>=%i && nBJet>=%i)*"%(preselCut, nJets, nBJets)
    extraCutsPhoton = "(%s && nJet>=%i && nBJet>=%i && phoMediumID)*"%(preselCut, nJets, nBJets)
    weights = "evtWeight*PUweight*muEffWeight*eleEffWeight*btagWeight[%i]"%nBJets
    hist2 = TH1F("Njet_LowIso_2b","Njet_LowIso_2b",15,0,15)
    hist2Pho = TH1F("Njet_LowIso_2b_1Photon","Njet_LowIso_2b_1Photon",15,0,15)
    tree.Draw("nJet>>Njet_LowIso_2b",extraCuts+weights)
    tree.Draw("nJet>>Njet_LowIso_2b_1Photon",extraCutsPhoton+weights)
    outputFile.cd()
    hist2.Write()
    histCRPho.Write()
    hist0Pho.Write()
    hist1Pho.Write()
    hist2Pho.Write()
    
    #-----------------------------------------
    # Determine the TF (nb/CR) in each bin
    #----------------------------------------
    hist0_TF = hist0.Clone("TF_BinByBin_0b")
    hist0_TF.SetNameTitle("TF_BinByBin_0b","TF_BinByBin_0b")
    hist0_TF.Divide(histCR)
    hist1_TF = hist1.Clone("TF_BinByBin_1b")
    hist1_TF.SetNameTitle("TF_BinByBin_1b","TF_BinByBin_1b")
    hist1_TF.Divide(histCR)
    hist2_TF = hist2.Clone("TF_BinByBin_2b")
    hist2_TF.SetNameTitle("TF_BinByBin_2b","TF_BinByBin_2b")
    hist2_TF.Divide(histCR)
    hist0_TF.Write()
    hist1_TF.Write()
    hist2_TF.Write()
    
    hist0Pho_TF = hist0Pho.Clone("TF_BinByBin_0b_1Photon")
    hist0Pho_TF.SetNameTitle("TF_BinByBin_0b_1Photon","TF_BinByBin_0b_1Photon")
    hist0Pho_TF.Divide(histCR)
    hist1Pho_TF = hist1Pho.Clone("TF_BinByBin_1b_1Photon")
    hist1Pho_TF.SetNameTitle("TF_BinByBin_1b_1Photon","TF_BinByBin_1b_1Photon")
    hist1Pho_TF.Divide(histCR)
    hist2Pho_TF = hist2Pho.Clone("TF_BinByBin_2b_1Photon")
    hist2Pho_TF.SetNameTitle("TF_BinByBin_2b_1Photon","TF_BinByBin_2b_1Photon")
    hist2Pho_TF.Divide(histCR)
    hist0Pho_TF.Write()
    hist1Pho_TF.Write()
    hist2Pho_TF.Write()
    
    #-----------------------------------------
    # Determine the TF (nb/CR) in total yield
    #----------------------------------------
    hist_TF = TH1F("TF_TotalYield_012b","TF_TotalYield_012b",3,0,3)
    hist_TFCR = TH1F("TF_TotalYield_012bCR","TF_TotalYield_012bCR",3,0,3)
    histCR.Rebin(15)
    hist0.Rebin(15)
    hist1.Rebin(15)
    hist2.Rebin(15)
    hist_TF.SetBinContent(1,hist0.GetBinContent(1))
    hist_TF.SetBinError(1,hist0.GetBinError(1))
    hist_TF.SetBinContent(2,hist1.GetBinContent(1))
    hist_TF.SetBinError(2,hist1.GetBinError(1))
    hist_TF.SetBinContent(3,hist2.GetBinContent(1))
    hist_TF.SetBinError(3,hist2.GetBinError(1))
    hist_TFCR.SetBinContent(1,histCR.GetBinContent(1))
    hist_TFCR.SetBinError(1,histCR.GetBinError(1))
    hist_TFCR.SetBinContent(2,histCR.GetBinContent(1))
    hist_TFCR.SetBinError(2,histCR.GetBinError(1))
    hist_TFCR.SetBinContent(3,histCR.GetBinContent(1))
    hist_TFCR.SetBinError(3,histCR.GetBinError(1))
    hist_TF.Divide(hist_TFCR)
    hist_TF.Write()
    
    hist_TFPho = TH1F("TF_TotalYield_012b_1Photon","TF_TotalYield_012b_1Photon",3,0,3)
    hist_TFCRPho = TH1F("TF_TotalYield_012bCRPho","TF_TotalYield_012bCRPho",3,0,3)
    histCRPho.Rebin(15)
    hist0Pho.Rebin(15)
    hist1Pho.Rebin(15)
    hist2Pho.Rebin(15)
    hist_TFPho.SetBinContent(1,hist0Pho.GetBinContent(1))
    hist_TFPho.SetBinError(1,hist0Pho.GetBinError(1))
    hist_TFPho.SetBinContent(2,hist1Pho.GetBinContent(1))
    hist_TFPho.SetBinError(2,hist1Pho.GetBinError(1))
    hist_TFPho.SetBinContent(3,hist2Pho.GetBinContent(1))
    hist_TFPho.SetBinError(3,hist2Pho.GetBinError(1))
    hist_TFCRPho.SetBinContent(1,histCRPho.GetBinContent(1))
    hist_TFCRPho.SetBinError(1,histCRPho.GetBinError(1))
    hist_TFCRPho.SetBinContent(2,histCRPho.GetBinContent(1))
    hist_TFCRPho.SetBinError(2,histCRPho.GetBinError(1))
    hist_TFCRPho.SetBinContent(3,histCRPho.GetBinContent(1))
    hist_TFCRPho.SetBinError(3,histCRPho.GetBinError(1))
    hist_TFPho.Divide(hist_TFCRPho)
    hist_TFPho.Write()
    if nBJets==0:
    	hist2.Add(hist1)
    hist2.Add(hist0)
    transFact =  hist_TF.GetBinContent(1)
    if nBJets==1:
        hist2.Add(hist1)
        transFact = hist2.Integral(nJets+1,-1)/histCR.Integral(-1,-1)
    if nBJets==1:
    	transFact = hist2.Integral(nJets+1,-1)/histCR.Integral(-1,-1)
    if isLooseCR2e1Selection:
   		transFact = hist_TF.GetBinContent(2) 
    return transFact

#-----------------------------------------
# Determine data - nonQCDBkg from CR
#----------------------------------------
def getShapeFromCR(channel, hInfo):
    nBJets = -1
    btagWeightCategory = ["1","(1-btagWeight[0])","(btagWeight[2])","(btagWeight[1])","(btagWeight[0])"]
    if channel=="Mu":
    	sampleList[-1] = "DataMu"
    	sampleList[-2] = "QCDMu"
    	extraCuts            = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=3)*"
    	extraPhotonCuts      = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=3 && %s)*"
    	if isTightSelection:
    		extraCuts            = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=4)*"
    		extraPhotonCuts      = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=4 && %s)*"
    	#if isLooseSelection or isLooseCRSelection:
    		extraCuts            = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=2)*"
    		extraPhotonCuts      = "(passPresel_Mu && muPFRelIso<0.3 && nJet>=2 && %s)*"
    
    if channel=="Ele":
    	sampleList[-1] = "DataEle"
    	sampleList[-2] = "QCDEle"
    	extraCuts            = "(passPresel_Ele && muPFRelIso<0.3 && nJet>=3)*"
    	extraPhotonCuts      = "(passPresel_Ele && muPFRelIso<0.3 && nJet>=3 && %s)*"
    	if isTightSelection:
    		extraCuts            = "(passPresel_Ele && muPFRelIso<0.3 && nJet>=4)*"
    		extraPhotonCuts      = "(passPresel_Ele && muPFRelIso<0.3 && nJet>=4 && %s)*"
    	#if isLooseSelection or isLooseCRSelection:
    		extraCuts            = "(passPresel_Ele && muPFRelIso<0.3 && nJet>=2)*"
    		extraPhotonCuts      = "(passPresel_Ele && muPFRelIso<0.3 && nJet>=2 && %s)*"
    
    weights = "evtWeight*PUweight*muEffWeight*eleEffWeight*%s"%btagWeightCategory[nBJets]
    #if not hInfo[5]: continue
    print "filling", hInfo[1], sample
    evtWeight = ""
    if hInfo[4]=="":
        evtWeight = "%s%s"%(hInfo[3],weights)
    else:
        evtWeight = hInfo[4]
    hNonQCDBkgs = []
    hData = []
    for sample_ in sampleList:
        hist_ = TH1F("%s_%s"%(hInfo[1], sample_),"%s_%s"%(hInfo[1],sample_),hInfo[2][0],hInfo[2][1],hInfo[2][2])
	if sample_ not in ["QCDMu", "QCDEle","DataMu","DataEle", "TTGJets"]:
            tree = TChain("AnalysisTree")
            fileList = samples[sample_][0]
            for fileName in fileList:
    	        tree.Add("%s/QCDcr_%s"%(ntupleDirBaseCR,fileName))
            tree.Draw("%s>>%s_%s"%(hInfo[0],hInfo[1],sample_),evtWeight)
            hNonQCDBkgs.append(hist_)
        if "Data" in sample_:
            tree = TChain("AnalysisTree")
            fileList = samples[sampleList[-1]][0]
            evtWeight = hInfo[3]
            if evtWeight[-1]=="*":
                evtWeight= evtWeight[:-1]
            for fileName in fileList:
    	    	tree.Add("%s/QCDcr_%s"%(ntupleDirBaseCR,fileName))
            tree.Draw("%s>>%s_%s"%(hInfo[0],hInfo[1],sample_),evtWeight)
            hData.append(hist_)
        print "For data driven QCD: Sample = %s, Integral = %s"%(sample_, hist_.Integral())
    hDiffDataBkg = hData[0].Clone(hInfo[1])
    for hNonQCDBkg in hNonQCDBkgs:
        hDiffDataBkg.Add(hNonQCDBkg, -1)
    return hDiffDataBkg

#-----------------------------------------
# QCD in SR = TF * (data - nonQCDBkg from CR)
#----------------------------------------
transferFactor = 1.0
histograms=[]
canvas = TCanvas()
if sample =="QCD_DD":
	transferFactor = getQCDTransFact(channel, outputFile)
	print "Transfer factor = ", transferFactor
        for hist in histogramsToMake:
            if not histogramInfo[hist][5]: continue
	    dataMinusOtherBkg = getShapeFromCR(channel, histogramInfo[hist])
            histograms.append(dataMinusOtherBkg)
	    print histogramInfo[hist][1]
            histograms[-1].Scale(transferFactor)

#-----------------------------------------
# Use MC QCD in the SR, instead 
#----------------------------------------
if not "QCD_DD" in sample:
    if not sample in samples:
        print "Sample isn't in list"
        print samples.keys()
        sys.exit()

    tree = TChain("AnalysisTree")
    fileList = samples[sample][0]
    for fileName in fileList:
 	if year=="2017":
		fileName = fileName.replace("2016", "2017")
 	if year=="2018":
		fileName = fileName.replace("2016", "2018")
        tree.Add("%s%s"%(analysisNtupleLocation,fileName))
 	print "%s%s"%(analysisNtupleLocation,fileName)
    #print sample

    #print "Number of events:", tree.GetEntries()
    
    for hist in histogramsToMake:
        hInfo = histogramInfo[hist]
#	print hist
        # skip some histograms which rely on MC truth and can't be done in data or QCD data driven templates
        if ('Data' in sample or isQCD) and not hInfo[5]: continue

        if not runQuiet: toPrint("Filling the histogram", hInfo[1])
        evtWeight = ""
#	print TH1F("%s_%s"%(hInfo[1],sample),"%s_%s"%(hInfo[1],sample),hInfo[2][0],hInfo[2][1],hInfo[2][2])
        histograms.append(TH1F("%s"%(hInfo[1]),"%s"%(hInfo[1]),hInfo[2][0],hInfo[2][1],hInfo[2][2]))
        if hInfo[4]=="":
            evtWeight = "%s%s"%(hInfo[3],weights)
        else:
            evtWeight = hInfo[4]

        if "Data" in sample:
            evtWeight = "%s%s"%(hInfo[3],weights)

        if evtWeight[-1]=="*":
            evtWeight= evtWeight[:-1]


        ### Correctly add the photon weights to the plots
        if 'phosel' in hInfo[1]:
	    	    
            if hInfo[0][:8]=="loosePho":
                evtWeight = "%s*%s"%(evtWeight,loosePhoEff)
            elif hInfo[0][:3]=="pho":
#		print hInfo[0][:3], "%s*%s"%(evtWeight,PhoEff)
                evtWeight = "%s*%s"%(evtWeight,PhoEff)
            else:
#		print hInfo[0], "%s*%s[0]"%(evtWeight,PhoEff)
                evtWeight = "%s*%s[0]"%(evtWeight,PhoEff)
	#print "%s>>%s_%s"%(hInfo[0],hInfo[1],sample),evtWeight
     #   print "evtweight is:", evtWeight	
        tree.Draw("%s>>%s"%(hInfo[0],hInfo[1]),evtWeight)

histDirInFile = histDirInFile+"/"+signalOrCR
if not runQuiet: toPrint ("The histogram directory inside the root file is", histDirInFile) 
if not outputFile.GetDirectory(histDirInFile):
    outputFile.mkdir(histDirInFile)
outputFile.cd(histDirInFile)

for h in histograms:
    toPrint("Integral of Histogram %s = "%h.GetName(), h.Integral())
    outputFile.cd(histDirInFile)
    gDirectory.Delete("%s;*"%(h.GetName()))
    h.Write()
toPrint("Path of output root file", fullPath)
outputFile.Close()
