# AUTOSCRIPT NAME: CG_MPMNUMCHK
# CREATEDDATE: 2013-04-30 04:32:24
# CREATEDBY: UHD0
# CHANGEDATE: 2013-04-30 06:14:51
# CHANGEBY: UFCV
# SCRIPTLANGUAGE: jython
# STATUS: Draft

def setError(g, k, p):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = k
    params = p
		
siteid = mbo.getUserInfo().getInsertSite()
	
if mpmnum is not None and mpmnum != "" and siteid in ["MS","DIS"]:	
	if mpmnum[:2].upper() in ["CM","MP"]:
		setError("mpm","cg_msdis_masterpmnum",None)
		
if mpmnum is not None and mpmnum != "" and siteid == "TRN":
	if mpmnum[:2].upper() not in ["CM","MP"]:
		setError("mpm","cg_trn_masterpmnum",None)