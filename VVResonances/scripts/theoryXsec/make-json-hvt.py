import json, sys
from array import array

def get_theo_map(sqrts,model=""):

   V_mass = array('d',[])

   brs = {}
   index = {}

   mapping = ["M0","M+","BRWW","BRZh","BRWZ","BRWh","CX+(pb)","CX0(pb)","CX-(pb)"]

   for m in xrange(0,len(mapping)):
      if mapping[m] != "M0" and mapping[m] != "M+":
   	 brs[mapping[m]] = array('d',[])
   	 #print mapping[m]

   f = open('xsect_HVT%s_%sTeV.txt'%(model,sqrts),'r')
   for line in f:
      brDict = line.split(",")
      for d in xrange(0,len(brDict)):
   	 if brDict[d].find('\n') != -1:
   	    brDict[d] = brDict[d].split('\n')[0]
   	 for m in xrange(0,len(mapping)):
   	    if brDict[d] == mapping[m]:
   	       index[mapping[m]] = d
   	       print "%s %i" %(mapping[m],d)
	    
   f.close()

   f = open('xsect_HVT%s_%sTeV.txt'%(model,sqrts),'r')
   for line in f:
      if line.find('M0') != -1: continue
      brDict = line.split(",")  	    
      V_mass.append(float(brDict[index['M0']]))
      for m in xrange(0,len(mapping)):
   	 if mapping[m] != "M0" and mapping[m] != "M+":
   	    brs[mapping[m]].append(float(brDict[index[mapping[m]]]))

   f.close()

   return [brs,V_mass]


thMap13 = get_theo_map("13","B")
xsecMap13 = thMap13[0]
mass = thMap13[1]

fdict = {}
for k,m in enumerate(mass):
 fdict[str(int(m))] = {}
 for i,v in xsecMap13.iteritems():
  fdict[str(int(m))][i] = v[k]

f=open("HVTB.json","w")
json.dump(fdict,f)
f.close()

