# AUTOSCRIPT NAME: EX2POWF
# CREATEDDATE: 2015-07-08 03:58:11
# CREATEDBY: U047
# CHANGEDATE: 2015-07-29 05:40:13
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.tloam.app.po import PORemote
from psdi.app.invoice import InvoiceRemote

ownermbo = mbo.getOwner()
if isinstance(ownermbo,PORemote):
	mbo.setValue("ex2ponum",ownermbo.getString("ponum"),MboConstants.NOACCESSCHECK)
	mbo.setValue("ex2revisionnum",ownermbo.getString("revisionnum"),MboConstants.NOACCESSCHECK)
	mbo.setValue("ex2type",'PO',MboConstants.NOACCESSCHECK)
	mbo.setValue("siteid",ownermbo.getString("siteid"),MboConstants.NOACCESSCHECK)
if isinstance(ownermbo,InvoiceRemote):
	mbo.setValue("ex2ponum",ownermbo.getString("invoicenum"),MboConstants.NOACCESSCHECK)
	mbo.setValue("ex2type",'INVOICE',MboConstants.NOACCESSCHECK)
	mbo.setValue("siteid",ownermbo.getString("siteid"),MboConstants.NOACCESSCHECK)