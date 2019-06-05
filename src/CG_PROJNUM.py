# AUTOSCRIPT NAME: CG_PROJNUM
# CREATEDDATE: 2014-03-04 00:24:27
# CREATEDBY: UVX3
# CHANGEDATE: 2018-05-28 02:57:22
# CHANGEBY: U1MZ
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from psdi.server import MXServer
maximo = MXServer.getMXServer()
MboConstants.NOACCESSCHECK

def setError(g, k, p):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = k
    params = p
	
	
userInfo = mbo.getUserInfo()
personid=mbo.getUserInfo().getPersonId()
groupuserSet=maximo.getMboSet("GROUPUSER",userInfo)
groupuserSet.setWhere("GROUPNAME in ('TRNADMIN') and userid='"+personid+"'");


upperproj = mbo.getString("CG_PROJNO")
mWorktype = mbo.getString("CG_WORKTYPE")
mSubWorktype = mbo.getString("CG_SUBWORKTYPE")
noerrgen = True
#14TMAXIM

if (mbo.isModified("CG_PROJNO") and mbo.getString("CG_PROJNO") =='' and interactive and (app in ["WOT_TRN"] or mbo.getThisMboSet().getParentApp() in ["LOCATS_TRN"]) and mbo.getString("SITEID") =='TRN'):
    mbo.setValue("CG_PROJNO",'', MboConstants.NOACCESSCHECK)

elif mbo.isModified("CG_PROJNO") and mbo.getString("CG_PROJNO") !='' and len(upperproj) < 8 and interactive and (app in ["WOT_TRN"] or mbo.getThisMboSet().getParentApp() in ["LOCATS_TRN"]) and mbo.getString("SITEID") =='TRN' :
   setError("cg_wottrn", "ProjCodeLength", None)
   noerrgen = False
elif mWorktype.upper() in ["CAPITAL"] and len(upperproj) > 2 and upperproj[2].upper() <> 'T' and mSubWorktype =='' and noerrgen and interactive and (app in ["WOT_TRN"] or mbo.getThisMboSet().getParentApp() in ["LOCATS_TRN"]) and mbo.getString("SITEID") =='TRN': 
   setError("cg_wottrn", "needsTforCapital", None)
   noerrgen = False

if (mbo.isModified("CG_PROJNO") and mbo.getString("CG_PROJNO") =='' and interactive and (app in ["WOT_TRN"] or mbo.getThisMboSet().getParentApp() in ["LOCATS_TRN"]) and mbo.getString("SITEID") =='TRN'):
    mbo.setValue("CG_PROJNO",'', MboConstants.NOACCESSCHECK)

elif mbo.isModified("CG_PROJNO") and mbo.getString("CG_PROJNO") !='' and len(upperproj) < 8 and interactive and (app in ["WOT_TRN"] or mbo.getThisMboSet().getParentApp() in ["LOCATS_TRN"]) and mbo.getString("SITEID") =='TRN':
   setError("cg_wottrn", "ProjCodeLength", None)
   noerrgen = False
elif mWorktype.upper() in ["CORRECTIVE"] and len(upperproj) > 2 and upperproj[2].upper() <> 'P' and mSubWorktype =='' and noerrgen and interactive and (app in ["WOT_TRN"] or mbo.getThisMboSet().getParentApp() in ["LOCATS_TRN"]) and mbo.getString("SITEID") =='TRN': 
   setError("cg_wottrn", "needsPforCapital", None)
   noerrgen = False   
   
if (not groupuserSet.isEmpty()) and mSubWorktype =='GP' and mWorktype.upper() in ["CAPITAL"]  and  noerrgen:
    noerrgen = True

if noerrgen:
    mbo.setValue("CG_PROJNO", upperproj.upper(), MboConstants.NOACCESSCHECK)