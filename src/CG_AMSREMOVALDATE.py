# AUTOSCRIPT NAME: CG_AMSREMOVALDATE
# CREATEDDATE: 2015-12-18 22:29:45
# CREATEDBY: U03V
# CHANGEDATE: 2016-01-25 12:30:25
# CHANGEBY: UFAP
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.app.asset import AssetRemote
from psdi.mbo import MboConstants
from java.util import Date
from psdi.mbo import SqlFormat

if interactive:
  if isinstance(mbo,AssetRemote):
    assettype= mbo.getString("ASSETTYPE")
    assetStatus = mbo.getString("STATUS")
    if assetStatus == "AD" and (assettype== "C" or assettype== "O" or assettype == "T" or assettype== "U" or assettype == "V"):
     location = mbo.getString("LOCATION")
     print "@@@@@@@@@@@@@@@@@@"
     locMboSet = mbo.getMboSet("LOCATION")
     locType = locMboSet.getMbo(0).getString("TYPE")
     if locType !="PREMISE":
       mbo.setValue("EQ23", Date(), MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)