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

def returnString(func):
    st='0'
    for i in range(0,func.GetNpar()):
        st=st+"+("+str(func.GetParameter(i))+")"+("*MH"*i)
    return st    

def fillHisto(plotter,mvv,cuts,maxi,mini):
        print "ATTENTION: "+str(mvv)
        if mvv.find("l1")!=-1 or mvv.find("l2")!=-1:
            histo = plotter.drawTH1(mvv,cuts,"1",int((maxi-mini)/4),mini,maxi)
        else:
            histo = plotter.drawTH1(mvv.replace("random","l1"),cuts.replace("random","l1"),"1",int((maxi-mini)/4),mini,maxi) 
            tmp = plotter.drawTH1(mvv.replace("random","l2"),cuts.replace("random","l2"),"1",int((maxi-mini)/4),options.mini,options.maxi)
            histo.Add(tmp)
        return histo


parser = optparse.OptionParser()
parser.add_option("-s","--sample",dest="sample",default='',help="Type of sample")
parser.add_option("-c","--cut",dest="cut",help="Cut to apply for shape",default='')
parser.add_option("-o","--output",dest="output",help="Output JSON",default='')
parser.add_option("-V","--MVV",dest="mvv",help="mVV variable",default='')
parser.add_option("-m","--min",dest="mini",type=float,help="min MJJ",default=40)
parser.add_option("-M","--max",dest="maxi",type=float,help="max MJJ",default=160)
parser.add_option("-e","--exp",dest="doExp",type=int,help="useExponential",default=0)
parser.add_option("-f","--fix",dest="fixPars",help="Fixed parameters",default="1")
parser.add_option("-r","--minMX",dest="minMX",type=float, help="smallest Mx to fit ",default=1000.0)
parser.add_option("-R","--maxMX",dest="maxMX",type=float, help="largest Mx to fit " ,default=7000.0)
parser.add_option("-t","--triggerweight",dest="triggerW",action="store_true",help="Use trigger weights",default=False)

(options,args) = parser.parse_args()
#define output dictionary

isVH = False
isHH = False
samples={}


for filename in os.listdir(args[0]):
    if not (filename.find(options.sample)!=-1):
        continue
    if filename.find("VBF")!=-1 and options.sample.find("VBF")==-1:
        continue

    print ("hallo")
     
    fnameParts=filename.split('.')
    fname=fnameParts[0]
    ext=fnameParts[1]
    if ext.find("root") ==-1:
        continue
        
    #mass = float(fname.split('_')[-1])
    #if mass < options.minMX or mass > options.maxMX: continue	
    #samples[mass] = fname

    for i in range(6):
      EFTp = i*5		# now only for fs0: 0,5,10,15,20,25
      samples[EFTp] = fname
      print 'found',filename,'EFTparameter',str(EFTp) 
      if filename.find('hbb')!=-1: isVH=True;
      if filename.find("HH")!=-1: isHH=True; 
    

leg = options.mvv.split('_')[1]
print samples
print leg 
graphs={'mean':ROOT.TGraphErrors(),'sigma':ROOT.TGraphErrors(),'alpha':ROOT.TGraphErrors(),'n':ROOT.TGraphErrors(),'f':ROOT.TGraphErrors(),'slope':ROOT.TGraphErrors(),'alpha2':ROOT.TGraphErrors(),'n2':ROOT.TGraphErrors(),
        'meanH':ROOT.TGraphErrors(),'sigmaH':ROOT.TGraphErrors(),'alphaH':ROOT.TGraphErrors(),'nH':ROOT.TGraphErrors(),'fH':ROOT.TGraphErrors(),'slopeH':ROOT.TGraphErrors(),'alpha2H':ROOT.TGraphErrors(),'n2H':ROOT.TGraphErrors() }

#Now we have the samples: Sort the masses and run the fits
N=0
for mass in sorted(samples.keys()):

    if (mass > 0): continue
    print 'fitting',str(mass) 
    plotter=TreePlotter(args[0]+'/'+samples[mass]+'.root','AnalysisTree')
    plotter.addCorrectionFactor('genWeight','tree')
    plotter.addCorrectionFactor('puWeight','tree')

    eft_weight_string='EFT_weight['+str(mass*5)+']'	# the 5 is for fs0, should not be hard coded in the end!!! -> maybe add in .pckl file bc it is to be extracted from madgraph reweightcard ...
#    plotter.addCorrectionFactor(eft_weight_string,'tree')

    if options.triggerW:
     plotter.addCorrectionFactor('jj_triggerWeight','tree')
     print "Using triggerweight"
       


#    fitter.w.var("MH").setVal(mass)
    print options.mvv, options.cut, options.maxi, options.mini
    histo = fillHisto( plotter,options.mvv,options.cut,options.maxi,options.mini)
    debug = ROOT.TFile("/work/mneukum/aQGC_VBS_hadronic/3DFit_VBF_aQGC/CMGToolsForStat10X/CMSSW_10_2_10/src/CMGTools/VVResonances/interactive/debug_file.root","RECREATE")   
    histo.Write()
    debug.Write()
    debug.Close()


 
    fitter=Fitter(['x'])
    if isVH and options.cut.find('Truth')==-1: fitter.jetDoublePeakVH('model','x'); print "INFO: fit jet double peak";
    #if (not isVH and not isHH) or options.cut.find('VTruth')!=-1: fitter.jetResonanceNOEXP('model','x'); print "INFO: fit jetmass no exp "; # the function to fit is added to the RooWorkspace! 
    if (isVH and options.cut.find('HTruth')) or isHH: fitter.jetResonanceHiggs('model','x'); print "INFO: fit jetResonanceHiggs";

    # fixing the parameters defined in the .json    
#    if options.fixPars!="1":
#        fixedPars =options.fixPars.split(',')
#        print(fixedPars)
#        for par in fixedPars:
#            parVal = par.split(':')
#	    if len(parVal) > 1:
#             fitter.w.var(parVal[0]).setVal(float(parVal[1]))
#             fitter.w.var(parVal[0]).setConstant(1)

    fitter.importBinnedData(histo,['x'],'data')
    continue
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0)])
    fitter.fit('model','data',[ROOT.RooFit.SumW2Error(0),ROOT.RooFit.Minos(1)])
    fitter.projection("model","data","x","debugJ"+leg+"_"+options.output+"_"+str(mass)+".png")

    for var,graph in graphs.iteritems():
        value,error=fitter.fetch(var)
        graph.SetPoint(N,mass,value)
        graph.SetPointError(N,0.0,error)
                
    N=N+1
    fitter.delete()
        
sys.exit()
F=ROOT.TFile(options.output,"RECREATE")
F.cd()
for name,graph in graphs.iteritems():
    graph.Write(name)
F.Close()
            
