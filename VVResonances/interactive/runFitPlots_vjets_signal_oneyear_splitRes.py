#python runFitPlots_vjets_signal_oneyear_splitRes.py -n workspace_JJ_ZprimeZH_HPLP_13TeV_2016.root  -l sigonly -i 2016/JJ_nonRes_HPLP.root -M 2000 -s
import ROOT
ROOT.gROOT.SetBatch(True)
import os, sys, re, optparse,pickle,shutil,json
import time
from array import array
import math
import CMS_lumi
from tools import PostFitTools
ROOT.gErrorIgnoreLevel = ROOT.kWarning
ROOT.gROOT.ProcessLine(".x tdrstyle.cc");

#ROOT.gSystem.Load("Util_cxx.so")
#from ROOT import draw_error_band

#python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_combo_"+signalName+".root  -l comboHPHP -i /afs/cern.ch/user/j/jngadiub/public/2016/JJ_nonRes_HPHP.root -M 1200 -s
#python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_combo_"+signalName+".root  -l comboHPLP -i /afs/cern.ch/user/j/jngadiub/public/2016/JJ_nonRes_HPLP.root -M 1200

addTT = False 
doFit = True
parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",help="Output folder name",default='')
parser.add_option("-n","--name",dest="name",help="Input workspace",default='workspace.root')
parser.add_option("-i","--input",dest="input",help="Input nonRes histo",default='JJ_HPHP.root')
parser.add_option("-x","--xrange",dest="xrange",help="set range for x bins in projection",default="0,-1")
parser.add_option("-y","--yrange",dest="yrange",help="set range for y bins in projection",default="0,-1")
parser.add_option("-z","--zrange",dest="zrange",help="set range for z bins in projection",default="0,-1")
parser.add_option("-p","--projection",dest="projection",help="choose which projection should be done",default="xyz")
parser.add_option("-d","--data",dest="data",action="store_true",help="make also postfit plots",default=True)
parser.add_option("-l","--label",dest="label",help="add extra label such as pythia or herwig",default="")
#parser.add_option("--log",dest="log",help="write fit result to log file",default="fit_results.log")
parser.add_option("--pdfz",dest="pdfz",help="name of pdfs lie PTZUp etc",default="")
parser.add_option("--pdfx",dest="pdfx",help="name of pdfs lie PTXUp etc",default="")
parser.add_option("--pdfy",dest="pdfy",help="name of pdfs lie PTYUp etc",default="")
parser.add_option("-s","--signal",dest="fitSignal",action="store_true",help="do S+B fit",default=False)
parser.add_option("--doFit",dest="fit",action="store_false",help="actually fit the the distributions",default=True)
parser.add_option("-t","--addTop",dest="addTop",action="store_true",help="Fit top",default=False)
parser.add_option("-v","--doVjets",dest="doVjets",action="store_true",help="Fit top",default=False)
parser.add_option("-M","--mass",dest="signalMass",type=float,help="signal mass",default=1560.)
parser.add_option("--signalScaleF",dest="signalScaleF",type=float,help="scale factor to apply to signal when drawing so its still visible!",default=100.)
parser.add_option("--prelim",dest="prelim",type=int,help="add preliminary label",default=0)
parser.add_option("--log",dest="log",help="write output in logfile given as argument here!",default="chi2.log")
parser.add_option("--channel",dest="channel",help="which category to use? ",default="VV_HPHP")

(options,args) = parser.parse_args()
ROOT.gStyle.SetOptStat(0)
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.FATAL)



signalName = "ZprimeZH"
if options.name.find("WZ")!=-1:
    signalName="WprimeWZ"
if options.name.find("WH")!=-1:
    signalName="WprimeWH"
if options.name.find("ZprimeWW")!=-1:
    signalName="ZprimeWW"
if options.name.find("BulkGWW")!=-1:
    signalName="BulkGWW"
