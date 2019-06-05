# AUTOSCRIPT NAME: EX2UPDATECONTRACTLINE
# CREATEDDATE: 2015-08-03 09:00:07
# CREATEDBY: UVX3
# CHANGEDATE: 2015-08-04 05:24:29
# CHANGEBY: U047
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote


cntmboset = mbo.getMboSet("EX2CONTRACTLINE")
num = cntmboset.count()

if (num >0):
   for i in range (num) :
      cntmbo= cntmboset .getMbo(i)
      if launchPoint == 'EX2COMMODITYGROUPUPDATE':
           cntmbo.setValue("COMMODITYGROUP", mbo.getString("COMMODITYGROUP") , MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
           cntmbo.setValue("COMMODITY",mbo.getString("COMMODITY") , MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
      if launchPoint == 'EX2ITEMDESCRIPTIONUPDATE':
           cntmbo.setValue("DESCRIPTION", mbo.getString("DESCRIPTION") , MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
      if launchPoint == 'EX2ITEMCOMMODITYUPDATE':
           cntmbo.setValue("COMMODITY",mbo.getString("COMMODITY") , MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
      if launchPoint == 'EX2ORDERUNITUPDATE':
           cntmbo.setValue("ORDERUNIT",mbo.getString("ORDERUNIT") ,   MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
      if launchPoint == 'EX2ITEMLONGDESCRIPTIONUPDATE':
           cntmbo.setValue("description_longdescription", mbo.getString("description_longdescription") , MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)