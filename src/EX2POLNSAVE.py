# AUTOSCRIPT NAME: EX2POLNSAVE
# CREATEDDATE: 2018-03-23 07:10:41
# CREATEDBY: U3LO
# CHANGEDATE: 2018-05-06 00:57:02
# CHANGEBY: U3LO
# SCRIPTLANGUAGE: python
# STATUS: Draft

from psdi.mbo import MboConstants 
from psdi.app.po import PORemote
from psdi.mbo import MboRemote

def setError():
    global errorkey, errorgroup
    errorkey="ex2notaxorship"
    errorgroup="invoice"

pombo = mbo.getOwner()

if not (pombo and isinstance(pombo ,PORemote)) :
    print ("############ no owner")
    poset = mbo.getMboSet("PO")
    if poset .count() > 0 :
        pombo = poset.getMbo(0)

# either the tax code or the ship-to address is required.

if (isinstance(pombo ,PORemote)) :
   if not pombo.getString("sourcesysid") in  ["BROUSSARD", "EEPM", "ACIS", "W2MS"] :
	if mbo.isNull("ex2taxcode") and mbo.isNull("shipto") :
		print ("############### Error:Tax Code or ShipTo is required")
		setError()