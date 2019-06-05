# AUTOSCRIPT NAME: EX2COPYREVOWN2DESAPPR
# CREATEDDATE: 2016-02-05 05:41:40
# CREATEDBY: U03V
# CHANGEDATE: 2016-02-09 05:09:15
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants
from psdi.mbo import *

ex2po = mbo.getMboSet("EX2PO")
count=ex2po.count()
if count>0 :
  mbo1 = ex2po.getMbo(0)
  mbo1.setValue("EX2DESAPPR",mbo.getString("EX2REVOWNER"), MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION|MboConstants.NOACTION)