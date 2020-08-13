import ROOT
ROOT.gROOT.SetBatch(True)
import os, sys, re, optparse,pickle,shutil,json
import time
from array import array
import math
import CMS_lumi
import numpy as np
from tools import Postfitplotter
ROOT.gErrorIgnoreLevel = ROOT.kWarning
ROOT.gROOT.ProcessLine(".x tdrstyle.cc");

#ROOT.gSystem.Load("Util_cxx.so")
#from ROOT import draw_error_band

#python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_combo_BulkGWW.root  -l comboHPHP -i /afs/cern.ch/user/j/jngadiub/public/2016/JJ_nonRes_HPHP.root -M 1200 -s
#python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_combo_BulkGWW.root  -l comboHPLP -i /afs/cern.ch/user/j/jngadiub/public/2016/JJ_nonRes_HPLP.root -M 1200

addTT = False 
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
parser.add_option("--log",dest="log",help="write fit result to log file",default="fit_results.log")
parser.add_option("--pdfz",dest="pdfz",help="name of pdfs lie PTZUp etc",default="")
parser.add_option("--pdfx",dest="pdfx",help="name of pdfs lie PTXUp etc",default="")
parser.add_option("--pdfy",dest="pdfy",help="name of pdfs lie PTYUp etc",default="")
parser.add_option("-s","--signal",dest="fitSignal",action="store_true",help="do S+B fit",default=False)
parser.add_option("-t","--addTop",dest="addTop",action="store_true",help="Fit top",default=False)
parser.add_option("-M","--mass",dest="signalMass",type=float,help="signal mass",default=1560.)
parser.add_option("--signalScaleF",dest="signalScaleF",type=float,help="scale factor to apply to signal when drawing so its still visible!",default=100.)
parser.add_option("--prelim",dest="prelim",help="add extra text CMS label",default="Preliminary")
parser.add_option("--channel",dest="channel",help="which category to use? ",default="VV_HPHP")
parser.add_option("--doFit",dest="fit",action="store_true",help="actually fit the the distributions",default=False)
parser.add_option("-v","--doVjets",dest="doVjets",action="store_true",help="Fit top",default=False)

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


def addGraph(graphs):
    if graphs[0]==None: return None
    gnew = ROOT.TGraphAsymmErrors()
    h = graphs[0].GetHistogram()
    for p in range(0,h.GetNbinsX()):
        x = 0.
        y = 0.
        ex = 0.
        ey = 0.
        for g in graphs:
            x = h.GetBinCenter(p)
            y += g.Eval(x)
            ex = g.GetErrorX(p)
            ey += pow(g.GetErrorY(p),2)
        gnew.SetPoint(p,x,y)
        gnew.SetPointError(p,ex,np.sqrt(ey))

def addResults(results): #self.hfinals,self.dh, self.htot_sig,self.axis,self.Binslowedge,self.maxYaxis, norm_sig[0],errors
    histos = results[0][0]
    dh = results[0][1]
    hsig = results[0][2]
    maxY = results[0][5]
    normsig = results[0][6]
    errs = []
    for i in range(0,len(results)):
        errs.append(results[i][7])
    errors = addGraph(errs)
    for j in range(1,len(results)):
        dh.Add(results[j][1])
        hsig.Add(results[j][2])
        maxY += results[j][5]
        maxY += normsig[j][6]
        for i in range(0,len(histos)):
            histos[i].Add(results[j][i])
    return [histos,dh,hsig,results[0][3],results[0][4],maxY,normsig,errors]


def writeLogfile(options,fitresult):
    if options.log!="":
     	 params = fitresult.floatParsFinal()
     	 paramsinit = fitresult.floatParsInit()
     	 paramsfinal = ROOT.RooArgSet(params)
     	 paramsfinal.writeToFile(options.output+options.log)
     	 logfile = open(options.output+options.log,"a::ios::ate")
     	 logfile.write("#################################################\n")
     	 for k in range(0,len(params)):
     	     pf = params.at(k)
	     print pf.GetName(), pf.getVal(), pf.getError(), "%.2f"%(pf.getVal()/pf.getError())
     	     if not("nonRes" in pf.GetName()):
     		 continue
     	     pi = paramsinit.at(k)
     	     r  = pi.getMax()-1
     	     logfile.write(pf.GetName()+" & "+str((pf.getVal()-pi.getVal())/r)+"\\\\ \n")
     	 logfile.close()

