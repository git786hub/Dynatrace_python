# AUTOSCRIPT NAME: EX2PROTECTINVCSINWF
# CREATEDDATE: 2013-12-05 09:50:38
# CREATEDBY: UFQJ
# CHANGEDATE: 2015-10-20 04:55:29
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

#dupinvmboset = mbo.getMboSet("ex2activewfasgn")   # is there an active assignment?
#if  dupinvmboset.count() > 0 :

groupuserSet=mbo.getMboSet("EX2GROUPUSER")

if app == "INVOICE" and (mbo.getString("status") in ["BUPEND", 'APPR',"CKVD", "CSTP", "PD", "PSREVERSE", "UPD"]) or (groupuserSet.isEmpty() and mbo.getString("status") == "REVIEW") :
    #mbo.setFlag(MboConstants.READONLY, True)        #  set object readonly
    mbo.setFieldFlag("description", MboConstants.READONLY, True)        #  set field readonly - must leave status alone
    mbo.setFieldFlag("ponum", MboConstants.READONLY, True)  
    mbo.setFieldFlag("ex2extremarks", MboConstants.READONLY, True)  
    mbo.setFieldFlag("ex2extremarks_longdescription", MboConstants.READONLY, True)  
    mbo.setFieldFlag("vendorinvoicenum", MboConstants.READONLY, True)   
    mbo.setFieldFlag("enterby", MboConstants.READONLY, True)   
    mbo.setFieldFlag("ex2invappr", MboConstants.READONLY, True)   
    mbo.setFieldFlag("ex2prepaid", MboConstants.READONLY, True)   
    mbo.setFieldFlag("invoicedate", MboConstants.READONLY, True)   
    mbo.setFieldFlag("glpostdate", MboConstants.READONLY, True)   
    mbo.setFieldFlag("contact", MboConstants.READONLY, True)   
    mbo.setFieldFlag("paymentterms", MboConstants.READONLY, True)   
    mbo.setFieldFlag("inclusive1", MboConstants.READONLY, True)  
    mbo.setFieldFlag("ex2psaccrue", MboConstants.READONLY, True)  
    mbo.setFieldFlag("ex2controlamt", MboConstants.READONLY, True)   
    mbo.setFieldFlag("currencycode", MboConstants.READONLY, True)   

if app == "INVOICE" and mbo.getString("sourcesysid") in  ["BROUSSARD", "EEPM", "ACIS", "W2MS"] :
    mbo.setFieldFlag("ex2psaccrue", MboConstants.READONLY, True)