# AUTOSCRIPT NAME: EX2INVUSELNSAVE
# CREATEDDATE: 2014-04-26 10:34:10
# CREATEDBY: UFQJ
# CHANGEDATE: 2017-01-23 08:21:48
# CHANGEBY: UZHC
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

def setError():
    global errorkey, errorgroup
    errorkey="ex2noconsignmentreturns"
    errorgroup="inventoryusage"		

def setError(g, k, p):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = k
    params = p
	
if mbo.getBoolean("RETURNAGAINSTISSUE"):		
  inventoryset = mbo.getMboSet("INVENTORY")
  inventorycount = inventoryset.count()
  if inventorycount > 0 :
    invmbo = inventoryset.getMbo(0)
    if invmbo.getBoolean("CONSIGNMENT") and mbo.getString("usetype") in ["RETURN"]:
	  setError()
unitcost=mbo.getString("UNITCOST")
if '-' in unitcost:
 setError("inventory", "greaterThanZeroUnitCost",None)