if __name__=="__main__":
     finMC = ROOT.TFile(options.input,"READ");
     hinMC = finMC.Get("nonRes");
     print options.name
     purity = options.channel  
     
     print "open file " +options.name
     f = ROOT.TFile(options.name,"READ")
     workspace = f.Get("w")
     workspace.var("MH").setVal(options.signalMass)
     workspace.var("MH").setConstant(1)
     f.Close()
     #workspace.Print()
     years = ["2016"]#,"2017"]
     model = workspace.pdf("model_b")
     model_b = workspace.pdf("model_b")
     if options.fitSignal: model = workspace.pdf("model_s")
     data_all = workspace.data("data_obs")
     args  = model.getComponents()
     data_all.Print()
     data = {}
     pdf1Name = {}
     all_expected = {}
     signal_expected= {}
     workspace.var("MJJ").setVal(2000)
     bkgs = ["nonRes","Wjets","Zjets","TTJetsTop","TTJetsW","TTJetsNonRes","TTJetsWNonResT","TTJetsResWResT" ,"TTJetsTNonResT"]
     #print number of events before the fit
     for year in years:
        data[year] = (workspace.data("data_obs").reduce("CMS_channel==CMS_channel::JJ_"+purity+"_13TeV_"+year))
        pdf1Name [year] =  "pdf_binJJ_"+purity+"_13TeV_"+year+"_bonly"
        if options.fitSignal: pdf1Name [year] =  "pdf_binJJ_"+purity+"_13TeV_"+year
        print "pdf1Name ",pdf1Name
        print
        print "Observed number of events in",purity,"category:"
        print data[year].sumEntries() ,"   ("+year+")"
        expected = {}
	N_expected_tot = 0
        for bkg in bkgs:
            if options.doVjets==False and (bkg=="Wjets" or bkg=="Zjets"): expected[bkg] = [None,None]; continue
            if options.addTop==False and (bkg.find("TTJets")!=-1): expected[bkg] = [None,None]; continue
            expected[bkg] = [ (args[pdf1Name[year]].getComponents())["n_exp_binJJ_"+purity+"_13TeV_"+year+"_proc_"+bkg],0.]
            print "Expected number of "+bkg+" events:",(expected[bkg][0].getVal()),"   ("+year+")"
	    N_expected_tot += (expected[bkg][0].getVal())
        all_expected[year] = expected 
        if options.fitSignal:
            print "Expected signal yields:",(args[pdf1Name[year]].getComponents())["n_exp_final_binJJ_"+purity+"_13TeV_2016_proc_"+signalName].getVal(),"(",year,")"
            signal_expected[year] = [ (args[pdf1Name[year]].getComponents())["n_exp_final_binJJ_"+purity+"_13TeV_2016_proc_"+signalName], 0.]
        else: signal_expected[year] = [0.,0.]
        print 
   
        print "Total number of expected background events:",N_expected_tot,"--> data/bkg =",data[year].sumEntries()/N_expected_tot,"(",year,")"
     ################################################# do the fit ###################################
     print
     
     if options.fit:
        fitresult = model.fitTo(data_all,ROOT.RooFit.SumW2Error(not(options.data)),ROOT.RooFit.Minos(0),ROOT.RooFit.Verbose(0),ROOT.RooFit.Save(1),ROOT.RooFit.NumCPU(8))  
        if options.label.find("sigonly")==-1:
            fitresult_bkg_only = model_b.fitTo(data_all,ROOT.RooFit.SumW2Error(not(options.data)),ROOT.RooFit.Minos(0),ROOT.RooFit.Verbose(0),ROOT.RooFit.Save(1),ROOT.RooFit.NumCPU(8))
        else: fitresult_bkg_only = fitresult
        fitresult.Print() 
        print 
        writeLogfile(options,fitresult)
     ############################################################################################
     

     #################################################
     
     ########### lets add all the pdfs we need ################
     allpdfs = {}
     allsignalpdfs={}
     for year in years:
        allpdfs[year] = []
        allsignalpdfs[year] = None
        for bkg in bkgs:
                if options.doVjets==False and (bkg=="Wjets" or bkg=="Zjets"): continue
                if options.addTop==False and (bkg.find("TTJets")!=-1): continue
                allpdfs[year].append(args["shapeBkg_"+bkg+"_JJ_"+purity+"_13TeV_"+year])
                print year, " shape ", bkg, " :"
                allpdfs[year][-1].Print()
                #allpdfs[year][-1].funcList().Print()
                #allpdfs[year][-1].coefList().Print()
        if options.fitSignal:
            allsignalpdfs[year] = args["shapeSig_"+signalName+"_JJ_"+purity+"_13TeV_"+year]
        else: allsignalpdfs[year] =None
        
        
        print 
        print year+" Prefit nonRes pdf:"
        pdf1_nonres_shape_prefit = args["nonResNominal_JJ_"+purity+"_13TeV_"+year]
        pdf1_nonres_shape_prefit.Print()
        print "Full "+year+" post-fit pdf:"     
        allpdfs[year].append( args[pdf1Name[year]+"_nuis"])
        allpdfs[year][-1].Print()
	
     allpdfsz = Postfitplotter.definefinalPDFs(options,"z",allpdfs)
     allpdfsx = Postfitplotter.definefinalPDFs(options,"x",allpdfs)
     allpdfsy = Postfitplotter.definefinalPDFs(options,"y",allpdfs)
     
     if options.fit:
        for year in years:
            expected = {}
            for bkg in bkgs:
                if options.doVjets==False and (bkg=="Wjets" or bkg=="Zjets"): expected[bkg] = [0.,0.]; continue
                if options.addTop==False and (bkg.find("TTJets")!=-1): expected[bkg] = [0.,0.]; continue
                print
                (args[pdf1Name[year]].getComponents())["n_exp_binJJ_"+purity+"_13TeV_"+year+"_proc_"+bkg].dump()
                expected[bkg] = [ (args[pdf1Name[year]].getComponents())["n_exp_binJJ_"+purity+"_13TeV_"+year+"_proc_"+bkg],(args[pdf1Name[year]].getComponents())["n_exp_binJJ_"+purity+"_13TeV_"+year+"_proc_"+bkg].getPropagatedError(fitresult)]
                print "normalization of "+bkg+" after fit:",(expected[bkg][0].getVal()), " +/- ",expected[bkg][1] ,"   ("+year+")"
            all_expected[year] = expected  
            if options.fitSignal:
                signal_expected[year] = [ (args[pdf1Name[year]].getComponents())["n_exp_final_binJJ_"+purity+"_13TeV_2016_proc_"+signalName], (args[pdf1Name[year]].getComponents())["n_exp_final_binJJ_"+purity+"_13TeV_2016_proc_"+signalName].getPropagatedError(fitresult)]
                print "Fitted signal yields:",signal_expected[year][0].getVal()," +/- ", signal_expected[year][bkg][1] ,"(",year,")"
            print 
          	 	 	
         
     logfile = open(options.output+options.log,"a::ios::ate")
     forplotting = Postfitplotter.Postfitplotter(options,logfile,signalName)
     forproj = Postfitplotter.Projection(hinMC,[options.xrange,options.yrange,options.zrange], workspace,options.fit)
     #make projections onto MJJ axis 
     if options.projection =="z":
         results = []
         for year in years:
            tmp = forproj.doProjection(data[year],allpdfsz[year],all_expected[year],"z",allsignalpdfs[year],signal_expected[year])
            results.append(tmp) 
         res = addResults(results)
         forplotting.MakePlots(res[0],res[1],res[2],res[3],res[4],res[5], res[6],res[7])
     #make projections onto MJ1 axis
     if options.projection =="x":
         results = []
         for year in years:
            tmp = forproj.doProjection(data[year],allpdfsx[year],all_expected[year],"x",allsignalpdfs[year],signal_expected[year])
            results.append(tmp)
         res = addResults(results)
         forplotting.MakePlots(res[0],res[1],res[2],res[3],res[4],res[5], res[6],res[7])
     #make projections onto MJ2 axis
     if options.projection =="y":
         results = []
         for year in years:
            tmp = forproj.doProjection(data[year],allpdfsy[year],all_expected[year],"y",allsignalpdfs[year],signal_expected[year])
            results.append(tmp)
         res = addResults(results)
         forplotting.MakePlots(res[0],res[1],res[2],res[3],res[4],res[5], res[6],res[7])

     if options.projection =="xyz":
         results = []
         for year in years:
            print data[year],allpdfsz[year],all_expected[year],"z",allsignalpdfs[year],signal_expected[year]
            tmp = forproj.doProjection(data[year],allpdfsz[year],all_expected[year],"z",allsignalpdfs[year],signal_expected[year])
            results.append(tmp) 
         res = addResults(results)
         forplotting.MakePlots(res[0],res[1],res[2],res[3],res[4],res[5], res[6],res[7])
    
         results = []
         for year in years:
            tmp = forproj.doProjection(data[year],allpdfsx[year],all_expected[year],"x",allsignalpdfs[year],signal_expected[year])
            results.append(tmp)
         res = addResults(results)
         forplotting.MakePlots(res[0],res[1],res[2],res[3],res[4],res[5], res[6],res[7])
         results = []
         for year in years:
            tmp = forproj.doProjection(data[year],allpdfsy[year],all_expected[year],"y",allsignalpdfs[year],signal_expected[year])
            results.append(tmp)
         res = addResults(results)
         forplotting.MakePlots(res[0],res[1],res[2],res[3],res[4],res[5], res[6],res[7])

        
     logfile.close()
     #################################################   
     #calculate chi2  
     #norm=norm_nonres+norm_res
     #chi2 = getChi2fullModel(pdf_nonres_shape_postfit,data,norm)
     #print "Chi2/ndof: %.2f/%.2f"%(chi2[0],chi2[1])," = %.2f"%(chi2[0]/chi2[1])," prob = ",ROOT.TMath.Prob(chi2[0], int(chi2[1]))
   
