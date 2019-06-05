# AUTOSCRIPT NAME: EX2PMWKRLOG
# CREATEDDATE: 2018-10-11 07:35:34
# CREATEDBY: U4B0
# CHANGEDATE: 2018-11-29 23:36:33
# CHANGEBY: U4B0
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from java.util import Date
wologmboset = mbo.getMboSet ("MODIFYWORKLOG")

wologcount = wologmboset.count()
if wologmboset.count() == 0 :
    wrklogmbo = wologmboset.add()
    #wrklogmbo.setValue("RECORDKEY", mbo.getString("WONUM"))
    #wrklogmbo.setValue("CLASS", 'WORKORDER')
    #wrklogmbo.setValue("SITEID", mbo.getString("SITEID"))
    #wrklogmbo.setValue("CLASS", mbo.getString("CLASS"))
    wrklogmbo.setValue("LOGTYPE", "FIELDNOTE")
    #wrklogmbo.setValue("CREATEBY", "PMGENDIS1")
    #wrklogmbo.setValue("CREATEDATE", SYSDATE)	
    #Please replace battery and do not incomplete
    wrklogmbo.setValue("DESCRIPTION", "Please replace battery and do not incomplete order")
    wrklogmbo.setValue("description_longdescription", "Please replace battery and do not incomplete order")
wologmboset.save()