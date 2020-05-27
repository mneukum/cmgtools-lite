#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
import os, sys, re, optparse,pickle,shutil,json
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

def returnString(func):
    st='0'
    for i in range(0,func.GetNpar()):
        st=st+"+("+str(func.GetParameter(i))+")"+("*MH"*i)
    return st    

def getBinning(binsMVV,minx,maxx,bins):
    l=[]
    if binsMVV=="":
        for i in range(0,bins+1):
            l.append(minx + i* (maxx - minx)/bins)
    else:
        s = binsMVV.split(",")
        for w in s:
            l.append(int(w))
    return l

def truncate(binning,mmin,mmax):
    res=[]
    for b in binning:
        if b >= mmin and b <= mmax:
            res.append(b)
    return res


def getMJPdf(mvv_min,mvv_max,MH,postfix="",fixPars="1"):
 
        var = ROOT.RooRealVar("MVV","MVV",mvv_min,mvv_max)
	
        pdfName 	= "signal_%d%s" %(MH,postfix)
        

        mean        = ROOT.RooRealVar("mean_%d%s"%(MH,postfix),"mean_%d%s"%(MH,postfix),MH ,0.8*MH,1.2*MH)
        sigma       = ROOT.RooRealVar("sigma_%d%s"%(MH,postfix),"sigma_%d%s"%(MH,postfix),MH*0.05,MH*0.02,MH*0.10)
        alpha       = ROOT.RooRealVar("alpha_%d%s"%(MH,postfix),"alpha_%d%s"%(MH,postfix),1.2,0.0,18)
        alpha2      = ROOT.RooRealVar("alpha2_%d%s"%(MH,postfix),"alpha2_%d%s"%(MH,postfix),1.2,0.0,10)
        sign        = ROOT.RooRealVar("sign_%d%s"%(MH,postfix),"sign_%d%s"%(MH,postfix),5,0,600)
        sign2        = ROOT.RooRealVar("sign2_%d%s"%(MH,postfix),"sign2_%d%s"%(MH,postfix),5,0,50)  
        
        if fixPars!="1":
            fixedPars =fixPars.split(',')
            for par in fixedPars:
                parVal = par.split(':')
                if len(parVal) > 1:
                    if par.find("MEAN")!=-1:
                        mean.setVal(float(parVal[1]))
                        mean.setConstant(1)
                    if par.find("SIGMA")!=-1:
                        sigma.setVal(float(parVal[1]))
                        sigma.setConstant(1)
                    if par.find("ALPHA1")!=-1:
                        alpha.setVal(float(parVal[1]))
                        alpha.setConstant(1)
                    if par.find("ALPHA2")!=-1:
                        alpha2.setVal(float(parVal[1]))
                        alpha2.setConstant(1)
                    if par.find("N1")!=-1:
                        sign.setVal(float(parVal[1]))
                        sign.setConstant(1)
                    if par.find("N2")!=-1:
                        sign2.setVal(float(parVal[1]))
                        sign2.setConstant(1)
       
	function = ROOT.RooDoubleCB(pdfName, pdfName, var, mean, sigma, alpha, sign,  alpha2, sign2)  
	return function,var,[mean,sigma,alpha,alpha2,sign,sign2]

def chooseBin(sample,b,binmidpoint):
    
    if sample.find('WZ')!=-1 :
        if b <= 55+2*binmidpoint : b = 80
        if b > 55+2*binmidpoint: b = 90
        return b
    elif sample.find('ZH')!=-1 or sample.find('Zh')!=-1:
        if b <= 55+binmidpoint*2 and b > 55: b = 90
        if b > 55+binmidpoint*2: b = 120
        return b
    elif sample.find('WH')!=-1 or sample.find('Wh')!=-1:
        if b <= 55+2*binmidpoint and b > 65: b = 80
        if b > 55+2*binmidpoint: b = 90
        return b
    
def dodCBFits(h1,mass,prefix,fixpars):
    
    func,var,params = getMJPdf(1126,5000,mass,options.sample,fixpars)
    data1 = ROOT.RooDataHist("dh","dh", ROOT.RooArgList(var), ROOT.RooFit.Import(h1)) 
    
    
    func.fitTo(data1,ROOT.RooFit.Range(mass*0.6,mass*1.3),ROOT.RooFit.PrintEvalErrors(-1))
    
    c3 = ROOT.TCanvas("test3","test3",400,400)
    frame = var.frame() 
    data1.plotOn(frame)
    func.plotOn(frame)
    frame.Draw()
   
    c3.SaveAs("test3_M"+str(mass)+"_"+prefix+".pdf")
    del func,var
    return { "MEAN":params[0].getVal(), "SIGMA": params[1].getVal(), "ALPHA1": params[2].getVal(), "ALPHA2": params[3].getVal() , "N1": params[4].getVal(), "N2": params[5].getVal(),"MEANERR":params[0].getError(), "SIGMAERR": params[1].getError(), "ALPHA1ERR": params[2].getError(), "ALPHA2ERR": params[3].getError() , "N1ERR": params[4].getError(), "N2ERR": params[5].getError()}
    

