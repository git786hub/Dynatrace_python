# AUTOSCRIPT NAME: EX2POWFAPPRSTATUS
# CREATEDDATE: 2015-09-23 04:14:31
# CREATEDBY: U047
# CHANGEDATE: 2016-02-15 04:54:47
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from psdi.mbo import *
from java.util import Date

ex2po = mbo.getMboSet("EX2PO")
count=ex2po.count()
if count>0 :
	mbo1 = ex2po.getMbo(0)
	mbo1.changeStatus("APPR",Date(),"Review Process",MboConstants.NOACCESSCHECK)
	mbo1.setValue("EX2BUDOAAPPR",mbo1.getString("ex2revowner"),MboConstants.NOACCESSCHECK)
	mbo1.setValue("EX2BUDOADATE",Date(),MboConstants.NOACCESSCHECK)
	mbo1.setValue("EX2BUDOAAUTHAMT",mbo1.getString("EX2APPROVERSREQLIM.ex2limitamount"),MboConstants.NOACCESSCHECK)

#ex2po.save()