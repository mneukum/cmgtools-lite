import ROOT
ROOT.gROOT.SetBatch(True)
import os, sys, re, optparse,pickle,shutil,json
import time
from array import array
import math
import CMS_lumi
ROOT.gErrorIgnoreLevel = ROOT.kWarning
ROOT.gROOT.ProcessLine(".x tdrstyle.cc");


class Postfitplotter():
    logfile = ""
    options = None
    colors = [ROOT.kGray+2,ROOT.kRed,ROOT.kBlue,ROOT.kMagenta,210,210,ROOT.kMagenta,ROOT.kOrange,ROOT.kOrange,ROOT.kViolet,ROOT.kViolet]
    signalName = "BulkG"
    def __init__(self,options,logfile,signalName):
        print "initialize plotter"
        self.logfile = logfile
        self.options = options
        self.signalName = signalName

    def calculateChi2ForSig(self,hsig,pred,axis,logfile,label):
        if axis.find("z")!=-1:
            #logfile.open("testChi2.log","rw")
            chi2 = self.getChi2proj(pred,hsig)
            #print hsig.GetEntries(),hsig.Integral()
            logfile.write(label+"\n")
            if chi2[1]!=0:
                logfile.write("full chi2 \n ")
                logfile.write( "Projection %s: Chi2/ndf = %.2f/%i"%(axis,chi2[0],chi2[1])+"= %.2f"%(chi2[0]/chi2[1])+" prob = "+str(ROOT.TMath.Prob(chi2[0],chi2[1]))+"\n")
                logfile.write( "\n calculate Chi2 value around 2RMS of the mean value \n")
                
                mean = hsig.GetMean()
                rms = hsig.GetRMS()
                logfile.write( "mean : "+str(mean)+"  RMS "+str(rms)+" \n")
                chi2 = self.getChi2proj(pred,hsig,mean-rms,mean+rms)
                print hsig.GetEntries(),hsig.Integral()
                logfile.write( "Projection %s: Chi2/ndf = %.2f/%i"%(axis,chi2[0],chi2[1])+"= %.2f"%(chi2[0]/chi2[1])+" prob = "+str(ROOT.TMath.Prob(chi2[0],chi2[1]))+"\n")
                
                logfile.write("\n chi2 basen on window 10% around the mean:  \n")
                chi2 = self.getChi2proj(pred,hsig,mean*0.9,mean*1.1)
                print hsig.GetEntries(),hsig.Integral()
                logfile.write( "Projection %s: Chi2/ndf = %.2f/%i"%(axis,chi2[0],chi2[1])+"= %.2f"%(chi2[0]/chi2[1])+" prob = "+str(ROOT.TMath.Prob(chi2[0],chi2[1]))+"\n")
        

    def addPullPlot(self,hdata,hpostfit,nBins,error_band):
        #print "make pull plots: (data-fit)/sigma_data"
        N = hdata.GetNbinsX()
        gpost = ROOT.TGraphErrors(0)
        gt = ROOT.TH1F("gt","gt",len(nBins)-1,nBins)
        for i in range(1,N+1):
            m = hdata.GetXaxis().GetBinCenter(i)
            #ypostfit = (hdata.GetBinContent(i) - hpostfit.GetBinContent(i))/hdata.GetBinErrorUp(i)
            if hpostfit.GetBinContent(i) <= hdata.GetBinContent(i):
                if error_band !=0: ypostfit = (hdata.GetBinContent(i) - hpostfit.GetBinContent(i))/ ROOT.TMath.Abs(hdata.GetBinErrorUp(i))
                else: ypostfit = (hdata.GetBinContent(i) - hpostfit.GetBinContent(i))/ hdata.GetBinErrorUp(i)
            else:
                if error_band!=0: ypostfit = (hdata.GetBinContent(i) - hpostfit.GetBinContent(i))/ ROOT.TMath.Sqrt(ROOT.TMath.Abs( pow(hdata.GetBinErrorUp(i),2) - pow(error_band.GetErrorYlow(i-1),2) ))
                else: ypostfit = (hdata.GetBinContent(i) - hpostfit.GetBinContent(i))/ hdata.GetBinErrorUp(i)
            gpost.SetPoint(i-1,m,ypostfit)
            gt.SetBinContent(i,ypostfit)
            #print "bin",i,"x",m,"data",hdata.GetBinContent(i),"post fit",hpostfit.GetBinContent(i),"err data",hdata.GetBinErrorUp(i),"err fit",error_band.GetBinError(i),"pull postfit",ypostfit
            #print "bin",i,"x",m,"data",hdata.GetBinContent(i),"post fit",hpostfit.GetBinContent(i),"err data",hdata.GetBinErrorUp(i),"err fit",error_band.GetErrorYhigh(i-1),"pull postfit",ypostfit
                    
        gpost.SetLineColor(self.colors[1])
        gpost.SetMarkerColor(self.colors[1])
        gpost.SetFillColor(ROOT.kGray+3)
        gpost.SetMarkerSize(1)
        gpost.SetMarkerStyle(20)
        gt.SetFillColor(ROOT.kGray+3)
        gt.SetLineColor(ROOT.kGray+3)
        
        #gt = ROOT.TH1F("gt","gt",hdata.GetNbinsX(),hdata.GetXaxis().GetXmin(),hdata.GetXaxis().GetXmax())
        #gt = ROOT.TH1F("gt","gt",len(nBins)-1,nBins)
        gt.SetTitle("")
        #gt.SetMinimum(0.5);
        #gt.SetMaximum(1.5);
        gt.SetMinimum(-3.5);
        gt.SetMaximum(3.5);
        gt.SetDirectory(0);
        gt.SetStats(0);
        gt.SetLineStyle(0);
        gt.SetMarkerStyle(20);
        gt.GetXaxis().SetTitle(hpostfit.GetXaxis().GetTitle());
        gt.GetXaxis().SetLabelFont(42);
        gt.GetXaxis().SetLabelOffset(0.02);
        gt.GetXaxis().SetLabelSize(0.17);
        gt.GetXaxis().SetTitleSize(0.15);
        gt.GetXaxis().SetTitleOffset(1.2);
        gt.GetXaxis().SetTitleFont(42);
        gt.GetYaxis().SetTitle("#frac{Data-fit}{#sigma}");
        gt.GetYaxis().CenterTitle(True);
        gt.GetYaxis().SetNdivisions(205);
        gt.GetYaxis().SetLabelFont(42);
        gt.GetYaxis().SetLabelOffset(0.007);
        gt.GetYaxis().SetLabelSize(0.15);
        gt.GetYaxis().SetTitleSize(0.15);
        gt.GetYaxis().SetTitleOffset(0.4);
        gt.GetYaxis().SetTitleFont(42);
        gt.GetXaxis().SetNdivisions(505)
        #gpre.SetHistogram(gt);
        #gpost.SetHistogram(gt);       
        return [gt] 
    
    def addRatioPlot(self,hdata,hpostfit,nBins,error_band):
        #print "make pull plots: (data-fit)/sigma_data"
        N = hdata.GetNbinsX()
        gpost = ROOT.TGraphErrors(0)
        gt = ROOT.TH1F("gt","gt",len(nBins)-1,nBins)
        for i in range(1,N+1):
            m = hdata.GetXaxis().GetBinCenter(i)
            ypostfit = (hdata.GetBinContent(i)/hpostfit.GetBinContent(i))
            gpost.SetPoint(i-1,m,ypostfit)
            gt.SetBinContent(i,ypostfit)
            print "bin",i,"x",m,"data",hdata.GetBinContent(i),"post fit",hpostfit.GetBinContent(i),"err data",hdata.GetBinErrorUp(i),"err fit",error_band.GetBinError(i),"pull postfit",ypostfit
                    
        gpost.SetLineColor(self.colors[1])
        gpost.SetMarkerColor(self.colors[1])
        gpost.SetFillColor(ROOT.kBlue)
        gpost.SetMarkerSize(1)
        gpost.SetMarkerStyle(20)
        gt.SetFillColor(ROOT.kBlue)
        gt.SetLineColor(ROOT.kBlue)
        
        #gt = ROOT.TH1F("gt","gt",hdata.GetNbinsX(),hdata.GetXaxis().GetXmin(),hdata.GetXaxis().GetXmax())
        #gt = ROOT.TH1F("gt","gt",len(nBins)-1,nBins)
        gt.SetTitle("")
        #gt.SetMinimum(0.5);
        #gt.SetMaximum(1.5);
        gt.SetMinimum(0.001);
        gt.SetMaximum(1.999);
        gt.SetDirectory(0);
        gt.SetStats(0);
        gt.SetLineStyle(0);
        gt.SetMarkerStyle(20);
        gt.GetXaxis().SetTitle(hpostfit.GetXaxis().GetTitle());
        gt.GetXaxis().SetLabelFont(42);
        gt.GetXaxis().SetLabelOffset(0.02);
        gt.GetXaxis().SetLabelSize(0.17);
        gt.GetXaxis().SetTitleSize(0.15);
        gt.GetXaxis().SetTitleOffset(1);
        gt.GetXaxis().SetTitleFont(42);
        gt.GetYaxis().SetTitle("#frac{data}{fit}");
        gt.GetYaxis().CenterTitle(True);
        gt.GetYaxis().SetNdivisions(205);
        gt.GetYaxis().SetLabelFont(42);
        gt.GetYaxis().SetLabelOffset(0.007);
        gt.GetYaxis().SetLabelSize(0.15);
        gt.GetYaxis().SetTitleSize(0.15);
        gt.GetYaxis().SetTitleOffset(0.4);
        gt.GetYaxis().SetTitleFont(42);
        gt.GetXaxis().SetNdivisions(505)
        #gpre.SetHistogram(gt);
        #gpost.SetHistogram(gt);       
        return [gt]




    def getChi2fullModel(self,pdf,data,norm):
        pr=[]
        dr=[]
        for xk, xv in xBins.iteritems():
            MJ1.setVal(xv)
            for yk, yv in yBins.iteritems():
                MJ2.setVal(yv)
                for zk,zv in zBins.iteritems():
                    MJJ.setVal(zv)
                    dr.append(data.weight(argset))
                    binV = zBinsWidth[zk]*xBinsWidth[xk]*yBinsWidth[yk]
                    pr.append( pdf.getVal(argset)*binV*norm)
        ndof = 0
        chi2 = 0
        for i in range(0,len(pr)):
            if dr[i] < 10e-10:
                continue
            ndof+=1
            #chi2+= pow((dr[i] - pr[i]),2)/pr[i]
            if pr[i] > 10e-10:
                chi2+= 2*( pr[i] - dr[i] + dr[i]* ROOT.TMath.Log(dr[i]/pr[i]))

        return [chi2,ndof]

    def getChi2proj(self,histo_pdf,histo_data,minx=-1,maxx=-1):
        pr=[]
        dr=[]
        for b in range(1,histo_pdf.GetNbinsX()+1):
            if minx!=-1:
                if histo_pdf.GetBinCenter(b) < minx: continue
            if maxx!=-1:
                if histo_pdf.GetBinCenter(b) > maxx: continue
            dr.append(histo_data.GetBinContent(b))
            pr.append(histo_pdf.GetBinContent(b))
        
        ndof = 0
        chi2 = 0
        for i in range(0,len(pr)):
            if dr[i] < 10e-10:
                continue
            ndof+=1
            #chi2+= pow((dr[i] - pr[i]),2)/pr[i]
            #print i,dr[i],pr[i],(dr[i] - pr[i]),pow((dr[i] - pr[i]),2)/pr[i],(dr[i] - pr[i])/histo_data.GetBinError(i+1)
            if pr[i] > 10e-10:
                chi2+= 2*( pr[i] - dr[i] + dr[i]* ROOT.TMath.Log(dr[i]/pr[i]))

        return [chi2,ndof]       

    def get_canvas(self,cname):

        #change the CMS_lumi variables (see CMS_lumi.py)
        CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
        CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
        CMS_lumi.writeExtraText = 1
        if self.options.prelim==0:
            CMS_lumi.extraText = " "
        else:
            CMS_lumi.extraText = "Preliminary"

        H_ref = 600 
        W_ref = 600 
        W = W_ref
        H  = H_ref

        iPeriod = 0

        # references for T, B, L, R
        T = 0.08*H_ref
        B = 0.12*H_ref 
        L = 0.12*W_ref
        R = 0.04*W_ref

        canvas = ROOT.TCanvas(cname,cname,50,50,W,H)
        canvas.SetFillColor(0)
        canvas.SetBorderMode(0)
        canvas.SetFrameFillStyle(0)
        canvas.SetFrameBorderMode(0)
        canvas.SetLeftMargin( L/W )
        canvas.SetRightMargin( R/W )
        canvas.SetTopMargin( T/H )
        canvas.SetBottomMargin( B/H )
        canvas.SetTickx()
        canvas.SetTicky()
        
        return canvas

    def get_pad(self,name):

        #change the CMS_lumi variables (see CMS_lumi.py)
        CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
        CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
        period = "2016"
        if self.options.name.find("2017")!=-1: period = "2017"
        if self.options.name.find("16+17")!=-1: period = "16+17"
        if self.options.name.find("Run2")!=-1: period = "Run2"
        if period =="2016":  CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
        if period =="2017":  CMS_lumi.lumi_13TeV = "77.3 fb^{-1}"
        if period =="16+17":  CMS_lumi.lumi_13TeV = "113.2 fb^{-1}"
        if period =="run2":  CMS_lumi.lumi_13TeV = "run2 fb^{-1}"
        CMS_lumi.writeExtraText = 1
        CMS_lumi.lumi_sqrtS = "13 TeV (2016+2017)" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
        if self.options.prelim==0:
            CMS_lumi.extraText = " "
        if self.options.prelim==1:
            CMS_lumi.extraText = "Preliminary"
        if self.options.prelim==2:
            CMS_lumi.extraText = "Supplementary"

        CMS_lumi.lumiText = "(13 TeV)"
        iPos = 0
        if( iPos==0 ): CMS_lumi.relPosX = 0.014
        CMS_lumi.relPosX=0.05
        H_ref = 600 
        W_ref = 600 
        W = W_ref
        H  = H_ref

        iPeriod = 0
        iPeriod = 4

        pad = ROOT.TPad(name, name, 0, 0.3, 1, 1.0)
        pad.SetFillColor(0)
        pad.SetBorderMode(0)
        pad.SetFrameFillStyle(0)
        pad.SetFrameBorderMode(0)
        pad.SetTickx()
        pad.SetTicky()
        
        pad.SetBottomMargin(0.01)    
        pad.SetTopMargin(0.1) 
        
        return pad



    def MakePlots(self,histos,hdata,hsig,axis,nBins,maxY=-1.,normsig = 1.,errors=None):
        print histos
        extra1 = ''
        extra2 = ''
        htitle = ''
        xtitle = ''
        ymin = 0
        ymax = 0
        xrange = self.options.xrange
        yrange = self.options.yrange
        zrange = self.options.zrange
        if self.options.xrange == '0,-1': xrange = '55,215'
        if self.options.yrange == '0,-1': yrange = '55,215'
        if self.options.zrange == '0,-1': zrange = '1126,5500'
        if axis=='z':
            print "make Z projection"
            htitle = "Z-Proj. x : "+self.options.xrange+" y : "+self.options.yrange
            hhtitle = self.options.channel
            xtitle = "Dijet invariant mass [GeV]"
            ymin = 0.2
            ymax = max(hdata.GetMaximum()*5000,maxY*5000)
            extra1 = xrange.split(',')[0]+' < m_{jet1} < '+ xrange.split(',')[1]+' GeV'
            extra2 = yrange.split(',')[0]+' < m_{jet2} < '+ yrange.split(',')[1]+' GeV'
        elif axis=='x':
            print "make X projection"
            htitle = "X-Proj. y : "+self.options.yrange+" z : "+self.options.zrange
            hhtitle = self.options.channel
            xtitle = " m_{jet1} [GeV]"
            ymin = 0.02
            ymax = hdata.GetMaximum()*2#max(hdata.GetMaximum()*1.3,maxY*1.3)
            extra1 = yrange.split(',')[0]+' < m_{jet2} < '+ yrange.split(',')[1]+' GeV'
            extra2 = zrange.split(',')[0]+' < m_{jj} < '+ zrange.split(',')[1]+' GeV'
        elif axis=='y':
            print "make Y projection"
            htitle = "Y-Proj. x : "+self.options.xrange+" z : "+self.options.zrange
            hhtitle = self.options.channel
            xtitle = " m_{jet2} [GeV]"
            ymin = 0.02
            ymax = hdata.GetMaximum()*2#max(hdata.GetMaximum()*1.3,maxY*1.3)
            extra1 = xrange.split(',')[0]+' < m_{jet1} < '+ xrange.split(',')[1]+' GeV'
            extra2 = zrange.split(',')[0]+' < m_{jj} < '+ zrange.split(',')[1]+' GeV'
                    
        #leg = ROOT.TLegend(0.450436242,0.5531968,0.7231544,0.8553946)
        leg = ROOT.TLegend(0.40809045,0.5063636,0.7622613,0.8520979)
        leg.SetTextSize(0.05)
        c = self.get_canvas('c')
        pad1 = self.get_pad("pad1") #ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
        if axis == 'z': pad1.SetLogy()

        pad1.Draw()
        pad1.cd()	 
    
        histos[0].SetMinimum(ymin)
        histos[0].SetMaximum(ymax) 
        histos[0].SetTitle(hhtitle)
        histos[0].SetLineColor(self.colors[0])
        histos[0].SetLineWidth(2)
        histos[0].GetXaxis().SetTitle(xtitle)
        histos[0].GetYaxis().SetTitleOffset(1.3)
        histos[0].GetYaxis().SetTitle("Events")
        histos[0].GetYaxis().SetTitleOffset(1.3)
        histos[0].GetYaxis().SetTitle("Events / 2 GeV")
        if axis == 'z': histos[0].GetYaxis().SetTitle("Events / 100 GeV")
        histos[0].GetYaxis().SetTitleSize(0.06)
        histos[0].GetYaxis().SetLabelSize(0.06)
        histos[0].Draw('HIST')
        print "---------------------------------------------------------------------------------------"
        print histos[0].Integral()
        print "---------------------------------------------------------------------------------------"

        if len(histos)>1:
            histos[1].SetLineColor(self.colors[1])
            histos[1].SetLineWidth(2)
            
            histos[2].SetLineColor(self.colors[2])
            histos[2].SetLineWidth(2)
            
        
            if self.options.addTop:
                histos[3].SetLineColor(self.colors[3])
                histos[3].SetLineWidth(2)
            
        for i in range(4,len(histos)):
            histos[i].SetLineColor(self.colors[i])
            histos[i].Draw("histsame")
            name = histos[i].GetName().split("_")
            if len(name)>2:
                leg.AddEntry(histos[i],name[1],"l")
            else:
                leg.AddEntry(histos[i],name[0],"l")
        hdata.SetMarkerStyle(20)
        hdata.SetMarkerColor(ROOT.kBlack)
        hdata.SetLineColor(ROOT.kBlack)
        hdata.SetMarkerSize(0.7)
        
        if errors!=None:
            errors[0].SetFillColor(self.colors[0])
            errors[0].SetFillStyle(3001)
            errors[0].SetLineColor(self.colors[0])
            errors[0].SetLineWidth(0)
            errors[0].SetMarkerSize(0)
        
        
        #change this scaling in case you don't just want to plot signal! has to match number of generated signal events


        scaling = self.options.signalScaleF
        eff = 0.1
        
        
        if hsig!= None: # and (self.options.name.find('sigonly')!=-1  and doFit==0):
            print "print do hsignal ", hsig.Integral()
            if hsig.Integral()!=0.:   
                hsig.Scale(scaling/normsig)
        #        print "sig integral ",hsig.Integral()
        #        hsig.Scale(scaling/hsig.Integral())
        
            hsig.SetFillColor(ROOT.kGreen-6)
            hsig.SetLineColor(ROOT.kBlack)
            hsig.SetLineStyle(1)
            #hsig.SetTitle("category  "+self.options.channel)
            hsig.Draw("HISTsame")
            #leg.AddEntry(hsig,"Signal pdf","F")
            
        #errors[0].Draw("E5same")
        if errors!=None:
            if axis=="z":
                errors[0].Draw("2same")
            else:
                errors[0].Draw("3same")
        histos[0].SetTitle("category  "+self.options.channel)
        histos[0].Draw("samehist")
        if len(histos)>1:
            if self.options.addTop: histos[3].Draw("histsame") 
            histos[1].SetLineStyle(7)
            histos[2].SetLineStyle(6)
            histos[1].Draw("histsame") 
            histos[2].Draw("histsame")
        hdata.Draw("samePE0")         
        leg.SetLineColor(0)
        
        
        leg.AddEntry(hdata,"Data","ep")
        leg.AddEntry(histos[0],"Signal+background fit","l")
        if errors!=None:
            leg.AddEntry(errors[0],"#pm 1#sigma unc.","f")
        if len(histos)>1:    
            leg.AddEntry(histos[1],"W+jets","l")
            leg.AddEntry(histos[2],"Z+jets","l")
        if len(histos)>2:
            if self.options.addTop: leg.AddEntry(histos[3],"t#bar{t}","l")
        
        text = "G_{bulk} (%.1f TeV) #rightarrow WW (#times %i)"%(self.options.signalMass/1000.,scaling)
        if (self.options.signalMass%1000.)==0:
            text = "G_{bulk} (%i TeV) #rightarrow WW (#times %i)"%(self.options.signalMass/1000.,scaling) 
        
        if self.signalName.find("ZprimeWW")!=-1:
            text = "Z' (%.1f TeV) #rightarrow WW (#times %i)"%(self.options.signalMass/1000.,scaling)
            if (self.options.signalMass%1000.)==0:
                text = "Z' (%i TeV) #rightarrow WW (#times %i)"%(self.options.signalMass/1000.,scaling) 
                
        if self.signalName.find("ZprimeZH")!=-1:
            text = "Z' (%.1f TeV) #rightarrow ZH (#times %i)"%(self.options.signalMass/1000.,scaling)
            if (self.options.signalMass%1000.)==0:
                text = "Z' (%i TeV) #rightarrow ZH (#times %i)"%(self.options.signalMass/1000.,scaling) 
                
                
        if self.signalName.find("WprimeWZ")!=-1:
            text = "W' (%.1f TeV) #rightarrow WZ (#times %i)"%(self.options.signalMass/1000.,scaling)
            if (self.options.signalMass%1000.)==0:
                text = "W' (%i TeV) #rightarrow WZ (#times %i)"%(self.options.signalMass/1000.,scaling) 
                
        if self.signalName.find("WprimeWH")!=-1:
            text = "W' (%.1f TeV) #rightarrow WH (#times %i)"%(self.options.signalMass/1000.,scaling)
            if (self.options.signalMass%1000.)==0:
                text = "W' (%i TeV) #rightarrow WH (#times %i)"%(self.options.signalMass/1000.,scaling) 
        
        if self.options.fitSignal==True: 
            leg.AddEntry(hsig,text,"F")
        leg.Draw("same")
        
        #errors[0].Draw("E2same")
        print "projection "+extra1+"  "+extra2+" \n"
        
        chi2 = self.getChi2proj(histos[0],hdata)
        print hdata.GetEntries(),hdata.Integral()
        if chi2[1]!=0:
            print "Projection %s: Chi2/ndf = %.2f/%i"%(axis,chi2[0],chi2[1]),"= %.2f"%(chi2[0]/chi2[1])," prob = ",ROOT.TMath.Prob(chi2[0],chi2[1])

        pt = ROOT.TPaveText(0.18,0.06,0.54,0.17,"NDC")
        pt.SetTextFont(42)
        pt.SetTextSize(0.05)
        pt.SetTextAlign(12)
        pt.SetFillColor(0)
        pt.SetBorderSize(0)
        pt.SetFillStyle(0)
        if chi2[1]!=0:
            pt.AddText("Chi2/ndf = %.2f/%i = %.2f"%(chi2[0],chi2[1],chi2[0]/chi2[1]))
            pt.AddText("Prob = %.3f"%ROOT.TMath.Prob(chi2[0],chi2[1]))
        #pt.Draw()

        #pt2 = ROOT.TPaveText(0.55,0.29,0.99,0.4,"NDC")
        pt2 = ROOT.TPaveText(0.55,0.35,0.99,0.52,"NDC")
        pt2.SetTextFont(42)
        pt2.SetTextSize(0.05)
        pt2.SetTextAlign(12)
        pt2.SetFillColor(0)
        pt2.SetBorderSize(0)
        pt2.SetFillStyle(0)
        pt2.AddText("category  "+self.options.channel)
        pt2.AddText(extra1)
        pt2.AddText(extra2)
        pt2.Draw()

        pt3 = ROOT.TPaveText(0.65,0.39,0.99,0.52,"NDC")
        pt3.SetTextFont(42)
        pt3.SetTextSize(0.05)
        pt3.SetTextAlign(12)
        pt3.SetFillColor(0)
        pt3.SetBorderSize(0)
        pt3.SetFillStyle(0)
        #pt3.AddText("%s category"%self.options.channel)
        #pt3.AddText(extra1)
        #pt3.AddText(extra2)
        #pt3.Draw()

        CMS_lumi.CMS_lumi(pad1, 4, 10)
        
        pad1.Modified()
        pad1.Update()
        
        c.Update()
        c.cd()
        pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.4)
        #pad2.SetGridy()
        pad2.Draw()
        pad2.cd()
        
        #for ratio
        #graphs = addRatioPlot(hdata,histos[0],nBins,errors[0])
        #graphs[1].Draw("AP")
        #graphs[0].Draw("E3same")
        #graphs[1].Draw("Psame")
        
        #for pulls
        if errors ==None: errors=[0,0];
        if self.options.name.find('sigonly')!=-1: graphs = self.addPullPlot(hdata,hsig,nBins,errors[0])
        else:
            graphs = self.addPullPlot(hdata,histos[0],nBins,errors[0])
        # graphs = addRatioPlot(hdata,histos[0],nBins,errors[0])
        graphs[0].Draw("HIST")

        pad2.Modified()
        pad2.Update()
        
        c.cd()
        c.Update()
        c.Modified()
        c.Update()
        c.cd()
        c.SetSelected(c)
        #errors[0].Draw("E2same")
        #CMS_lumi.CMS_lumi(c, 0, 11)
        #c.cd()
        #c.Update()
        #c.RedrawAxis()
        #frame = c.GetFrame()
        #frame.Draw()
        
        self.calculateChi2ForSig(hdata,hsig,axis,self.logfile,"\n \n projection "+extra1+"  "+extra2+" \n")
        if self.options.prelim==0:
            c.SaveAs(self.options.output+"PostFit"+self.options.label+"_"+htitle.replace(' ','_').replace('.','_').replace(':','_').replace(',','_')+".png")
            c.SaveAs(self.options.output+"PostFit"+self.options.label+"_"+htitle.replace(' ','_').replace('.','_').replace(':','_').replace(',','_')+".pdf")
            c.SaveAs(self.options.output+"PostFit"+self.options.label+"_"+htitle.replace(' ','_').replace('.','_').replace(':','_').replace(',','_')+".C")
            c.SaveAs(self.options.output+"PostFit"+self.options.label+"_"+htitle.replace(' ','_').replace('.','_').replace(':','_').replace(',','_')+".root")
        else:
            c.SaveAs(self.options.output+"PostFit"+self.options.label+"_"+htitle.replace(' ','_').replace('.','_').replace(':','_').replace(',','_')+"_prelim.png")
            c.SaveAs(self.options.output+"PostFit"+self.options.label+"_"+htitle.replace(' ','_').replace('.','_').replace(':','_').replace(',','_')+"_prelim.pdf")
            c.SaveAs(self.options.output+"PostFit"+self.options.label+"_"+htitle.replace(' ','_').replace('.','_').replace(':','_').replace(',','_')+"_prelim.C")
            c.SaveAs(self.options.output+"PostFit"+self.options.label+"_"+htitle.replace(' ','_').replace('.','_').replace(':','_').replace(',','_')+"_prelim.root")


