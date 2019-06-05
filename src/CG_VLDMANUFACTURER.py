# AUTOSCRIPT NAME: CG_VLDMANUFACTURER
# CREATEDDATE: 2016-09-07 04:20:01
# CREATEDBY: U03V
# CHANGEDATE: 2017-03-14 06:14:19
# CHANGEBY: U144
# SCRIPTLANGUAGE: jython
# STATUS: Draft

def setError(g, e):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = e		
	
if app=='ASSETS_MS':	 
 compSet = mbo.getMboSet("CG_VLDMANUFACTURER")  
 if compSet.count() == 0 : 
 	setError("company", "companyDisabled")