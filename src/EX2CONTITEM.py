# AUTOSCRIPT NAME: EX2CONTITEM
# CREATEDDATE: 2013-10-08 14:15:30
# CREATEDBY: UFQJ
# CHANGEDATE: 2015-07-06 14:01:16
# CHANGEBY: UT76
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

def setError():
    global errorkey,errorgroup,params
    errorkey='ex2_dupitem'
    errorgroup='contract'

# Verify same Item not in multiple lines
# INC000001145129 Included condition to check duplicate only for ITEM LineType
if mbo.getString("LINETYPE")=="ITEM":
  ctlmboset = mbo.getThisMboSet()
  num = ctlmboset.count()
  for i in range(num):
      ctlmbo = ctlmboset.getMbo(i)
      if ctlmbo.getInt("CONTRACTLINENUM") <> mbo.getInt("CONTRACTLINENUM") and ctlmbo.getString("ITEMNUM") ==  mbo.getString("ITEMNUM") and ctlmbo.getString("LINETYPE")=="ITEM":
          setError()