class Projection():
    xBins_redux ={}
    yBins_redux ={}
    zBins_redux ={}
    xBinsWidth ={}
    yBinsWidth ={}
    zBinsWidth ={}
    
    BinsWidth_1 ={}
    BinsWidth_2 ={}
    BinsWidth_3 ={}
    
    
    Bins_redux ={}
    Bins_redux_1 ={}
    Bins_redux_2 ={}

    xBinslowedge =[]
    yBinslowedge =[]
    zBinslowedge =[]
    Binslowedge =[]
    neventsPerBin_1 = {}
    
    h=[]
    hfinals = []
    lv=[]
    lv1_sig=[]
    h1_sig = 0
    dh = None
    data = None
    h1_sig = None
    
    M1=None
    M2=None
    M3=None
    argset_ws = None
    workspace = None
    htot_sig = None
    htot_nonres = None
    htot_Wres = None
    htot_Zres = None
    htot_TTJets = None
    htot = None
    doFit = False
    axis = ""
    maxYaxis = 0
    
    
    def __init__(self,hinMC,opt_range,workspace,doFit):
        self.workspace = workspace
        #################################################
        xBins= self.getListOfBins(hinMC,"x")
        self.xBinslowedge = self.getListOfBinsLowEdge(hinMC,'x')
        self.xBinsWidth   = self.getListOfBinsWidth(hinMC,"x")     
        #################################################
        yBins= self.getListOfBins(hinMC,"y")
        self.yBinslowedge = self.getListOfBinsLowEdge(hinMC,'y')     
        self.yBinsWidth   = self.getListOfBinsWidth(hinMC,"y")
        #################################################
        zBins= self.getListOfBins(hinMC,"z")
        self.zBinslowedge = self.getListOfBinsLowEdge(hinMC,'z')
        self.zBinsWidth   = self.getListOfBinsWidth(hinMC,"z")
        ################################################# 
        
        #################################################
        x = self.getListFromRange(opt_range[0])
        y = self.getListFromRange(opt_range[1])
        z = self.getListFromRange(opt_range[2])     
        
        self.xBins_redux = self.reduceBinsToRange(xBins,x)
        self.yBins_redux = self.reduceBinsToRange(yBins,y)
        self.zBins_redux = self.reduceBinsToRange(zBins,z)

        ################################################# 
    
    def getListFromRange(self,xyzrange):
        r=[]
        a,b = xyzrange.split(",")
        r.append(float(a))
        r.append(float(b))
        return r


    def getListOfBins(self,hist,dim):
        axis =0
        N = 0
        if dim =="x":
            axis= hist.GetXaxis()
            N = hist.GetNbinsX()
        if dim =="y":
            axis = hist.GetYaxis()
            N = hist.GetNbinsY()
        if dim =="z":
            axis = hist.GetZaxis()
            N = hist.GetNbinsZ()
        if axis==0:
            return {}
        
        mmin = axis.GetXmin()
        mmax = axis.GetXmax()
        bins ={}
        for i in range(1,N+1): bins[i] = axis.GetBinCenter(i) 
        
        return bins


    def getListOfBinsLowEdge(self,hist,dim):
        axis =0
        N = 0
        if dim =="x":
            axis= hist.GetXaxis()
            N = hist.GetNbinsX()
        if dim =="y":
            axis = hist.GetYaxis()
            N = hist.GetNbinsY()
        if dim =="z":
            axis = hist.GetZaxis()
            N = hist.GetNbinsZ()
        if axis==0:
            return {}
        
        mmin = axis.GetXmin()
        mmax = axis.GetXmax()
        r=[]
        for i in range(1,N+2): r.append(axis.GetBinLowEdge(i)) 
        
        return array("d",r)


    def getListOfBinsWidth(self,hist,dim):
        axis =0
        N = 0
        if dim =="x":
            axis= hist.GetXaxis()
            N = hist.GetNbinsX()
        if dim =="y":
            axis = hist.GetYaxis()
            N = hist.GetNbinsY()
        if dim =="z":
            axis = hist.GetZaxis()
            N = hist.GetNbinsZ()
        if axis==0:
            return {}
        
        mmin = axis.GetXmin()
        mmax = axis.GetXmax()
        r ={}
        for i in range(0,N+2):
            #v = mmin + i * (mmax-mmin)/float(N)
            r[i] = axis.GetBinWidth(i) 
        return r 

    
    def reduceBinsToRange(self,Bins,r):
        if r[0]==0 and r[1]==-1:
            return Bins
        result ={}
        for key, value in Bins.iteritems():
            if value >= r[0] and value <=r[1]:
                result[key]=value
        return result


    def doProjection(self,data,pdfs,norms,axis,pdf_sig=None,norm_sig=0):
        self.neventsPerBin_1 = {}
        self.h=[]
        self.hfinals = []
        self.lv=[]
        self.lv1_sig=[]
        self.h1_sig = 0
        self.dh = None
        self.data = None
        self.h1_sig = None
        self.maxYaxis = 0
        self.axis = axis
        if axis=="x":
           self.dh = ROOT.TH1F("dh","dh",len(self.xBinslowedge)-1,self.xBinslowedge)
           self.Bins_redux = self.xBins_redux
           self.Bins_redux_1 = self.yBins_redux
           self.Bins_redux_2 = self.zBins_redux
           self.Binslowedge = self.xBinslowedge
           self.BinsWidth_1 = self.xBinsWidth
           self.BinsWidth_2 = self.yBinsWidth
           self.BinsWidth_3 = self.zBinsWidth
           # get variables from workspace 
           self.M1 = self.workspace.var("MJ1");
           self.M2 = self.workspace.var("MJ2");
           self.M3 = self.workspace.var("MJJ");
           for xk,xv in self.xBins_redux.iteritems():
                self.neventsPerBin_1[xk]=0
        if axis=="y":
           self.dh = ROOT.TH1F("dh","dh",len(self.yBinslowedge)-1,self.yBinslowedge)
           self.Bins_redux = self.yBins_redux
           self.Bins_redux_1 = self.xBins_redux
           self.Bins_redux_2 = self.zBins_redux
           self.BinsWidth_1 = self.yBinsWidth
           self.BinsWidth_2 = self.xBinsWidth
           self.BinsWidth_3 = self.zBinsWidth
           self.Binslowedge = self.yBinslowedge
           # get variables from workspace 
           self.M1 = self.workspace.var("MJ2");
           self.M2 = self.workspace.var("MJ1");
           self.M3 = self.workspace.var("MJJ");
           for yk,yv in self.yBins_redux.iteritems():
                self.neventsPerBin_1[yk]=0
        if axis=="z":
           self.dh = ROOT.TH1F("dh","dh",len(self.zBinslowedge)-1,self.zBinslowedge)
           self.Bins_redux = self.zBins_redux
           self.Bins_redux_1 = self.xBins_redux
           self.Bins_redux_2 = self.yBins_redux
           self.BinsWidth_1 = self.zBinsWidth
           self.BinsWidth_2 = self.xBinsWidth
           self.BinsWidth_3 = self.yBinsWidth
           self.Binslowedge = self.zBinslowedge
           # get variables from workspace 
           self.M1 = self.workspace.var("MJJ");
           self.M2 = self.workspace.var("MJ1");
           self.M3 = self.workspace.var("MJ2");
           for zk,zv in self.zBins_redux.iteritems():
                self.neventsPerBin_1[zk]=0 
        argset = ROOT.RooArgSet();
        argset.add(self.M3);
        argset.add(self.M2);
        argset.add(self.M1);
        self.args_ws = argset
        print "initialize histograms with ",self.Binslowedge
        self.data = ROOT.RooDataHist("data","data",self.args_ws,data)
        self.htot_nonres = ROOT.TH1F("htot_nonres","htot_nonres",len(self.Binslowedge)-1,self.Binslowedge)
        self.htot_sig = ROOT.TH1F("htot_sig","htot_sig",len(self.Binslowedge)-1,self.Binslowedge)
        self.htot = ROOT.TH1F("htot","htot",len(self.Binslowedge)-1,self.Binslowedge)
        self.htot_Wres = ROOT.TH1F("htot_Wres","htot_Wres",len(self.Binslowedge)-1,self.Binslowedge)
        self.htot_Zres = ROOT.TH1F("htot_Zres","htot_Zres",len(self.Binslowedge)-1,self.Binslowedge)
        self.htot_TTJets = ROOT.TH1F("htot_TTJets","htot_TTJets",len(self.Binslowedge)-1,self.Binslowedge)
         
        for p in pdfs:
            self.h.append( ROOT.TH1F("h_"+p.GetName(),"h_"+p.GetName(),len(self.Binslowedge)-1,self.Binslowedge))
            self.lv.append({})
        for i in range(0,len(pdfs)):
            for ik,iv in self.Bins_redux.iteritems(): self.lv[i][iv]=0
        
        if pdf_sig!=None:
                self.h1_sig = ROOT.TH1F("h1_"+pdf_sig.GetName(),"h1_"+pdf_sig.GetName(),len(self.Binslowedge)-1,self.Binslowedge)
                self.lv1_sig.append({})
                for ik,iv in self.Bins_redux.iteritems(): self.lv1_sig[0][iv]=0
	
    	
        for ik, iv in self.Bins_redux_1.iteritems():
            self.M2.setVal(iv)
            for jk, jv in self.Bins_redux_2.iteritems():
                self.M3.setVal(jv)
                for kk,kv in self.Bins_redux.iteritems():
                    self.M1.setVal(kv)
                    self.neventsPerBin_1[kk] += self.data.weight(self.args_ws)
                    i=0
                    binV = self.BinsWidth_2[ik]*self.BinsWidth_3[jk]*self.BinsWidth_1[kk]
                    for p in pdfs:
                        if "nonRes" in str(p.GetName()) : 
                            self.lv[i][kv] += p.getVal(self.args_ws)*binV*norms["nonRes"][0].getVal()
                        if "Wjets" in str(p.GetName()) : 
                            self.lv[i][kv] += p.getVal(self.args_ws)*binV*norms["Wjets"][0].getVal()
                        if "Zjets" in str(p.GetName()) : 
                            self.lv[i][kv] += p.getVal(self.args_ws)*binV*norms["Zjets"][0].getVal()
                        if "TTJetsTop" in str(p.GetName()) : 
                            self.lv[i][kv] += p.getVal(self.args_ws)*binV*norms["TTJetsTop"][0].getVal()
                        if "TTJetsW" in str(p.GetName()) : 
                            self.lv[i][kv] += p.getVal(self.args_ws)*binV*norms["TTJetsW"][0].getVal()
                        if "TTJetsNonRes" in str(p.GetName()) : 
                            self.lv[i][kv] += p.getVal(self.args_ws)*binV*norms["TTJetsNonRes"][0].getVal()
                            print norms["TTJetsNonRes"][0].getVal()
                        i+=1
                    if pdf_sig!=None:
                        self.lv1_sig[0][kv] += pdf_sig.getVal(self.args_ws)*binV
        return self.fillHistos(pdfs,data,norms,pdf_sig,norm_sig)
        
    def fillHistos(self,pdfs,data,norms,pdf_sig=None,norm_sig=None):
        print " make Projection ", self.axis
        for i in range(0,len(pdfs)):
            for ik,iv in self.Bins_redux.iteritems():
                tmp = self.lv[i][iv]
                if tmp >+ self.maxYaxis: self.maxYaxis = tmp
                if "nonRes" in str(pdfs[i].GetName()) : self.htot_nonres.Fill(iv,self.lv[i][iv]); 
                elif "Wjets" in str(pdfs[i].GetName()) : self.htot_Wres.Fill(iv,self.lv[i][iv]); 
                elif "Zjets" in str(pdfs[i].GetName()) : self.htot_Zres.Fill(iv,self.lv[i][iv]); 
                elif "TTJetsTop" in str(pdfs[i].GetName()): self.htot_TTJets.Fill(iv,self.lv[i][iv])
                elif "TTJetsW" in str(pdfs[i].GetName()): self.htot_TTJets.Fill(iv,self.lv[i][iv])
                elif "TTJetsNonRes" in str(pdfs[i].GetName()): self.htot_TTJets.Fill(iv,self.lv[i][iv])
                else: self.h[i].Fill(iv,tmp);
        
        if pdf_sig!=None:
            print "fill signal "
            for ik,iv in self.Bins_redux.iteritems(): self.htot_sig.Fill(iv,self.lv1_sig[0][iv]*norm_sig[0]); # print self.lv1_sig[0][iv]*norm_sig[0]    
     
        self.htot.Add(self.htot_nonres)
        if self.htot_Wres!=None: self.htot.Add(self.htot_Wres)
        if self.htot_Zres!=None: self.htot.Add(self.htot_Zres)
        if self.htot_TTJets!=None: self.htot.Add(self.htot_TTJets)
        if self.htot_sig!=None: self.htot.Add(self.htot_sig); 
        print "htot sig ",str(self.htot_sig.Integral())
        print "htot integral" , self.htot.Integral()
        print "htot_Wres integral" , self.htot_Wres.Integral()
        self.hfinals.append(self.htot)
        if self.htot_Wres!=None: self.hfinals.append(self.htot_Wres)
        if self.htot_Zres!=None: self.hfinals.append(self.htot_Zres)
        if self.htot_TTJets!=None: self.hfinals.append(self.htot_TTJets)
        #for i in range(10,len(h)): hfinals.append(h[i])    
        for b,v in self.neventsPerBin_1.iteritems(): self.dh.SetBinContent(b,self.neventsPerBin_1[b]);
        self.dh.SetBinErrorOption(ROOT.TH1.kPoisson)
        if self.doFit:
            errors = self.draw_error_band(norms,pdfs[-1])
        else: errors =  None
        return [self.hfinals,self.dh, self.htot_sig,self.axis,self.Binslowedge,self.maxYaxis, norm_sig[0],errors]
        
    
    def draw_error_band(self,norms,rpdf1):
        histo_central = self.htot
        norm1 = norms["nonRes"][0]+norms["Wjets"][0]+norms["Zjets"][0]+norms["TTJets"][0]
        err_norm1 = math.sqrt(norms["nonRes"][1]*norms["nonRes"][1]+norms["Wjets"][1]*norms["Wjets"][1]+norms["Zjets"][1]*norms["Zjets"][1]+norms["TTJets"][1]*norms["TTJets"][1])
        x_min = self.Binslowedge
        proj = self.axis
        rand = ROOT.TRandom3(1234);
        number_errorband = 5
        syst = [0 for i in range(number_errorband)]
      
        value = [0 for x in range(len(x_min))]  
        number_point = len(value)
    
        par_pdf1 = rpdf1.getParameters(self.args_ws)  
        iter = par_pdf1.createIterator()
        var = iter.Next()
        print var.GetName()
        for j in range(number_errorband):
            syst[j] = ROOT.TGraph(number_point+1);
        #paramters value are randomized using rfres and this can be done also if they are not decorrelate
        if self.options.label.find("sigonly")==-1:
            par_tmp = ROOT.RooArgList(fitresult_bkg_only.randomizePars())
        else:
            par_tmp = ROOT.RooArgList(fitresult.randomizePars())
        iter = par_pdf1.createIterator()
        var = iter.Next()

        while var:
            index = par_tmp.index(var.GetName())
            if index != -1:
                #print "pdf1",var.GetName(), var.getVal()
                var.setVal(par_tmp.at(index).getVal())     
                #print " ---> new value: ",var.getVal()
            var = iter.Next()
      
        norm1_tmp = rand.Gaus(norm1,err_norm1); #new poisson random number of events
        value = [0 for i in range(number_point)]
        for ik, iv in self.Bins_redux.iteritems():
            self.M1.setVal(iv)
            for jk, jv in self.Bins_redux_1.iteritems():
                self.M2.setVal(jv)
                for kk,kv in self.Bins_redux_2.iteritems():
                    self.M3.setVal(kv)
                    binV = self.BinsWidth_1[ik]*self.BinsWidth_2[jk]*self.BinsWidth_3[kk]
                    value[ik-1] += (norm1_tmp*rpdf1.getVal( self.args_ws )*binV)
                   
        for ix,x in enumerate(x_min): 
            syst[j].SetPoint(ix, x, value[ix])

            #Try to build and find max and minimum for each point --> not the curve but the value to do a real envelope -> take one 2sigma interval        
            errorband = ROOT.TGraphAsymmErrors()#ROOT.TH1F("errorband","errorband",len(x_min)-1,x_min)

            val = [0 for i in range(number_errorband)]
            for ix,x in enumerate(x_min):
    
                for j in range(number_errorband):
                    val[j]=(syst[j]).GetY()[ix]
                val.sort()
                errorband.SetPoint(ix,x_min[ix]+histo_central.GetBinWidth(ix+1)/2.,histo_central.GetBinContent(ix+1))
                errup = (val[int(0.84*number_errorband)]-histo_central.GetBinContent(ix+1)) #ROOT.TMath.Abs
                errdn = ( histo_central.GetBinContent(ix+1)-val[int(0.16*number_errorband)])
                print "error up "+str(errup)+" error down "+str(errdn)
                errorband.SetPointError(ix,histo_central.GetBinWidth(ix+1)/2.,histo_central.GetBinWidth(ix+1)/2.,ROOT.TMath.Abs(errdn),ROOT.TMath.Abs(errup))
        errorband.SetFillColor(ROOT.kBlack)
        errorband.SetFillStyle(3008)
        errorband.SetLineColor(ROOT.kGreen)
        errorband.SetMarkerSize(0)
       
        return [errorband]
    
    
def definefinalPDFs(options,axis,allpdfs):
    allpdfsz = allpdfs
    listofextrapdf = []
    if axis=="z":
         #let's have always pre-fit and post-fit as firt elements here, and add the optional shapes if you want with options.pdf
         listofextrapdf = options.pdfz.split(",")
    if axis=="x": listofextrapdf = options.pdfx.split(",")
    if axis=="x": listofextrapdf = options.pdfy.split(",")
    for p in listofextrapdf:
        if p == '': continue
        print "add pdf:",p
        args[p].Print()
        if p.find("2016")!=-1:
            allpdfsz["2016"].append(args[p])
        if p.find("2017")!=-1:
            allpdfsz["2017"].append(args[p])
        if p.find("2018")!=-1:
            allpdfsz["2018"].append(args[p])
    return allpdfsz
