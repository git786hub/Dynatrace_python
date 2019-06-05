# AUTOSCRIPT NAME: EX2_CONTR_ONADD
# CREATEDDATE: 2015-05-03 05:28:50
# CREATEDBY: UVX3
# CHANGEDATE: 2015-05-22 01:18:59
# CHANGEBY: UQRM
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.server import MXServer
from java.lang import String
from java.lang import Long

contractMboSet= mbo.getMboSet("EX2_PURCHVIEW") #Relationship to fetch the contractid for the previously revised latest Approved Contract
# If new contract it would fetch zero
count2 = contractMboSet.count()
if (count2 > 0) :
        contractid = Long.toString(LCONTRACTID) 
        mbosetESCTRACK = MXServer.getMXServer().getMboSet("ESCREPEATTRACK", mbo.getUserInfo())
        notifycount1 = mbosetESCTRACK.count()
        mbosetESCTRACK.setWhere(" OWNERID = '"+contractid+ "'AND OBJECTNAME ='PURCHVIEW' and ESCALATION ='EX2PURCTREXP' ");
        mbosetESCTRACK.reset()
        notifycount = mbosetESCTRACK.count() #Saves the number of notifications sent for this contractid
        if (notifycount == 3):
           mbo.setValue("EX2EMAILFLAG", '3' ,MboConstants.NOACCESSCHECK)
           mbo.setValue("EX2ENDDATE", ENDDATE ,MboConstants.NOACCESSCHECK)
        elif (notifycount == 2) :
            mbo.setValue("EX2EMAILFLAG", '2' ,MboConstants.NOACCESSCHECK)
            mbo.setValue("EX2ENDDATE", ENDDATE ,MboConstants.NOACCESSCHECK)
        elif (notifycount == 1) :
            mbo.setValue("EX2EMAILFLAG", '1' ,MboConstants.NOACCESSCHECK)
            mbo.setValue("EX2ENDDATE", ENDDATE ,MboConstants.NOACCESSCHECK)





status= mbo.getString("status")
EX2BUAPPREXCIND=mbo.getString("EX2BUAPPREXCIND")
if (status=='PNDREV') :
   mbo.setValue("EX2BUAPPREXCIND", '0' ,MboConstants.NOACCESSCHECK)