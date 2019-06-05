# AUTOSCRIPT NAME: UPDATEDESC
# CREATEDDATE: 2013-10-22 10:39:49
# CREATEDBY: UFDA
# CHANGEDATE: 2014-10-13 04:05:02
# CHANGEBY: UQRM
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.app.asset import AssetRemote

ownermboset = mbo.getThisMboSet()

ownermboset.clearWarnings()

if (onadd):
   print("add. Do nothing")

else:
   mbo.updateDesc()
   mbo.save()