
#!/usr/bin/env python

import ROOT
from array import array
from CMGTools.VVResonances.plotting.TreePlotter import TreePlotter
from CMGTools.VVResonances.plotting.MergedPlotter import MergedPlotter
from CMGTools.VVResonances.plotting.StackPlotter import StackPlotter
from CMGTools.VVResonances.statistics.Fitter import Fitter
from math import log
from cuts import cuts
import os, sys, re, optparse,pickle,shutil,json
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

def returnString(func):
    st='0'
    for i in range(0,func.GetNpar()):
        st=st+"+("+str(func.GetParameter(i))+")"+("*MH"*i)
    return st    


parser = optparse.OptionParser()
parser.add_option("-s","--sample",dest="sample",default='',help="Type of sample")
parser.add_option("-c","--cat",dest="cat",help="category for cuts to apply",default='')
parser.add_option("-V","--MVV",dest="mvv",help="mVV variable",default='')
parser.add_option("-t","--toy",dest="toy",help="test by using toys with 1000 events",action="store_true")
parser.add_option("-m","--min",dest="mini",type=float,help="min MJJ",default=40)
parser.add_option("-M","--max",dest="maxi",type=float,help="max MJJ",default=160)
parser.add_option("-e","--exp",dest="doExp",type=int,help="useExponential",default=1)
parser.add_option("-r","--minMX",dest="minMX",type=float, help="smallest Mx to fit ",default=1100.0)
parser.add_option("-R","--maxMX",dest="maxMX",type=float, help="largest Mx to fit " ,default=7000.0)
parser.add_option("--fitResults",dest="fitResults",default="debug_JJ_BulkGWW_MJl1_HPLP.json.root",help="name of root file containing the fitted curves for each parameter")

(options,args) = parser.parse_args()
#define output dictionary

samples={}

title = "Dijet invariant mass [GeV]"







def getVal(mass,param,File):
    f = File.Get(param+"_func")
    print f
    val = f.Eval(mass)
    return val


def getValues(mass,params,File):
    print mass 
    print params
    print File
    val = {}
    for p in params:
        print p
        val[p] = getVal(mass,p,File)
    #if options.sample.find("WJets")!=-1:
        #val["mean"]=83.
    return val

def setPDF(vals,variabletype, sampletype, doExp, Fitter):
    if variabletype.find("l1")!=-1 or variabletype.find("l2")!=-1 :
        print "make mjet plots "
        #fitter=Fitter(['x'])
        if doExp==1:
                Fitter.jetResonance('model','x')
        else:
            if sampletype.find("ZH")!=-1 or sampletype.find('WH')!=-1 or sampletype.find("Zh")!=-1 or sampletype.find('Wh')!=-1:
            
                Fitter.jetDoublePeakVH('model','x')
            else:
                Fitter.jetResonanceNOEXP('model','x')
    else:
        print "make mVV plots "
        Fitter.signalResonance('model','MVV',mass)
        Fitter.w.var("MH").setVal(mass)
    for v in vals.keys():
            print "set vars " +v +" to "+str(vals[v])
            Fitter.w.var(v).setVal(vals[v])
            Fitter.w.var(v).setConstant(1)
        

def beautifyPull(gpre,title):
    gpre.SetTitle("")
    if title.find("jet")!=-1:
        gpre.GetXaxis().SetRangeUser(55,215)
    gpre.GetXaxis().SetTitle(title)
    gpre.GetYaxis().SetTitle("pull")
    gpre.GetYaxis().SetTitleSize(0.15)
    gpre.GetYaxis().SetTitleOffset(0.2)
    gpre.GetXaxis().SetTitleSize(0.15)
    gpre.GetXaxis().SetTitleOffset(0.7)
    gpre.GetXaxis().SetLabelSize(0.15)
    gpre.GetYaxis().SetLabelSize(0.15)
    gpre.GetXaxis().SetNdivisions(6)
    gpre.GetYaxis().SetNdivisions(4)
    gpre.SetMaximum(5)
    gpre.SetMinimum(-5)
    return gpre


def printHistContent(histo,pullDist):
    for b in range(1,histo.GetNbinsX()):
        i = histo.GetBinCenter(b)
        #fitters[N].w.var("x").setVal(i)
        print str(i)+" "+str(round(histo.GetBinContent(b),4))+ "  "+str(round(pullDist.Eval(i),4))


def truncate(binning,mmin,mmax):
    res=[]
    for b in binning:
        if b >= mmin and b <= mmax:
            res.append(b)
            print b
    return res
    

