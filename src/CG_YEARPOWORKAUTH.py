# AUTOSCRIPT NAME: CG_YEARPOWORKAUTH
# CREATEDDATE: 2013-10-25 02:20:15
# CREATEDBY: UFDA
# CHANGEDATE: 2014-05-13 09:45:31
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from java.util import Date

propertyUnit = None
dateSet  = None

doclinksmboSet= mbo.getThisMboSet()

dateSet = mbo.getMboSet("CG_DATEVIEW")
yearmbo = dateSet.getMbo(0)

year = yearmbo.getString("CURRENTYR")

mbo.setValue("CG_YEARCAPITALIZED", year, MboConstants.NOACCESSCHECK)

propertyUnit = mbo.getMboSet("CG_ASSETPROPUNITWA")
poworkmbo = propertyUnit .getMbo(0)

poworkauth = poworkmbo.getString("POWORKAUTH")

mbo.setValue("CG_POWORKAUTH", poworkauth, MboConstants.NOACCESSCHECK)

if (propertyUnit is not None and not propertyUnit.isEmpty()) :   
   propertyUnit.close()
   

if (dateSet is not None and not dateSet.isEmpty()) :   
   dateSet.close()