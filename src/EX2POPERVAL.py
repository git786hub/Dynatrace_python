# AUTOSCRIPT NAME: EX2POPERVAL
# CREATEDDATE: 2016-12-19 05:37:59
# CREATEDBY: U171
# CHANGEDATE: 2016-12-21 03:40:23
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from psdi.server import MXServer

def setError(g, k, p):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = k
    params = p

postatus = mbo.getString("STATUS")

#1
ex2invapprmbo = mbo.getString("EX2INVAPPR")
ex2invapprMboSet = None
ex2invapprMboSet = mbo.getMboSet("EX2INVAPPR")

if launchPoint =='EX2INVAPPR':
   if ex2invapprmbo <> "" and ex2invapprMboSet.count() < 1 :
      p = ["Invoice Approver"]      
      setError("ex2_person", "DoesNotExist", p)
	  
if ex2invapprmbo <> "" and postatus == 'WAPPR' and varEX2INVAPPR == 'INACTIVE' : 
   p = ["Invoice Approver"]
   setError("ex2_inactper", "inactPer", p)
   
#2   
EX2REVOWNERmbo= mbo.getString("EX2REVOWNER")
ex2reownerMboSet = None
ex2reownerMboSet = mbo.getMboSet("EX2REVOWNER") 

if launchPoint =='EX2REVOWNER':
   if EX2REVOWNERmbo <> "" and ex2reownerMboSet.count() < 1 :
      p = ["Revision Owner"]
      setError("ex2_person", "DoesNotExist",p)
	  
if EX2REVOWNERmbo <> "" and postatus == 'WAPPR' and varEX2REVOWNER== 'INACTIVE' : 
   p = ["Revision Owner"]
   setError("ex2_inactper", "inactPer", p)
   
#3  
EX2REVBUYERmbo= mbo.getString("EX2REVBUYER")
ex2revbuyerMboSet = None
ex2revbuyerMboSet = mbo.getMboSet("EX2REVBUYER")

if launchPoint =='EX2REVBUYER':
   if EX2REVBUYERmbo <> "" and ex2revbuyerMboSet.count() < 1 :
      p = ["Processing Buyer"]      
      setError("ex2_person", "DoesNotExist", p)
	  
if EX2REVBUYERmbo <> "" and postatus == 'WAPPR' and varEX2REVBUYER== 'INACTIVE' : 
   p = ["Processing Buyer"]
   setError("ex2_inactper", "inactPer", p)
   
#4 
EX2REQUESTEDBYmbo= mbo.getString("EX2REQUESTEDBY")
ex2reqbyMboSet = None
ex2reqbyMboSet = mbo.getMboSet("EX2REQUESTEDBY")

if launchPoint =='EX2REQBY':
   if EX2REQUESTEDBYmbo <> "" and ex2reqbyMboSet.count() < 1 :
      p = ["Requested by"]      
      setError("ex2_person", "DoesNotExist", p)

if EX2REQUESTEDBYmbo<> "" and postatus == 'WAPPR' and varREQUESTEDBY== 'INACTIVE' : 
    p = ["Requested by"]
    setError("ex2_inactper", "inactPer", p)

#5
EX2DESAPPRmbo= mbo.getString("EX2DESAPPR")
ex2desapprMboSet = None
ex2desapprMboSet = mbo.getMboSet("EX2DESAPPR")

if launchPoint =='EX2DESAPPR':
   if EX2DESAPPRmbo <> "" and ex2desapprMboSet.count() < 1 :
      p = ["Designated Approver"]      
      setError("ex2_person", "DoesNotExist", p)

if EX2DESAPPRmbo <> "" and postatus == 'WAPPR' and varEX2DESAPPR== 'INACTIVE' : 
   p = ["Designated Approver"]
   setError("ex2_inactper", "inactPer", p)
   
#6
EX2BUDOAAPPRmbo= mbo.getString("EX2BUDOAAPPR")
ex2budoapprMboSet = None
ex2budoapprMboSet = mbo.getMboSet("EX2BUDOAAPPR")

if launchPoint =='EX2BUDOAAPPR':
   if EX2BUDOAAPPRmbo <> "" and ex2budoapprMboSet.count() < 1 :
      p = ["BU DOA Approver"]      
      setError("ex2_person", "DoesNotExist", p)

if EX2BUDOAAPPRmbo <> "" and postatus == 'WAPPR' and varEX2BUDOAAPPR== 'INACTIVE' : 
   p = ["BU DOA Approver"]
   setError("ex2_inactper", "inactPer", p)

#7
PURCHASEAGENTmbo= mbo.getString("PURCHASEAGENT")
puragntMboSet = None
puragntMboSet = mbo.getMboSet("EX2PURCHASEAGENT")

if launchPoint =='PURCHASEAGENT':
   if PURCHASEAGENTmbo <> "" and puragntMboSet.count() < 1 :
      p = ["Buyer"]
      setError("ex2_person", "DoesNotExist", p)

if PURCHASEAGENTmbo <> "" and postatus == 'WAPPR' and varPURCHASEAGENT== 'INACTIVE' : 
   p = ["Buyer"]
   setError("ex2_inactper", "inactPer", p)

#8
SHIPTOATTNmbo= mbo.getString("SHIPTOATTN")
shiptoattnMboSet = None
shiptoattnMboSet = mbo.getMboSet("EX2SHIPTOATTN")

if launchPoint =='SHIPTOATTN':
   if SHIPTOATTNmbo <> "" and shiptoattnMboSet.count() < 1 :
      p = ["Attention"]
      setError("ex2_person", "DoesNotExist", p)

if SHIPTOATTNmbo <> "" and postatus == 'WAPPR' and varSHIPTOATTN== 'INACTIVE' : 
   p = ["Attention"]
   setError("ex2_inactper", "inactPer", p)
   
#9
BILLTOATTNmbo= mbo.getString("BILLTOATTN")
billtoattnMboSet = None
billtoattnMboSet = mbo.getMboSet("EX2BILLTOATTN")

if launchPoint =='BILLTOATTN':
   if BILLTOATTNmbo <> "" and billtoattnMboSet.count() < 1 :
      p = ["Attention"]
      setError("ex2_person", "DoesNotExist", p)

if BILLTOATTNmbo <> "" and postatus == 'WAPPR' and varBILLTOATTN== 'INACTIVE' : 
   p = ["Attention"]
   setError("ex2_inactper", "inactPer", p)