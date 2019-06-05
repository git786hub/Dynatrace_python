# AUTOSCRIPT NAME: EX2POWFPDRVSTATUS
# CREATEDDATE: 2015-09-02 06:38:52
# CREATEDBY: U047
# CHANGEDATE: 2016-02-15 04:40:04
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
	mbo1.changeStatus("PNDREV",Date(),"Review Process",MboConstants.NOACCESSCHECK)