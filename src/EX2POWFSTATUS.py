# AUTOSCRIPT NAME: EX2POWFSTATUS
# CREATEDDATE: 2015-08-07 09:16:42
# CREATEDBY: U047
# CHANGEDATE: 2016-02-21 13:54:56
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
	mbo1.changeStatus("BUPEND",Date(),"Review Process",MboConstants.NOACCESSCHECK)