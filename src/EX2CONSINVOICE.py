# AUTOSCRIPT NAME: EX2CONSINVOICE
# CREATEDDATE: 2015-04-08 08:39:53
# CREATEDBY: UVX3
# CHANGEDATE: 2015-04-08 08:41:22
# CHANGEBY: UT76
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

# Get Payment Terms from Purchase Contract
if mbo.getString("DOCUMENTTYPE") == "CONSIGNMENT":
	pvmboset = mbo.getMboSet("EX2IVVENDCONT")
	if pvmboset.count() > 0:
		pvmbo = pvmboset.getMbo(0)
		mbo.setValue("PAYMENTTERMS",pvmbo.getString("PAYMENTTERMS"),MboConstants.NOACCESSCHECK)