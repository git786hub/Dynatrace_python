# AUTOSCRIPT NAME: CG_MOVEASSET
# CREATEDDATE: 2017-04-06 05:42:33
# CREATEDBY: U03V
# CHANGEDATE: 2017-04-18 06:36:30
# CHANGEBY: U144
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.app.location import Location
from psdi.app.location import LocationRemote
from psdi.app.location import LocationSetRemote
from psdi.mbo import SqlFormat

def setError():
        global errorkey,errorgroup,params
        errorkey='invalidStatusForThisMove'
        errorgroup='asset'
if interactive :
 prevloc=mbo.getString("LOCATION")
 prevloc1=mbo.getMboValue("LOCATION").getPreviousValue().asString()
 if prevloc!=prevloc1:
  loc=mbo.getMboSet("NEWLOCATION").getMbo(0)
  if ( loc != "" or loc is not None ) and mbo.getString("SITEID") == "MS":
   assetnum=mbo.getString("ASSETNUM")
   sqf = SqlFormat("location=:1 and siteid=:2")
   sqf.setObject(1, "LOCATIONS", "LOCATION", mbo.getMboValue("LOCATION").getPreviousValue().asString())
   sqf.setObject(2, "LOCATIONS", "SITEID", mbo.getString("SITEID"))
   fromLoc=mbo.getMboSet("$newlocation", "LOCATIONS", sqf.format()).getMbo(0)
 
   fromlocation=fromLoc.getString("LOCATION")

   fromlocationtype=fromLoc.getString("TYPE")
   loclocation=loc.getString("LOCATION")

   loclocationtype1=loc.getString("TYPE")
 

   sqlfmt = SqlFormat("siteid=:1 and fromlocationtype=:2 and tolocationtype=:3 and assetstatus=:4")
   sqlfmt.setObject(1, "CG_ASSETMOVERESTRICTION", "SITEID", mbo.getString("SITEID"))
   sqlfmt.setObject(2, "CG_ASSETMOVERESTRICTION", "FROMLOCATIONTYPE", fromLoc.getString("TYPE"))
   sqlfmt.setObject(3, "CG_ASSETMOVERESTRICTION", "TOLOCATIONTYPE", loc.getString("TYPE"))
   sqlfmt.setObject(4, "CG_ASSETMOVERESTRICTION", "ASSETSTATUS", mbo.getString("STATUS"))

 
   mboSetMoveRestriction = mbo.getMboSet("$moverestriction", "CG_ASSETMOVERESTRICTION", sqlfmt.format())
   if mboSetMoveRestriction .count() > 0 :
    setError()