# AUTOSCRIPT NAME: EX2VALIDATEGLONWO
# CREATEDDATE: 2014-08-25 10:30:04
# CREATEDBY: UVX3
# CHANGEDATE: 2016-11-15 03:56:13
# CHANGEBY: U171
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants


def setError(g, e):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = e


#appli = mbo.getOwner().getThisMboSet().getApp()
appli = mbo.getThisMboSet().getParentApp()
print '<<<<<<<<<<<<<<>>>>>>>>>>>>'

print appli
print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'


if  appli =='PLUSDWOTRK':
 if appli !='WOT_TRN':
   mGLdebit = mbo.getString("GLACCOUNT")
   if '?' in mGLdebit:
      setError("WOGLACCOUNT", "EnterCompleteGLAcount")
  
print "VALIDATEGL: "+launchPoint+": End"

#INC000001353063 - INV - Work Orders (Populate EX2DERNUM from WO header in case it is not auto populated in Work Order Tracking (T&D) app)
if  appli =='PLUSDWOTRK' and onadd:
 wombo=mbo.getOwner()
 if wombo and mbo.isNull("EX2DERNUM"): 
  mbo.setValue("EX2DERNUM", wombo.getString("EX2DERNUM"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)  
# End INC000001353063 - INV - Work Orders