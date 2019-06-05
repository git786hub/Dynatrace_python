# AUTOSCRIPT NAME: EX2POADDUPD
# CREATEDDATE: 2016-09-08 11:29:34
# CREATEDBY: U03V
# CHANGEDATE: 2018-04-19 20:07:04
# CHANGEBY: UT76
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants 
from psdi import server
from psdi.security import UserInfo	
from psdi.server import  MXServer

server = MXServer.getMXServer()
userid = mbo.getUserInfo().getUserName() 

if onadd:
    #INC000001350849
    #OOB Doesn't allow multiple revisions, but issue happnened during MIF JVM Issue, having this rule to explicitly stop that.
    if not interactive and mbo.getString("sourcesysid") in ["PTR","TED"]:
        poMboSet=mbo.getMboSet("$POREVHISTORY","PO", "PONUM = :PONUM AND SITEID = :SITEID AND STATUS = 'PNDREV'")
        pombo = poMboSet.getMbo(0)
        if poMboSet.count()>0:
            global errorkey, errorgroup
            errorkey="revisionAlreadyCreated"
            errorgroup="po"

if onupdate:
    #INC000001010131
    #Stop TED to Change on Approved PO
    if not interactive and mbo.getString("sourcesysid") in ["PTR","TED"] and (mbo.getInternalStatus() not in ["WAPPR","PNDREV","CLOSE"] ) and userid not in ["MAXADMIN"]:
        global errorkey, errorgroup
        errorkey="invalidstatuschange"
        errorgroup="po"