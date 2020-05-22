import ROOT
from ROOT import *
from array import array
import sys, math

class PostFitTools():

 def __init__(self,hist,argset,xrange,yrange,zrange,label,outdir,data):
  print "PostFitTools__init__!"
  self.xrange = xrange
  self.yrange = yrange
  self.zrange = zrange
  self.argset = argset
  self.setBins(hist)
  self.label = label
  self.output = outdir
  self.colors = [ROOT.kBlack,ROOT.kPink-1,ROOT.kAzure+1,ROOT.kAzure+1,210,210,ROOT.kMagenta,ROOT.kMagenta,ROOT.kOrange,ROOT.kOrange,ROOT.kViolet,ROOT.kViolet]

  self.ndata = {}
  self.errdata_lo = {}
  self.errdata_hi = {}
  for xk, xv in self.xBins.iteritems():
    self.ndata[xv] = {}
    self.errdata_lo[xv] = {}
    self.errdata_hi[xv] = {}
    for yk, yv in self.yBins.iteritems():
      self.ndata[xv][yv] = {}
      self.errdata_lo[xv][yv] = {}
      self.errdata_hi[xv][yv] = {}
      for zk,zv in self.zBins.iteritems():
  	 self.ndata[xv][yv][zv] = 0
  	 self.errdata_lo[xv][yv][zv] = 0
  	 self.errdata_hi[xv][yv][zv] = 0

  data_ = ROOT.RooDataHist("data_","data_",self.argset,data)
  for i in range(data_.numEntries()):
    entry = data_.get(i)
    mj1 = entry.find('MJ1').getVal()
    mj2 = entry.find('MJ2').getVal()
    mjj = entry.find('MJJ').getVal()
    self.ndata[mj1][mj2][mjj] = data_.weight()
    hi = ROOT.Double(0.)
    lo = ROOT.Double(0.)
    data_.weightError(lo,hi)
    self.errdata_lo[mj1][mj2][mjj] = lo
    self.errdata_hi[mj1][mj2][mjj] = hi

 def setBins(self,hist):
 
     self.xBins = self.getListOfBins(hist,"x")
     self.xBinslowedge = self.getListOfBinsLowEdge(hist,'x')
     self.xBinsWidth   = self.getListOfBinsWidth(hist,"x")
     self.yBins= self.getListOfBins(hist,"y")
     self.yBinslowedge = self.getListOfBinsLowEdge(hist,'y')     
     self.yBinsWidth   = self.getListOfBinsWidth(hist,"y")
     self.zBins= self.getListOfBins(hist,"z")
     self.zBinslowedge = self.getListOfBinsLowEdge(hist,'z')
     self.zBinsWidth   = self.getListOfBinsWidth(hist,"z")

     x = self.getListFromRange(self.xrange)
     y = self.getListFromRange(self.yrange)
     z = self.getListFromRange(self.zrange)     
     
     self.xBins_redux = self.reduceBinsToRange(self.xBins,x)
     self.yBins_redux = self.reduceBinsToRange(self.yBins,y)
     self.zBins_redux = self.reduceBinsToRange(self.zBins,z)
      
 def getBins(self):
 
     return [self.xBins,self.xBinslowedge,self.xBinsWidth,self.yBins,self.yBinslowedge,self.yBinsWidth,self.zBins,self.zBinslowedge,self.zBinsWidth]   
      
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
    
 def doZprojection(self,pdfs,data,norm,proj=0):
    data_ = ROOT.RooDataHist("data_","data_",self.argset,data)
    h=[]
    lv=[]
    dh = ROOT.TH1F("dh","dh",len(self.zBinslowedge)-1,self.zBinslowedge)
    neventsPerBin = [0 for zv in range(len(self.zBins_redux))]
    for p in pdfs:
        h.append( ROOT.TH1F("h_"+p.GetName(),"h_"+p.GetName(),len(self.zBinslowedge)-1,self.zBinslowedge))
        lv.append({})
    for i in range(0,len(pdfs)):
        for zk,zv in self.zBins_redux.iteritems():
            lv[i][zv]=0    
    for xk, xv in self.xBins_redux.iteritems():
         self.argset['MJ1'].setVal(xv)
         for yk, yv in self.yBins_redux.iteritems():
             self.argset['MJ2'].setVal(yv)
             for zk,zv in self.zBins_redux.iteritems():
                 self.argset['MJJ'].setVal(zv)
                 neventsPerBin[zk-1] += data_.weight(self.argset)
                 i=0
                 binV = self.zBinsWidth[zk]*self.xBinsWidth[xk]*self.yBinsWidth[yk]     
                 for p in pdfs:
                    if "pdfdata" in p.GetName():
                            lv[i][zv] += p.weight(self.argset)
                    else:
                            lv[i][zv] += p.getVal(self.argset)*binV
                    i+=1
    for i in range(0,len(pdfs)):
        for zk,zv in self.zBins_redux.iteritems():
            if "pdfdata" in pdfs[i].GetName():
                h[i].Fill(zv,lv[i][zv])
            else:
                h[i].Fill(zv,lv[i][zv]*norm)
     
    for b,e in enumerate(neventsPerBin): dh.SetBinContent(b+1,e)           
    dh.SetBinErrorOption(ROOT.TH1.kPoisson)
    self.MakePlots(h,dh,'z',self.zBinslowedge)    

 def doXprojection(self,pdfs,data,norm,hin=0):
    data_ = ROOT.RooDataHist("data_","data_",self.argset,data)
    h=[]
    lv=[]
    proj = ROOT.TH1F("px","px",len(self.xBinslowedge)-1,self.xBinslowedge)
    neventsPerBin = [0 for xv in range(len(self.xBins_redux))]
    
    for p in pdfs:
        h.append( ROOT.TH1F("hx_"+p.GetName(),"hx_"+p.GetName(),len(self.xBinslowedge)-1,self.xBinslowedge))
        lv.append({})
    for xk, xv in self.xBins_redux.iteritems():
         self.argset['MJ1'].setVal(xv)
         for i in range(0,len(pdfs)):
            lv[i][xv]=0
         for yk, yv in self.yBins_redux.iteritems():
             self.argset['MJ2'].setVal(yv)
             for zk,zv in self.zBins_redux.iteritems():
                 self.argset['MJJ'].setVal(zv)
                 i=0
                 binV = self.zBinsWidth[zk]*self.xBinsWidth[xk]*self.yBinsWidth[yk]
                 neventsPerBin[xk-1] += data_.weight(self.argset)
                 for p in pdfs:
                     if "postfit" in p.GetName():
                         if "data_" in p.GetName():
                            lv[i][xv] += p.weight(self.argset)#p.evaluate()*binV
                         else:
                             lv[i][xv] += p.evaluate()*binV
                     else:
                        lv[i][xv] += p.getVal(self.argset)*binV
                     i+=1
    for i in range(0,len(pdfs)):
        for key, value in lv[i].iteritems():
            if "pdfdata" in pdfs[i].GetName():
                h[i].Fill(key,value)
            else:
                h[i].Fill(key,value*norm)

    for b,e in enumerate(neventsPerBin): proj.SetBinContent(b+1,e)
    proj.SetBinErrorOption(ROOT.TH1.kPoisson)
    self.MakePlots(h,proj,'x',self.xBinslowedge)    

 def doYprojection(self,pdfs,data,norm):
    data_ = ROOT.RooDataHist("data_","data_",self.argset,data)
    h=[]
    lv=[]
    proj = ROOT.TH1F("py","py",len(self.yBinslowedge)-1,self.yBinslowedge)
    neventsPerBin = [0 for yv in range(len(self.yBins_redux))]
    for p in pdfs:
        h.append( ROOT.TH1F("hy_"+p.GetName(),"hy_"+p.GetName(),len(self.yBinslowedge)-1,self.yBinslowedge))
        lv.append({})
    for yk, yv in self.yBins_redux.iteritems():
         self.argset['MJ2'].setVal(yv)
         for i in range(0,len(pdfs)):
            lv[i][yv]=0
         for xk, xv in self.xBins_redux.iteritems():
             self.argset['MJ1'].setVal(xv)
             for zk,zv in self.zBins_redux.iteritems():
                 self.argset['MJJ'].setVal(zv)
                 i=0
                 neventsPerBin[yk-1] += data_.weight(self.argset)
                 binV = self.zBinsWidth[zk]*self.xBinsWidth[xk]*self.yBinsWidth[yk]
                 for p in pdfs:
                    if "pdfdata" in p.GetName():
                            lv[i][yv] += p.weight(self.argset)#p.evaluate()*binV
                    else:
                            lv[i][yv] += p.getVal(self.argset)*binV
                    i+=1
    for i in range(0,len(pdfs)):
        for key, value in lv[i].iteritems():
            if "pdfdata" in pdfs[i].GetName():
                h[i].Fill(key,value)
            else:
                h[i].Fill(key,value*norm)

    for b,e in enumerate(neventsPerBin): proj.SetBinContent(b+1,e)      
    proj.SetBinErrorOption(ROOT.TH1.kPoisson)
    self.MakePlots(h,proj,'y',self.yBinslowedge) 
 
 def doZprojection2(self,pdfs,data,norm,proj=0):
    data_ = ROOT.RooDataHist("data_","data_",self.argset,data)
    h=[]
    lv=[]
    dh = ROOT.TH1F("dh","dh",len(self.zBinslowedge)-1,self.zBinslowedge)
    neventsPerBin = [0 for zv in range(len(self.zBins_redux))]
    errPerBin = [0 for zv in range(len(self.zBins_redux))]
    for p in pdfs:
        h.append( ROOT.TH1F("h_"+p.GetName(),"h_"+p.GetName(),len(self.zBinslowedge)-1,self.zBinslowedge))
        lv.append({})
    for i in range(0,len(pdfs)):
        for zk,zv in self.zBins_redux.iteritems():
            lv[i][zv]=0    
    for xk, xv in self.xBins_redux.iteritems():
         self.argset['MJ1'].setVal(xv)
         for yk, yv in self.yBins_redux.iteritems():
             self.argset['MJ2'].setVal(yv)
             for zk,zv in self.zBins_redux.iteritems():
                 self.argset['MJJ'].setVal(zv)
                 neventsPerBin[zk-1] += self.ndata[xv][yv][zv]
		 errPerBin[zk-1] += self.errdata_lo[xv][yv][zv]*self.errdata_lo[xv][yv][zv]
                 i=0
                 binV = self.zBinsWidth[zk]*self.xBinsWidth[xk]*self.yBinsWidth[yk]     
                 for p in pdfs:
                    if "pdfdata" in p.GetName():
                            lv[i][zv] += p.weight(self.argset)
                    else:
                            lv[i][zv] += p.getVal(self.argset)*binV
                    i+=1
    for i in range(0,len(pdfs)):
        for zk,zv in self.zBins_redux.iteritems():
            if "pdfdata" in pdfs[i].GetName():
                h[i].Fill(zv,lv[i][zv])
            else:
                h[i].Fill(zv,lv[i][zv]*norm)
     
    for b,e in enumerate(neventsPerBin):
     dh.SetBinContent(b+1,e)           
     dh.SetBinError(b+1,math.sqrt(errPerBin[b]))
    self.MakePlots(h,dh,'z',self.zBinslowedge)    

 def doXprojection2(self,pdfs,data,norm,hin=0):
    data_ = ROOT.RooDataHist("data_","data_",self.argset,data)
    h=[]
    lv=[]
    proj = ROOT.TH1F("px","px",len(self.xBinslowedge)-1,self.xBinslowedge)
    neventsPerBin = [0 for xv in range(len(self.xBins_redux))]
    errPerBin = [0 for xv in range(len(self.xBins_redux))]
    
    for p in pdfs:
        h.append( ROOT.TH1F("hx_"+p.GetName(),"hx_"+p.GetName(),len(self.xBinslowedge)-1,self.xBinslowedge))
        lv.append({})
    for xk, xv in self.xBins_redux.iteritems():
         self.argset['MJ1'].setVal(xv)
         for i in range(0,len(pdfs)):
            lv[i][xv]=0
         for yk, yv in self.yBins_redux.iteritems():
             self.argset['MJ2'].setVal(yv)
             for zk,zv in self.zBins_redux.iteritems():
                 self.argset['MJJ'].setVal(zv)
                 i=0
                 binV = self.zBinsWidth[zk]*self.xBinsWidth[xk]*self.yBinsWidth[yk]
                 neventsPerBin[xk-1] += self.ndata[xv][yv][zv]
		 errPerBin[xk-1] += self.errdata_lo[xv][yv][zv]*self.errdata_lo[xv][yv][zv]
                 for p in pdfs:
                     if "postfit" in p.GetName():
                         if "data_" in p.GetName():
                            lv[i][xv] += p.weight(self.argset)#p.evaluate()*binV
                         else:
                             lv[i][xv] += p.evaluate()*binV
                     else:
                        lv[i][xv] += p.getVal(self.argset)*binV
                     i+=1
    for i in range(0,len(pdfs)):
        for key, value in lv[i].iteritems():
            if "pdfdata" in pdfs[i].GetName():
                h[i].Fill(key,value)
            else:
                h[i].Fill(key,value*norm)

    for b,e in enumerate(neventsPerBin):
     proj.SetBinContent(b+1,e)           
     proj.SetBinError(b+1,math.sqrt(errPerBin[b]))
    self.MakePlots(h,proj,'x',self.xBinslowedge)  

 def doYprojection2(self,pdfs,data,norm):
    h=[]
    lv=[]
    proj = ROOT.TH1F("py","py",len(self.yBinslowedge)-1,self.yBinslowedge)
    neventsPerBin = [0 for yv in range(len(self.yBins_redux))]
    errPerBin = [0 for yv in range(len(self.yBins_redux))]
    for p in pdfs:
        h.append( ROOT.TH1F("hy_"+p.GetName(),"hy_"+p.GetName(),len(self.yBinslowedge)-1,self.yBinslowedge))
        lv.append({})
    for yk, yv in self.yBins_redux.iteritems():
         self.argset['MJ2'].setVal(yv)
         for i in range(0,len(pdfs)):
            lv[i][yv]=0
         for xk, xv in self.xBins_redux.iteritems():
             self.argset['MJ1'].setVal(xv)
             for zk,zv in self.zBins_redux.iteritems():
                 self.argset['MJJ'].setVal(zv)
                 i=0
                 neventsPerBin[yk-1] += self.ndata[xv][yv][zv]
		 errPerBin[yk-1] += self.errdata_lo[xv][yv][zv]*self.errdata_lo[xv][yv][zv]
                 binV = self.zBinsWidth[zk]*self.xBinsWidth[xk]*self.yBinsWidth[yk]
                 for p in pdfs:
                    if "pdfdata" in p.GetName():
                            lv[i][yv] += p.weight(self.argset)#p.evaluate()*binV
                    else:
                            lv[i][yv] += p.getVal(self.argset)*binV
                    i+=1
    for i in range(0,len(pdfs)):
        for key, value in lv[i].iteritems():
            if "pdfdata" in pdfs[i].GetName():
                h[i].Fill(key,value)
            else:
                h[i].Fill(key,value*norm)

    for b,e in enumerate(neventsPerBin):
     proj.SetBinContent(b+1,e)           
     proj.SetBinError(b+1,math.sqrt(errPerBin[b]))
    self.MakePlots(h,proj,'y',self.yBinslowedge) 
        
 def addPullPlot(self,hdata,hprefit,hpostfit,nBins):
    #print "make pull plots: (data-fit)/sigma_data"
    N = hdata.GetNbinsX()
    gpost = ROOT.TGraph(0)
    gpre  = ROOT.TGraph(0)
    for i in range(1,N+1):
        m = hdata.GetXaxis().GetBinCenter(i)
        if hdata.GetBinContent(i) == 0:
            continue
        ypostfit = (hdata.GetBinContent(i) - hpostfit.GetBinContent(i))/hdata.GetBinError(i)
        yprefit  = (hdata.GetBinContent(i) - hprefit.GetBinContent(i))/hdata.GetBinError(i)
        if abs(ypostfit)> 4.: 
                
                print "bin",i,"x",m,"data",hdata.GetBinContent(i),"post fit",hpostfit.GetBinContent(i),"prefit",hprefit.GetBinContent(i),"err data",hdata.GetBinError(i),"pull postfit",ypostfit,"pull prefit",yprefit
                print "bin %i x %i data %i post-fit %.2f pre-fit %.2f err data %.2f pull %.2f"%(i,m,hdata.GetBinContent(i),hpostfit.GetBinContent(i),hprefit.GetBinContent(i),hdata.GetBinError(i),ypostfit)
        # print "bin",i,"x",m,"data",hdata.GetBinContent(i),"post fit",hpostfit.GetBinContent(i),"prefit",hprefit.GetBinContent(i),"err data",hdata.GetBinError(i),"pull postfit",ypostfit,"pull prefit",yprefit
        # print "bin %i x %i data %i post-fit %.2f pre-fit %.2f err data %.2f pull %.2f"%(i,m,hdata.GetBinContent(i),hpostfit.GetBinContent(i),hprefit.GetBinContent(i),hdata.GetBinError(i),ypostfit)
        
        gpost.SetPoint(i-1,m,ypostfit)
        gpre.SetPoint(i-1,m,yprefit)
    gpost.SetLineColor(self.colors[1])
    gpre.SetLineColor(self.colors[0])
    gpost.SetMarkerColor(self.colors[1])
    gpre.SetMarkerColor(self.colors[0])
    gpost.SetFillColor(ROOT.kBlue)
    gpost.SetMarkerSize(1)
    gpre.SetMarkerSize(1)
    gpre.SetMarkerStyle(4)
    gpost.SetMarkerStyle(3)
    
    #gt = ROOT.TH1F("gt","gt",hdata.GetNbinsX(),hdata.GetXaxis().GetXmin(),hdata.GetXaxis().GetXmax())
    gt = ROOT.TH1F("gt","gt",len(nBins)-1,nBins)
    gt.SetTitle("")
    gt.SetMinimum(-4.999);
    gt.SetMaximum(4.999);
    gt.SetDirectory(0);
    gt.SetStats(0);
    gt.SetLineStyle(0);
    gt.SetMarkerStyle(20);
    gt.GetXaxis().SetTitle(hprefit.GetXaxis().GetTitle());
    gt.GetXaxis().SetLabelFont(42);
    gt.GetXaxis().SetLabelOffset(0.02);
    gt.GetXaxis().SetLabelSize(0.15);
    gt.GetXaxis().SetTitleSize(0.15);
    gt.GetXaxis().SetTitleOffset(1);
    gt.GetXaxis().SetTitleFont(42);
    gt.GetYaxis().SetTitle("#frac{data-fit}{#sigma}");
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
    gpost.SetHistogram(gt);       
    return [gpre,gpost] 
 
 def addRatioPlot(self,hdata,hprefit,hpostfit,nBins):
    #print "make pull plots: (data-fit)/sigma_data"
    N = hdata.GetNbinsX()
    gpost = ROOT.TGraph(0)
    gpre  = ROOT.TGraph(0)
    for i in range(1,N+1):
        m = hdata.GetXaxis().GetBinCenter(i)
        if hdata.GetBinContent(i) == 0:
            continue
        ypostfit = (hdata.GetBinContent(i) / hpostfit.GetBinContent(i))
        yprefit  = (hdata.GetBinContent(i) / hprefit.GetBinContent(i))
        gpost.SetPoint(i-1,m,ypostfit)
        gpre.SetPoint(i-1,m,yprefit)
    gpost.SetLineColor(self.colors[1])
    gpre.SetLineColor(self.colors[0])
    gpost.SetMarkerColor(self.colors[1])
    gpre.SetMarkerColor(self.colors[0])
    gpost.SetFillColor(ROOT.kBlue)
    gpost.SetMarkerSize(1)
    gpre.SetMarkerSize(1)
    gpre.SetMarkerStyle(4)
    gpost.SetMarkerStyle(20)
    
    #gt = ROOT.TH1F("gt","gt",hdata.GetNbinsX(),hdata.GetXaxis().GetXmin(),hdata.GetXaxis().GetXmax())
    gt = ROOT.TH1F("gt","gt",len(nBins)-1,nBins)
    gt.SetTitle("")
    gt.SetMinimum(0.5);
    gt.SetMaximum(1.5);
    gt.SetDirectory(0);
    gt.SetStats(0);
    gt.SetLineStyle(0);
    gt.SetMarkerStyle(20);
    gt.GetXaxis().SetTitle(hprefit.GetXaxis().GetTitle());
    gt.GetXaxis().SetLabelFont(42);
    gt.GetXaxis().SetLabelOffset(0.02);
    gt.GetXaxis().SetLabelSize(0.15);
    gt.GetXaxis().SetTitleSize(0.15);
    gt.GetXaxis().SetTitleOffset(1);
    gt.GetXaxis().SetTitleFont(42);
    gt.GetYaxis().SetTitle("#frac{Data}{Fit}");
    gt.GetYaxis().CenterTitle(True);
    gt.GetYaxis().SetNdivisions(205);
    gt.GetYaxis().SetLabelFont(42);
    gt.GetYaxis().SetLabelOffset(0.007);
    gt.GetYaxis().SetLabelSize(0.15);
    gt.GetYaxis().SetTitleSize(0.15);
    gt.GetYaxis().SetTitleOffset(0.4);
    gt.GetYaxis().SetTitleFont(42);
    gt.GetXaxis().SetNdivisions(505)
    gpost.SetHistogram(gt);     
    return [gpost] 

 def MakePlots(self,histos,hdata,axis,nBins):
   
    extra1 = ''
    extra2 = ''
    htitle = ''
    xtitle = ''
    ymin = 0
    ymax = 0
    xrange = self.xrange
    yrange = self.yrange
    zrange = self.zrange
    if self.xrange == '0,-1': xrange = '55,215'
    if self.yrange == '0,-1': yrange = '55,215'
    if self.zrange == '0,-1': zrange = '1126,5500'
    if axis=='z':
     htitle = "Z-Proj. x : "+self.xrange+" y : "+self.yrange
     xtitle = "m_{jj} [GeV]"
     ymin = 0.002
     ymax = hdata.GetMaximum()*10
     extra1 = xrange.split(',')[0]+' < m_{jet1} < '+ xrange.split(',')[1]+' GeV'
     extra2 = yrange.split(',')[0]+' < m_{jet2} < '+ yrange.split(',')[1]+' GeV'
    elif axis=='x':
     htitle = "X-Proj. y : "+self.yrange+" z : "+self.zrange
     xtitle = "m_{jet1} [GeV]"
     ymin = 0.0
     ymax = hdata.GetMaximum()*1.4
     extra1 = yrange.split(',')[0]+' < m_{jet2} < '+ yrange.split(',')[1]+' GeV'
     extra2 = zrange.split(',')[0]+' < m_{jj} < '+ zrange.split(',')[1]+' GeV'
    elif axis=='y':
     htitle = "Y-Proj. x : "+self.xrange+" z : "+self.zrange
     xtitle = "m_{jet2} [GeV]"
     ymin = 0.0
     ymax = hdata.GetMaximum()*1.4
     extra1 = xrange.split(',')[0]+' < m_{jet1} < '+ xrange.split(',')[1]+' GeV'
     extra2 = zrange.split(',')[0]+' < m_{jj} < '+ zrange.split(',')[1]+' GeV'
                   
    leg = ROOT.TLegend(0.88,0.65,0.7,0.88)
    c = ROOT.TCanvas("c","c")
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    if axis == 'z': pad1.SetLogy()
    pad1.SetBottomMargin(0.01)    
    pad1.Draw()
    pad1.cd()  
    histos[0].SetMinimum(ymin)
    histos[0].SetMaximum(ymax) 
    histos[0].SetLineColor(self.colors[0])
    histos[0].SetLineStyle(2)
    histos[0].SetLineWidth(2)
    histos[0].SetTitle(htitle)
    histos[0].GetXaxis().SetTitle(xtitle)
    histos[0].GetYaxis().SetTitleOffset(1.3)
    histos[0].GetYaxis().SetTitle("events")
    histos[0].GetYaxis().SetTitleOffset(1.3)
    histos[0].GetYaxis().SetTitle("events")
    histos[0].GetYaxis().SetTitleSize(0.06)
    histos[0].GetYaxis().SetLabelSize(0.06)
    histos[0].GetYaxis().SetNdivisions(5)
    histos[0].Draw("hist")
    leg.AddEntry(histos[0],"Pre fit pdf","l")
    
    histos[1].SetLineColor(self.colors[1])
    histos[1].SetLineWidth(2)
    histos[1].Draw('HISTsame')
    leg.AddEntry(histos[1],"Post fit pdf","l")
    
    for i in range(2,len(histos)):
        histos[i].SetLineColor(self.colors[i])
        histos[i].Draw("histsame")
        name = histos[i].GetName().split("_")
        leg.AddEntry(histos[i],name[2],"l")

    hdata.SetMarkerStyle(20)
    hdata.SetMarkerColor(ROOT.kBlack)
    hdata.SetLineColor(ROOT.kBlack)
    hdata.SetMarkerSize(0.7)
    hdata.Draw("samePE")
    leg.AddEntry(hdata,"data","lp")
        
    leg.SetLineColor(0)
    leg.Draw("same")

    pt2 = ROOT.TPaveText(0.18,0.80,0.53,0.93,"NDC")
    pt2.SetTextFont(62)
    pt2.SetTextSize(0.04)
    pt2.SetTextAlign(12)
    pt2.SetFillColor(0)
    pt2.SetBorderSize(0)
    pt2.SetFillStyle(0)
    pt2.AddText(extra1)
    pt2.AddText(extra2)
    pt2.Draw()
    
    c.cd()
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
    pad2.SetTopMargin(0.1)
    pad2.SetBottomMargin(0.4)
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    graphs = self.addRatioPlot(hdata,histos[0],histos[1],nBins)
    #graphs[0].Draw("AP")
    graphs[0].Draw("AP")
    c.SaveAs(self.output+"PostFit_"+htitle.replace(' ','_')+"_"+self.label+".png")
    c.SaveAs(self.output+"PostFit_"+htitle.replace(' ','_')+"_"+self.label+".root")
    c.SaveAs(self.output+"PostFit_"+htitle.replace(' ','_')+"_"+self.label+".pdf")
    
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
        chi2+= 2*( pr[i] - dr[i] + dr[i]* ROOT.TMath.Log(dr[i]/pr[i]))

    return [chi2,ndof]

 def getChi2proj(self,histo_pdf,histo_data):
    pr=[]
    dr=[]
    for b in range(1,histo_pdf.GetNbinsX()+1):
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
        chi2+= 2*( pr[i] - dr[i] + dr[i]* ROOT.TMath.Log(dr[i]/pr[i]))

    return [chi2,ndof]    