if __name__=="__main__":
    x=1100
    y=1000
    if options.mvv.find("l1")!=-1 or options.mvv.find("l2")!=-1:
        title="m_{jet1} [GeV]"
        x= options.mini + 50
    shapes = ["mean","sigma","alpha","n","alpha2","n2"]
    shapesH = ["meanH","sigmaH","alphaH","nH","alpha2H","n2H"]
    xvar = 'x'
    #if options.sample.find("Wprime")!=-1:
    #    shapes = ['meanW','sigmaW','alphaW','n','f','alphaW2','meanZ','sigmaZ','alphaZ','alphaZ2']
        
    if options.mvv.find("LV_mass")!=-1:
        shapes = ["MEAN","SIGMA","ALPHA1","N1","ALPHA2","N2"]
        xvar ="MVV"

    label="G_{bulk} #rightarrow WW"
    if options.sample.find("Zprime")!=-1:
        label = "Z' #rightarrow WW"
        if options.sample.find("ZH")!=-1 or options.sample.find("Zh")!=-1:label = "Z' #rightarrow ZH"
    if options.sample.find("Wprime")!=-1:
        label = "W' #rightarrow WZ"
        if options.sample.find("WH")!=-1 or options.sample.find("Wh")!=-1:label = "W' #rightarrow WH"
    if options.sample.find("Bulk")!=-1 and options.sample.find("ZZ")!=-1:
        label="G_{bulk} #rightarrow ZZ"

    for filename in os.listdir(args[0]):
        #print filename
        if not (filename.find(options.sample)!=-1):
            continue
    #found sample. get the mass
        fnameParts=filename.split('.')
        fname=fnameParts[0]
        ext=fnameParts[1]
        if ext.find("root") ==-1:
            continue
        print filename

        if fname.split('_')[-1] == "HT600toInf":
            mass = 1001
        else:
            mass = float(fname.split('_')[-1])
        #if mass < options.minMX or mass > options.maxMX: continue	

            
        if mass <=1000:
            continue
        if mass >5000:
            continue
        if mass ==1600:
            continue
        samples[mass] = fname

        print 'found',filename,'mass',str(mass) 

    leg = options.mvv.split('_')[1]

    #Now we have the samples: Sort the masses and make histograms
    
    h={}
    fitters=[]
    frames=[]
    tmp = []
    N=0
    print options.fitResults
    fitfiles = (options.fitResults).split(',')
    print fitfiles
    File =[]
    for f in fitfiles:
        File.append(ROOT.TFile(f,"READ"))
    histos = []
    for mass in sorted(samples.keys()):
        c = ROOT.TCanvas("c","c",600,600)
        c.SetTickx()
        c.SetTicky()
        if options.sample.find("WJets")!=-1:
            c.Divide(1,0)
        else:
            c.Divide(1,0)
            
        
        
        if options.mvv.find("LV_mass")!=-1:
            x = mass*1.1
        values =  getValues(mass,shapes,File[0])
        if len(File)>1:
            values.update(getValues(mass,shapesH,File[1]))
        print 'make histos ',str(mass) 
        plotter=TreePlotter(args[0]+'/'+samples[mass]+'.root','AnalysisTree')
        plotter.addCorrectionFactor('genWeight','AnalysisTree')
        plotter.addCorrectionFactor('puWeight','AnalysisTree')
        #plotter.addCorrectionFactor('genWeight_LO','AnalysisTree')
        
        fitters.append(Fitter([xvar]))
        if options.mvv.find("LV_mass")!=-1:
            frames.append(fitters[N].w.var(xvar).frame(mass*0.75,mass*1.25))
            #binning=[1, 3, 6, 10, 16, 23, 31, 40, 50, 61, 74, 88, 103, 119, 137, 156, 176, 197, 220, 244, 270, 296, 325, 354, 386, 419, 453, 489, 526, 565, 606, 649, 693, 740, 788, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337,4509, 4686, 4869, 5058, 5253, 5455, 5663, 5877, 6099, 6328, 6564, 6808]
            #truncatedbinning = truncate(binning,mass*0.75,mass*1.25)
            ##truncatedbinning = binning
            #histo = plotter.drawTH1Binned(options.mvv,cuts['common']+'*'+cuts['acceptance']+'*'+cuts[options.cat]+"*(jj_LV_mass>%f&&jj_LV_mass<%f)"%(0.75*mass,1.25*mass),"1",array("d",truncatedbinning))
            p = 10.
            pmin = 10.
            if mass < 2000:
                p =8.
                pmin = 12.
            if mass >= 2000 and mass < 3500:
                p =10.
                pmin =10.
            if mass >=3500:
                p = 12.
                pmin = 14.
            
            massmin = mass - mass/pmin
            if massmin< 1126.:
                massmin=1126.
            
            tmp.append(plotter.drawTH1(options.mvv,cuts['common']+'*'+cuts['acceptance']+'*'+cuts[options.cat],"1",30,massmin,mass + mass/p))
            ngev = (mass+mass/10.-massmin)/30.
            histos.append(ROOT.TH1F("tmp"+str(mass),"tmp"+str(mass),30,massmin,mass + mass/p))
            histo = histos[-1]
            
            #histos[-1].FillRandom(tmp[-1],int(1000))
            #fitters[N].importBinnedData(histos[-1],[xvar],'data')
            fitters[N].importBinnedData(tmp[-1],[xvar],'data')
        
            
        else:
            frames.append(fitters[N].w.var(xvar).frame(55,215))
            tmp.append(plotter.drawTH1(options.mvv,cuts['common']+'*'+cuts['acceptance']+'*'+cuts[options.cat],"1",20,options.mini,options.maxi))
            histos.append(ROOT.TH1F("tmp"+str(mass),"tmp"+str(mass),20,options.mini,options.maxi))
            ngev = (options.maxi-options.mini)/20.
            histo = histos[-1]
            
            if options.toy==True:
                histos[-1].FillRandom(tmp[-1],int(1000))
                fitters[N].importBinnedData(histos[-1],[xvar],'data')
            else:
                histo = plotter.drawTH1(options.mvv,cuts['common']+'*'+cuts['acceptance']+'*'+cuts[options.cat],"1",20,options.mini,options.maxi)
                fitters[N].importBinnedData(histo,[xvar],'data')
                

        setPDF(values,options.mvv, options.sample, options.doExp, fitters[N])
     
        #if options.sample.find("WJets")==-1:       
            #c.cd(N+1)
            #print "++++++++++++++++++++++++++++++"
            #print " go to pad "+str(N+1)
            #print "++++++++++++++++++++++++++++++"
        c.cd()
        #pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
        pad1 = ROOT.TPad("pad1"+str(mass), "pad1"+str(mass), 0, 0., 1., 1.0)
        pad1.SetTickx()
        pad1.SetTicky()
        pad1.SetBottomMargin(0.15)
        pad1.SetLeftMargin(0.17)
        pad1.Draw()                                                                                       
        pad1.cd()
 
        res =  fitters[N].getFrame("model","data",xvar,title,mass)
        res[0].GetXaxis().SetTitleSize(0.06)
        res[0].GetXaxis().SetLabelSize(0.06)
        res[0].GetXaxis().SetLabelOffset(0.018)
        res[0].GetYaxis().SetTitleSize(0.06)
        res[0].GetYaxis().SetLabelSize(0.06)
        res[0].GetYaxis().SetTitleOffset(1.4)
        res[0].GetXaxis().SetTitleOffset(1.2)
        res[0].GetYaxis().SetTitle("Events / "+str(round(ngev,1))+" GeV")
        res[0].SetNdivisions(5)
        res[0].GetYaxis().SetNdivisions(5)
        res[0].SetTitle(label+", "+str(int(mass))+" GeV")
        y = histo.GetBinContent(histo.GetMaximumBin())*2/3.
        res[0].SetMaximum(y*2.5)
        res[0].Draw("same")
        print "+++++++++++++++++++++++++++++++++"
        print res[0]
        print y
        print "+++++++++++++++++++++++++++++++++"
        res[1].Draw("same")
        
        chi2 = ROOT.TLatex()
        
        chi2.DrawLatexNDC(0.2,0.6,options.cat)
        chi2.DrawLatexNDC(0.2,0.65,"#chi^{2}/ndof. = "+str(round(res[3],2)))
        if options.sample.find("WJets")==-1:
            c.cd(N+1)
        else:
            c.cd(N)
        #pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
        #pad2.SetTopMargin(0.1)
        #pad2.SetBottomMargin(0.3)
        #pad2.SetGridy()
        #pad2.SetGridx()
        #pad2.Draw()
        #pad2.cd()
        #if options.mvv.find("LV_mass")!=-1:
            #res[2].GetXaxis().SetRangeUser(mass*0.75,mass*1.25)
        #beautifyPull(res[2],title).Draw()
        print res[0].getObject(1)
        N+=1
        del histo, res, plotter
        
        fname = options.fitResults.split(',')[0].replace(".json.root","_"+options.cat+"_M"+str(int(mass))+".pdf")
        if fname.find('Vjet')!=-1: fname = fname.replace('Vjet','')
        if options.toy==True: print 'whyyyyyyyyyyy'; print fname ;fname = fname.replace("NP","NP_toy")
        if options.mvv.find("l2")!=-1 and fname.find("l1")!=-1:
            fname = fname.replace("l1","l2")
        if options.sample.find("WJets")!=-1:
            fname = "WJetsToQQ.pdf"
        c.Update()
        c.SaveAs(fname)
        c.SaveAs(fname.replace(".pdf",".png"))
    print options.toy
    del fitters,Fitter,frames,tmp, histos
