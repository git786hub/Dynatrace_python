# AUTOSCRIPT NAME: CWOTRN
# CREATEDDATE: 2012-05-12 14:19:36
# CREATEDBY: UHD0
# CHANGEDATE: 2013-04-04 07:12:00
# CHANGEBY: UM7V
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from java.util import Date

jpn = mbo.getString("CG_JPNUM")

if jpn == ""  :
    global errorkey,errorgroup,params
    errorkey='canNotAddforNullRequiredFld'
    errorgroup='assetcatalog'
    params = ['Job Plan Number']
else :
    woSet = mbo.getMboSet("WORKORDER")
    wo = mbo.createWorkorder(woSet,False)
    wo = woSet.getMbo()
    wo.generateAutoKey()
    wo.setValue("STATUS","APPR",MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
    wo.setValue("JPNUM",jpn,MboConstants.NOACCESSCHECK)
    if mbo.getString("STATUS") <> "INPROG" :
        mbo.changeStatus("INPROG",Date(),"",MboConstants.NOACCESSCHECK)
    ownmboset = mbo.getThisMboSet()
    ownmboset.save()
    global errorkey,errorgroup,params
    errorkey='WOCreated'
    errorgroup='ticket'
    params = [wo.getString("WONUM")]