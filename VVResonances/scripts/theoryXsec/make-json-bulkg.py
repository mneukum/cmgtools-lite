import json, sys
from array import array
import ROOT
from ROOT import *

fin = ROOT.TFile.Open('BulkGWW.root','READ')
graph = fin.Get('gtheory')

xsec = {}

for i in range(graph.GetN()):
 x = ROOT.Double(0.)
 y = ROOT.Double(0.)
 graph.GetPoint(i,x,y)
 xsec[str(int(x*1000))] = {}

for i in range(graph.GetN()):
 x = ROOT.Double(0.)
 y = ROOT.Double(0.)
 graph.GetPoint(i,x,y)
 xsec[str(int(x*1000))]["BRWW"] = y
 xsec[str(int(x*1000))]["sigma"] = 1.0

x=5.2
xsec[str(int(x*1000))] = {}
xsec[str(int(x*1000))]["BRWW"] = graph.Eval(x)
xsec[str(int(x*1000))]["sigma"] = 1.0


fin.Close()

fin = ROOT.TFile.Open('BulkGZZ.root','READ')
graph = fin.Get('gtheory')

for i in range(graph.GetN()):
 x = ROOT.Double(0.)
 y = ROOT.Double(0.)
 graph.GetPoint(i,x,y)
 xsec[str(int(x*1000))]["BRZZ"] = y

x=5.2
xsec[str(int(x*1000))]["BRZZ"] = graph.Eval(x)
xsec[str(int(x*1000))]["sigma"] = 1.0

fin.Close()

f=open("BulkG.json","w")
json.dump(xsec,f)
f.close()