parser = optparse.OptionParser()
parser.add_option("-s","--sample",dest="sample",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("--addcut",dest="addcut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="Output JSON",default='')
parser.add_option("-V","--MVV",dest="mvv",help="mVV variable",default='')
parser.add_option("--fix",dest="fixPars",help="Fixed parameters",default="")
parser.add_option("-m","--minMVV",dest="min",type=float,help="mVV variable",default=1)
parser.add_option("-M","--maxMVV",dest="max",type=float, help="mVV variable",default=1)
parser.add_option("-r","--minMX",dest="minMX",type=float, help="smallest Mx to fit ",default=1000.0)
parser.add_option("-R","--maxMX",dest="maxMX",type=float, help="largest Mx to fit " ,default=7000.0)
parser.add_option("--binsMVV",dest="binsMVV",help="use special binning",default="")
parser.add_option("-t","--triggerweight",dest="triggerW",action="store_true",help="Use trigger weights",default=False)

(options,args) = parser.parse_args()
#define output dictionary


samples={}
graphs={'MEAN':ROOT.TGraphErrors(),'SIGMA':ROOT.TGraphErrors(),'ALPHA1':ROOT.TGraphErrors(),'N1':ROOT.TGraphErrors(),'ALPHA2':ROOT.TGraphErrors(),'N2':ROOT.TGraphErrors()}

testcorr= False


if options.sample.find("ZH")!=-1 or options.sample.find('Zh')!=-1 or options.sample.find("WZ")!=-1 or options.sample.find('WH')!=-1 or options.sample.find('Wh')!=-1:
    testcorr = True
print " ######### testcorr ",testcorr
for filename in os.listdir(args[0]):
    if not (filename.find(options.sample)!=-1):
        continue
    if filename.find("VBF")!=-1 and options.sample.find("VBF")==-1:
        continue

#found sample. get the mass
    fnameParts=filename.split('.')
    fname=fnameParts[0]
    ext=fnameParts[1]
    if ext.find("root") ==-1:
        continue
        
    
    mass = float(fname.split('_')[-1])
    if mass < options.minMX or mass > options.maxMX: continue
        

    samples[mass] = fname

    print 'found',filename,'mass',str(mass) 


#Now we have the samples: Sort the masses and run the fits
N=0
allgraphs = {}
allgraphs_sigma = {}
if (options.sample.find("H")!=-1 or options.sample.find("h")!=-1 or options.sample.find("WZ")!=-1):
    for mass in samples.keys():
        if samples[mass].find("WZ")!=-1:
            print 'histos for WZ signal'
            h = ROOT.TH2F("corr_mean_M"+str(mass),"corr_mean_M"+str(mass),2,array("f",[76,86,94]),2,array("f",[76,86,94]))
            hs = ROOT.TH2F("corr_sigma_M"+str(mass),"corr_sigma_M"+str(mass),2,array("f",[55,85,215]),2,array("f",[55,85,215]))

        elif samples[mass].find("WH")!=-1 or samples[mass].find("Wh")!=-1:
            print 'histos for WH signal'
            h = ROOT.TH2F("corr_mean_M"+str(mass),"corr_mean_M"+str(mass),2,array("f",[65,105,145]),2,array("f",[65,105,145]))
            hs = ROOT.TH2F("corr_sigma_M"+str(mass),"corr_sigma_M"+str(mass),2,array("f",[55,105,215]),2,array("f",[55,105,215]))    
        elif samples[mass].find("ZH")!=-1 or samples[mass].find("Zh")!=-1:
            print 'histos for ZH signal'
            h = ROOT.TH2F("corr_mean_M"+str(mass),"corr_mean_M"+str(mass),2,array("f",[85,105,145]),2,array("f",[85,105,145]))
            hs = ROOT.TH2F("corr_sigma_M"+str(mass),"corr_sigma_M"+str(mass),2,array("f",[55,105,215]),2,array("f",[55,105,215]))    
        
        allgraphs[mass] = h
        allgraphs_sigma[mass] = hs

    if samples[mass].find("WZ")!=-1:
        print 'sigma histo for WZ'
        graph_sum_sigma = ROOT.TH2F("corr_sigma","corr_sigma",2,array("f",[55,85,215]),2,array("f",[55,85,215]))
    else:
        print 'add sigma hist'
        graph_sum_sigma = ROOT.TH2F("corr_sigma","corr_sigma",2,array("f",[55,105,215]),2,array("f",[55,105,215]))

    if samples[mass].find("WZ")!=-1:
        print 'mean for WZ signal' 
        graph_sum_mean = ROOT.TH2F("corr_mean","corr_mean",2,array("f",[76,86,94]),2,array("f",[76,86,94]))
    elif options.sample.find("WH")!=-1 or samples[mass].find("Wh")!=-1:
        print 'mean for WH signal'
        graph_sum_mean  = ROOT.TH2F("corr_mean","corr_mean",2,array("f",[65,105,145]),2,array("f",[65,105,145]))
    elif samples[mass].find("ZH")!=-1 or samples[mass].find("Zh")!=-1:
        print 'mean for ZH signal'
        graph_sum_mean = ROOT.TH2F("corr_mean","corr_mean",2,array("f",[85,105,145]),2,array("f",[85,105,145]))
    minmjet = 55
    maxmjet = 215 
    binsmjet = 80
    bins_all = [[5,25],[25,50]]
    binmidpoint = 25
    if options.sample.find("WZ")!=-1:
        bins_all = [[5,15],[15,25]]
        binmidpoint = 15
    elif options.sample.find("WH")!=-1 or options.sample.find("Wh")!=-1:
        bins_all = [[5,15],[15,50]]
        binmidpoint = 15
    

for mass in sorted(samples.keys()):
    print 'fitting',str(mass) 
    plotter=TreePlotter(args[0]+'/'+samples[mass]+'.root','AnalysisTree')
    plotter.addCorrectionFactor('genWeight','tree')
    plotter.addCorrectionFactor('puWeight','tree')
    if options.triggerW:
        plotter.addCorrectionFactor('jj_triggerWeight','tree')	
        print "Using triggerweight"
   
    fitter=Fitter(['MVV'])
    fitter.signalResonance('model',"MVV",mass,False)
   
    fitter.w.var("MH").setVal(mass)

    extra_extra_cut = "&& (jj_LV_mass>%f&&jj_LV_mass<%f)"%(0.8*mass,1.1*mass)
    binning= truncate(getBinning(options.binsMVV,options.minMX,options.maxMX,500),0.80*mass,1.2*mass)    
    
    histo = plotter.drawTH1Binned(options.mvv,options.cut+extra_extra_cut,"1",binning)
    fitter.importBinnedData(histo,['MVV'],'data')
    ps = []
    if testcorr==True:
        histos2D = plotter.drawTH2("jj_LV_mass:jj_l2_softDrop_mass",options.cut.replace(options.addcut,"1"),"1",binsmjet,minmjet,maxmjet,100,options.min,options.max)
        proj = histos2D.ProjectionX("p")
      
        
        histos3D = plotter.drawTH3("jj_LV_mass:jj_l2_softDrop_mass:jj_l1_softDrop_mass",options.cut.replace(options.addcut,"1")+extra_extra_cut,"1",binsmjet,minmjet,maxmjet,binsmjet,minmjet,maxmjet,100,options.min,options.max)
       
        hall = histos3D.ProjectionZ("all",0,binmidpoint,binmidpoint,binsmjet)
        par = dodCBFits(hall,mass,"all","1")
        mean = par["MEAN"] 
        sigma = par["SIGMA"] 
        print " mean " +str(mean)
        n=0
        for bins in bins_all:
          for bins2 in bins_all:
            ps .append( histos3D.ProjectionZ("p2"+str(n+1),bins[0],bins[1],bins2[0],bins2[1]))
            
            par = dodCBFits(ps[-1],mass,str(n+1),"1")
            b1 = proj.GetBinCenter(bins[0])+ (proj.GetBinCenter(bins[1])-proj.GetBinCenter(bins[0]))/2. 
            b2 = proj.GetBinCenter(bins2[0])+ (proj.GetBinCenter(bins2[1])-proj.GetBinCenter(bins2[0]))/2.
            b1 = chooseBin(options.sample,b1,binmidpoint)
            b2 = chooseBin(options.sample,b2,binmidpoint)
            allgraphs[mass].Fill(b1 ,b2 , par['MEAN']/mean)
            allgraphs_sigma[mass].Fill(b1 ,b2 , par['SIGMA']/sigma)
            n+=1
       
   
    roobins = ROOT.RooBinning(len(binning)-1,array("d",binning))
   
   
    
    if options.fixPars!="1":
        fixedPars =options.fixPars.split(',')
        print fixedPars
        for par in fixedPars:
            parVal = par.split(':')
	    if len(parVal) > 1:
             fitter.w.var(parVal[0]).setVal(float(parVal[1]))
             fitter.w.var(parVal[0]).setConstant(1)

#    fitter.importBinnedData(histo,['MVV'],'data')
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0),ROOT.RooFit.Save()])
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0),ROOT.RooFit.Minos(1),ROOT.RooFit.Save()])
    
    fitter.projection("model","data","MVV","debugVV_"+options.output+"_"+str(mass)+".png",roobins)

    for var,graph in graphs.iteritems():
        value,error=fitter.fetch(var)
        graph.SetPoint(N,mass,value)
        graph.SetPointError(N,0.0,error)
                
    N=N+1
    fitter.delete()
    

F =ROOT.TFile(options.output,"RECREATE")
for name,graph in graphs.iteritems():
    graph.Write(name)
 
if testcorr==True:

    print "############### testcorr ###############"
    for mass in allgraphs.keys():
        graph_sum_sigma.Add(allgraphs_sigma[mass])
        graph_sum_mean.Add(allgraphs[mass])
    graph_sum_sigma.Scale(1/float(N))
    graph_sum_mean.Scale(1/float(N))
    print "sum mean",  graph_sum_mean
    print "sum sigma",  graph_sum_sigma
    graph_sum_sigma.Write()
    graph_sum_mean .Write()


F.Close()
            
