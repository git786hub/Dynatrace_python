# AUTOSCRIPT NAME: EX2SETQTYONORDER
# CREATEDDATE: 2013-09-10 13:32:43
# CREATEDBY: UFQJ
# CHANGEDATE: 2016-08-19 22:27:43
# CHANGEBY: UGVD
# SCRIPTLANGUAGE: jython
# STATUS: Active

#Script to calculate and update Quantity on Order value from the Open POs & Receipts.

from psdi.mbo import MboConstants
from psdi.mbo import Mbo

if not interactive:
	totalorderedqty=0
	polinercvdqty=0
	polineordqty=0

	polineSet = mbo.getMboSet("EX2EMTQTYONODR")
	polcount = polineSet.count()

	for i in range(polcount):
	 mbopoline = polineSet.getMbo(i)
	 polineordqty = mbopoline.getInt("ORDERQTY")
	 polinercvdqty = mbopoline.getInt("RECEIVEDQTY")
	 totalorderedqty = totalorderedqty + polineordqty - polinercvdqty

	mbo.setValue("EX2QTYONORDER", totalorderedqty,MboConstants.NOACCESSCHECK)