if options.name.find("BulkGZZ")!=-1:
    signalName="BulkGZZ"
period = "2016"
if options.name.find("2017")!=-1: period = "2017"

                 

   


if __name__=="__main__":
     finMC = ROOT.TFile(options.input,"READ");
     hinMC = finMC.Get("nonRes");
     print options.name
     purity = options.channel
     print " run on category ", purity
    
     print " get workspace "               
    
     print 
     print "open file " +options.name
     f = ROOT.TFile(options.name,"READ")
     workspace = f.Get("w")
     f.Close()
     #workspace.Print()

     model = workspace.pdf("model_b") 
     model_b = workspace.pdf("model_b")
     if options.fitSignal: model = workspace.pdf("model_s")
     data_all = workspace.data("data_obs")
     data1 = workspace.data("data_obs").reduce("CMS_channel==CMS_channel::JJ_"+purity+"_13TeV_"+period)
     
     print
     print "Observed number of events in",purity,"category:",data1.sumEntries(),"("+period+")"
     
     args  = model.getComponents()
     pdf1Name = "pdf_binJJ_"+purity+"_13TeV_"+period+"_bonly"
     if options.fitSignal:
      pdf1Name = "pdf_binJJ_"+purity+"_13TeV_"+period
     print "pdf1Name ",pdf1Name

     expected = {}
     for bkg in ["nonRes","Wjets","Zjets","TTJetsTop","TTJetsW","TTJetsNonRes"]:
        if options.doVjets==False and (bkg=="Wjets" or bkg=="Zjets"): expected[bkg] = [0.,0.]; continue
        if options.addTop==False and (bkg.find("TTJets")!=-1): expected[bkg] = [0.,0.]; continue
        print bkg
        expected[bkg] = [ (args[pdf1Name].getComponents())["n_exp_binJJ_"+purity+"_13TeV_"+period+"_proc_"+bkg].getVal(),0.]
        print "Expected number of "+bkg+" events:",(expected[bkg][0]),"("+period+")"
     norm_sig = 1.
     if options.fitSignal:
      workspace.var("MH").setVal(options.signalMass)
      workspace.var("MH").setConstant(1)
      workspace.var("r").setRange(0,2000)
      norm_sig = (args[pdf1Name].getComponents())["n_exp_final_binJJ_"+purity+"_13TeV_"+period+"_proc_"+signalName+""].getVal()
      print "signalName ",signalName
      print "Expected signal yields:",norm_sig,"("+period+")"
     print 
     if options.addTop:
         expected["TTJets"] = [0.,0.]
         for i in ["TTJetsTop","TTJetsW","TTJetsNonRes"]:
            expected["TTJets"][0] += expected[i][0]
            expected["TTJets"][1] += expected[i][1]
         

     #################################################
     if options.fit:
        fitresult = model.fitTo(data_all,ROOT.RooFit.SumW2Error(not(options.data)),ROOT.RooFit.Minos(0),ROOT.RooFit.Verbose(0),ROOT.RooFit.Save(1),ROOT.RooFit.NumCPU(8))  
        if options.label.find("sigonly")==-1:
            fitresult_bkg_only = model_b.fitTo(data_all,ROOT.RooFit.SumW2Error(not(options.data)),ROOT.RooFit.Minos(0),ROOT.RooFit.Verbose(0),ROOT.RooFit.Save(1),ROOT.RooFit.NumCPU(8))
        else: fitresult_bkg_only = fitresult
             
     print 
     print period+" Prefit nonRes pdf:"
     pdf1_nonres_shape_prefit = args["nonResNominal_JJ_"+purity+"_13TeV_"+period]
     pdf1_nonres_shape_prefit.Print()
     print
 
     print period+" Postfit nonRes pdf:"
     pdf1_nonres_shape_postfit  = args["shapeBkg_nonRes_JJ_"+purity+"_13TeV_"+period]
     pdf1_nonres_shape_postfit.Print()
     pdf1_nonres_shape_postfit.funcList().Print()
     pdf1_nonres_shape_postfit.coefList().Print()
     print
    
     if options.doVjets:
        print period+" Postfit W+jets res pdf:"
        pdf1_Wres_shape_postfit  = args["shapeBkg_Wjets_JJ_"+purity+"_13TeV_"+period]
        pdf1_Wres_shape_postfit.Print()

        print period+" Postfit Z+jets res pdf:"
        pdf1_Zres_shape_postfit  = args["shapeBkg_Zjets_JJ_"+purity+"_13TeV_"+period]
        pdf1_Zres_shape_postfit.Print()
        
     
     if options.addTop:
        print period+" Postfit tt res pdf:"
        pdf1_TTJets_shape_postfit  = []
        pdf1_TTJets_shape_postfit.append(args["shapeBkg_TTJetsTop_JJ_"+purity+"_13TeV_"+period])
        pdf1_TTJets_shape_postfit.append(args["shapeBkg_TTJetsNonRes_JJ_"+purity+"_13TeV_"+period])
        pdf1_TTJets_shape_postfit.append(args["shapeBkg_TTJetsW_JJ_"+purity+"_13TeV_"+period])
        pdf1_TTJets_shape_postfit[0].Print()
 
     pdf1_signal_postfit = None
     if options.fitSignal:
      print period+" Signal pdf:"     
      pdf1_signal_postfit  = args["shapeSig_"+signalName+"_JJ_"+purity+"_13TeV_"+period]
      pdf1_signal_postfit.Print()
      print
  
     print "Full 2016 post-fit pdf:"     
     pdf1_shape_postfit  = args[pdf1Name+"_nuis"]
     pdf1_shape_postfit.Print()
     print
    
		    
     allpdfs = [] 
     allpdfs.append(pdf1_nonres_shape_postfit)
     if options.doVjets:
        allpdfs.append(pdf1_Wres_shape_postfit)
        allpdfs.append(pdf1_Zres_shape_postfit)
        if options.addTop:
            print "add top"
            for pdf_tt in pdf1_TTJets_shape_postfit:
                allpdfs.append(pdf_tt)
     allpdfs.append(pdf1_shape_postfit)
     
     #let's have always pre-fit and post-fit as firt elements here, and add the optional shapes if you want with options.pdf
     allpdfsz = allpdfs
     for p in options.pdfz.split(","):
         if p == '': continue
         print "add pdf:",p
         args[p].Print()
         allpdfsz.append(args[p])
     allpdfsx = allpdfs
     for p in options.pdfx.split(","):
         if p == '': continue
	 print "add pdf:",p
	 args[p].Print()
         allpdfsx.append(args[p])
     allpdfsy = allpdfs
     allpdfsy.append(pdf1_shape_postfit)
     for p in options.pdfy.split(","):
         if p == '': continue
         print "add pdf:",p
         args[p].Print()
         allpdfsy.append(args[p])
      
     norm1_sig= [0.,0.] 
     norm1_sig[0] = norm_sig
     if options.fitSignal:
         norm1_sig[0] = (args[pdf1Name].getComponents())["n_exp_final_binJJ_"+purity+"_13TeV_"+period+"_proc_"+signalName+""].getVal() 
         if options.fit:
            norm1_sig[1] = (args[pdf1Name].getComponents())["n_exp_final_binJJ_"+purity+"_13TeV_"+period+"_proc_"+signalName+""].getPropagatedError(fitresult)
         print "get norm sig "+str(norm1_sig[0])
     
     
     if options.fit:
        for bkg in ["nonRes","Wjets","Zjets","TTJetsTop","TTJetsW","TTJetsNonRes"]:
            if options.doVjets==False and (bkg=="Wjets" or bkg=="Zjets"): expected[bkg] = [0.,0.]; continue
            if options.addTop==False and (bkg.find("TTJets")!=-1): expected[bkg] = [0.,0.]; continue 
            expected[bkg][1] = (args[pdf1Name].getComponents())["n_exp_binJJ_"+purity+"_13TeV_"+period+"_proc_"+bkg].getPropagatedError(fitresult)
            expected[bkg][0] = (args[pdf1Name].getComponents())["n_exp_binJJ_"+purity+"_13TeV_"+period+"_proc_"+bkg].getVal()
            print bkg
            print "Expected number of "+bkg+" events:",(expected[bkg][0]),"("+period+")"
            print (args[pdf1Name].getComponents())["n_exp_binJJ_"+purity+"_13TeV_"+period+"_proc_"+bkg].dump() 
    
        print "QCD normalization after fit: ",expected["nonRes"][0],"+/-",expected["nonRes"][1],"("+period+")"
        if options.doVjets:
            print "W+jets normalization after fit: ",expected["Wjets"][0],"+/-",expected["Wjets"][1],"("+period+")"
            print "Z+jets normalization after fit: ",expected["Zjets"][0],"+/-",expected["Zjets"][1],"("+period+")"
        if options.addTop:
            expected["TTJets"] = [0.,0.]
            for i in ["TTJetsTop","TTJetsW","TTJetsNonRes"]:
                print "tt normalization after fit: ",expected[i][0],"+/-",expected[i][1],"("+period+")"
                expected["TTJets"][0] += expected[i][0]
                expected["TTJets"][1] += expected[i][1]
        if options.fitSignal: print "Signal yields after fit: ",norm1_sig[0],"+/-",norm1_sig[1],"("+period+")"
            
      
     logfile = open(options.log,"a")
     forplotting = PostFitTools.Postfitplotter(options,logfile,signalName)
     forproj = PostFitTools.Projection(hinMC,[options.xrange,options.yrange,options.zrange], workspace,options.fit)
     #make projections onto MJJ axis 
     if options.projection =="z":
         results = forproj.doProjection(data1,allpdfsz,expected,"z",pdf1_signal_postfit,norm1_sig) 
         forplotting.MakePlots(results[0],results[1],results[2],results[3],results[4],results[5], results[6],results[7])
     #make projections onto MJ1 axis
     if options.projection =="x":
         results = forproj.doProjection(data1,allpdfsx,expected,"x",pdf1_signal_postfit,norm1_sig)
         forplotting.MakePlots(results[0],results[1],results[2],results[3],results[4],results[5], results[6],results[7])
     #make projections onto MJ2 axis
     if options.projection =="y":
         results = forproj.doProjection(data1,allpdfsy,expected,"y",pdf1_signal_postfit,norm1_sig)
         forplotting.MakePlots(results[0],results[1],results[2],results[3],results[4],results[5], results[6],results[7])
     if options.projection =="xyz":
         resultsz =forproj.doProjection(data1,allpdfsz,expected,"z",pdf1_signal_postfit,norm1_sig)
         resultsx =forproj.doProjection(data1,allpdfsx,expected,"x",pdf1_signal_postfit,norm1_sig)
         resultsy =forproj.doProjection(data1,allpdfsy,expected,"y",pdf1_signal_postfit,norm1_sig)
         print resultsz 
         print resultsz
         forplotting.MakePlots(resultsz[0],resultsz[1],resultsz[2],resultsz[3],resultsz[4],resultsz[5], resultsz[6],resultsz[7])
         forplotting.MakePlots(resultsx[0],resultsx[1],resultsx[2],resultsx[3],resultsx[4],resultsx[5], resultsx[6],resultsx[7])
         forplotting.MakePlots(resultsy[0],resultsy[1],resultsy[2],resultsy[3],resultsy[4],resultsy[5], resultsy[6],resultsy[7])
     logfile.close()
     print "signal " ,pdf1_signal_postfit, norm1_sig
     

     
