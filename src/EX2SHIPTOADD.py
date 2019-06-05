# AUTOSCRIPT NAME: EX2SHIPTOADD
# CREATEDDATE: 2017-01-25 01:06:47
# CREATEDBY: U171
# CHANGEDATE: 2017-02-16 20:45:58
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.server import MXServer
from psdi.mbo import SqlFormat
from psdi.mbo import MboConstants

print '*********************************************'
userInfo = mbo.getUserInfo()
site=mbo.getUserInfo().getInsertSite()
print '*********************************************'
print site

mbosite=mbo.getString("SITEID")

# print mbo.getThisMboSet().getParentApp()

if mbo.getThisMboSet().getParentApp() == 'PR' :
   if(cmp(site,mbosite)==false):
      mbo.setValue('EX2SHIPTO', ' ', MboConstants.NOACCESSCHECK)