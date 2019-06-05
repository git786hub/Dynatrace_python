# AUTOSCRIPT NAME: CG_UPDROUTESEQ
# CREATEDDATE: 2014-10-12 09:42:19
# CREATEDBY: UVX3
# CHANGEDATE: 2014-10-13 03:17:09
# CHANGEBY: USZN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

#import time
from psdi.mbo import MboConstants
from psdi.mbo import MboConstants
assetnum = mbo.getString("ASSETNUM")
location = mbo.getString("LOCATION")
if (assetnum is not None and assetnum <> '') :
   record = mbo.getMboSet("ROUTE_STOP_ASSET")
   if record.count() > 0:
      recordi = record.getMbo(0)
      recsetAs = mbo.getMboSet("CG_ROUTEMETER")
      if recsetAs.count() > 0 :
         num1 = recsetAs.count()
         for i in range(num1):
            recdi = recsetAs.getMbo(i)
            recdi.setValue("CG_STOPSEQUENCE",recordi.getInt("STOPSEQUENCE"),MboConstants.NOACCESSCHECK)
else :
   if (location is not None and location <> '') :
      recordl = mbo.getMboSet("ROUTE_STOP_LOCATION")
      if recordl.count() > 0:
         recordli = recordl.getMbo(0)
         recsetLoc = mbo.getMboSet("CG_ROUTEMETER")
         if recsetLoc.count() > 0 :
            num1 = recsetLoc.count()
            for i in range(num1):
               recdiL = recsetLoc.getMbo(i)
               recdiL.setValue("CG_STOPSEQUENCE",recordli.getInt("STOPSEQUENCE"),MboConstants.NOACCESSCHECK)