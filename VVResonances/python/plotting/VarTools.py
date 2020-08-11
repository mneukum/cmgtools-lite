import ROOT
import copy
import sys


# function to extract string from function -> in order write a proper json file
def returnString(func,ftype):
    if func.GetName().find("corr")!=-1:
        st = "("+str(func.GetParameter(0))+" + ("+str(func.GetParameter(1))+")*MJ1 + ("+str(func.GetParameter(2))+")*MJ2  + ("+str(func.GetParameter(3))+")*MJ1*MJ2)"
        if func.GetName().find("sigma")!=-1:
            st = "("+str(func.GetParameter(0))+" + ("+str(func.GetParameter(1))+")*MJ1 + ("+str(func.GetParameter(2))+")*MJ2 )"
        return st
    else:
        if ftype.find("pol")!=-1:
            st='(0'
            if func.GetName().find("corr")!=-1: 
                n = 1. #func.Integral(55,215)
                st = "(0"
                for i in range(0,func.GetNpar()):
                    st = st+"+("+str(func.GetParameter(i))+")"+("*(MJ1+MJ2)/2."*i)
                st+=")/"+str(n)
            else:
                for i in range(0,func.GetNpar()):
                    st=st+"+("+str(func.GetParameter(i))+")"+("*MH"*i)
                st+=")"
            return st
        if ftype.find("1/sqrt")!=-1:
            st='(0'
            if func.GetName().find("corr")!=-1:
                n = 1. # func.Integral(55,215)
                st = str(func.GetParameter(0))+"+("+str(func.GetParameter(1))+")*1/sqrt((MJ1+MJ2)/2.)/"+str(n)
            else:
                st = str(func.GetParameter(0))+"+("+str(func.GetParameter(1))+")"+")*1/sqrt(MH)"
                st+=")"
            return st
        if ftype.find("sqrt")!=-1 and ftype.find("1/")==-1:
            n =1.
            st='(0'
            if func.GetName().find("corr")!=-1: st = str(func.GetParameter(0))+"+("+str(func.GetParameter(1))+")"+"*sqrt((MJ1+MJ2)/2.))/"+str(n)
            else:
                st = str(func.GetParameter(0))+"+("+str(func.GetParameter(1))+")"+"*sqrt(MH)"
                st+=")"
            return st    
        if ftype.find("llog")!=-1:
            return str(func.GetParameter(0))+"+"+str(func.GetParameter(1))+"*log(MH)"
        if ftype.find("laur")!=-1:
            st='(0'
            for i in range(0,func.GetNpar()):
                st=st+"+("+str(func.GetParameter(i))+")"+"/MH^"+str(i)
            st+=")"
            return st    
        if ftype.find("spline")!=-1:
            print "write json for spline function"
            print "returns list not string!"
            st=[]
            nnknots = func.GetNp()
            for i in range(0,nnknots):
                x = ROOT.Double(0) 
                y = ROOT.Double(0) 
                func.GetKnot(i,x,y)
                st.append([x,y])
            return st
        else:
            return ""

