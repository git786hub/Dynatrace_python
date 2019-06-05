# AUTOSCRIPT NAME: EX2POWFINSTATUS
# CREATEDDATE: 2015-10-08 04:06:23
# CREATEDBY: U047
# CHANGEDATE: 2015-10-08 04:06:23
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
from psdi.mbo import *
from java.util import Date

ex2invoiceSet = mbo.getMboSet("EX2INVOICE")
count=ex2invoiceSet.count()
if count>0 :
        mbo1 = ex2invoiceSet.getMbo(0)
	mbo1.changeStatus("BUPEND",Date(),"Reviewer Process",MboConstants.NOACCESSCHECK)