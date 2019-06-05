# AUTOSCRIPT NAME: CG_ASSETMFG
# CREATEDDATE: 2012-06-24 19:55:19
# CREATEDBY: UHD0
# CHANGEDATE: 2017-03-01 05:14:58
# CHANGEBY: U144
# SCRIPTLANGUAGE: jython
# STATUS: Draft

def setError(g, e):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = e		

if not mbo.getBoolean("CG_NOSERIALNUM") :
    outmfg = inmfg
else :
    outmfg = None

if app=='ASSETS_TRN':	
 compSet = mbo.getMboSet("CG_VLDMANUFACTURERF")  
 if compSet.count() == 0 : 
 	setError("company", "companyDisabled")