# AUTOSCRIPT NAME: CG_TESTOK
# CREATEDDATE: 2016-09-20 02:29:31
# CREATEDBY: U03V
# CHANGEDATE: 2016-10-16 04:46:22
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.server import MXServer



num1=mbo.getDouble("AVG_WHR_REG_AF")


if (num1>=98.00 and num1<=102.00) :
 mbo.setValue("TEST_OK",'Y',MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
else :
 mbo.setValue("TEST_OK",'N',MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)