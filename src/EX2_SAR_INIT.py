# AUTOSCRIPT NAME: EX2_SAR_INIT
# CREATEDDATE: 2013-10-08 18:17:40
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-06-13 14:01:43
# CHANGEBY: UFQJ
# SCRIPTLANGUAGE: jython
# STATUS: Active

# protect fields in the main tab if contract is approved 
from psdi.mbo import MboConstants 

curstat = mbo.getString("STATUS")
if app in ["SARITEM"]:
  if ( (curstat == "ACTIVE"  or curstat == "PENDING" ) and (mbo.isNull("ex2requesttype") == False) ):
      mbo.setFieldFlag("ex2requesttype", MboConstants.READONLY, True)
  if mbo.getString("EX2REQUESTTYPE") == "CHANGE ITEM" and mbo.getBoolean("EX2NEWSDS")  and mbo.getBoolean("EX2SDS"):
      mbo.setFieldFlag("EX2NEWSDS", MboConstants.READONLY, True)