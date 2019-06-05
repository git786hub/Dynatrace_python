# AUTOSCRIPT NAME: EX2INVLOWCOST
# CREATEDDATE: 2016-11-28 02:54:05
# CREATEDBY: U03V
# CHANGEDATE: 2018-01-10 23:36:30
# CHANGEBY: UZHC
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from psdi.server import MXServer


if (launchPoint in ['EX2WOITEMLOWCOST', 'EX2WOGLTASK'] and mbo.getThisMboSet().getParentApp()== 'PLUSDWOTRK') or launchPoint in ['EX2ISSUEGLLOW', 'EX2INVITEMLOW', 'EX2INVGLLOW']:

    maximo = MXServer.getMXServer()
    userInfo = mbo.getUserInfo()
    personid=mbo.getUserInfo().getPersonId()

    def setError(g, e, p):
        global errorgroup, errorkey, params
        errorgroup = g
        errorkey = e
        params= p

    itemnum= mbo.getString("ITEMNUM")

    if launchPoint == 'EX2WOITEMLOWCOST':
	glacct = mbo.getOwner().getString("GLACCOUNT")

    if launchPoint == 'EX2WOGLTASK' :
	    taskid= mbo.getString("TASKID")
	    glacct =""
            isInvalidTaskID= "true"
	    if taskid != "":
                if mbo.getOwner().getName() == 'WORKORDER':
                    woactSet=mbo.getOwner().getMboSet("WOACTIVITY")
                else:
                    woactSet=mbo.getOwner().getMboSet("EX2CURPARENTWO")
                woact=woactSet.moveFirst()
                while woact != None:
                    if woact.getString("TASKID") == taskid:
                        glacct = woact.getString("GLACCOUNT")
                        isInvalidTaskID= "false"
                        break
                    woact=woactSet.moveNext()
                if isInvalidTaskID =="true" :
                    setError("workorder","NotValidTaskID", ["Task", taskid])

    if launchPoint in ['EX2ISSUEGLLOW', 'EX2INVITEMLOW', 'EX2INVGLLOW']:
        glacct = mbo.getString("GLDEBITACCT")

#Temporary solution of INC000001506101 PMR#49706,004,000 - INV - Reservation on PENDOBS
    if (launchPoint in ['EX2WOITEMLOWCOST'] and mbo.getThisMboSet().getParentApp()== 'PLUSDWOTRK') and itemnum != "":
        itemSet=maximo.getMboSet("ITEM",userInfo)
        itemSet.setWhere("ITEMNUM='"+itemnum+"' and STATUS='PENDOBS'");
        if not itemSet.isEmpty():
          setError("item","ActionNotAllowedStatus", [itemnum , "Item"])
        
    if itemnum != "" and glacct != "" :
        itemSet=maximo.getMboSet("ITEM",userInfo)
        itemSet.setWhere("ITEMNUM='"+itemnum+"' and EX2LOWCOST='1'");

        if (itemSet.isEmpty() and 'DDLOWCST' in glacct):
            setError("EX2WO","LowCost item", [itemnum, glacct ])