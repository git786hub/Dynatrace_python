# AUTOSCRIPT NAME: EX2INT43
# CREATEDDATE: 2014-03-13 13:42:40
# CREATEDBY: UFQJ
# CHANGEDATE: 2016-02-05 03:48:10
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 
from java.lang import String

# EX2INT43 
# SITE.EX2FREIGHTACCT
# Freight Charges for DIS Site
# Freight Charges for TRN Site
# SITE.EX2FREIGHTMGMTACCT
# Broussard Service Fee for TRN Site
# Broussard Service Fee for DIS Site

def getGLacct(description):
	descr=String(description)
	acct=""
	ck = mbo.getUserInfo().getConnectionKey()
	conn = mbo.getMboServer().getDBConnection(ck)
	stmt = conn.createStatement()
	whereClause = "SITEID='DIS'"
	if descr.indexOf("TRN")>-1:
		whereClause = "SITEID='TRN'"
	rs = stmt.executeQuery("select * from site where " + whereClause)
	if rs.next():
		if descr.indexOf(" Service Fee ")>-1:
			acct= rs.getString("EX2FREIGHTMGMTACCT")
		else:
			acct= rs.getString("EX2FREIGHTACCT")

	mbo.getMboServer().freeDBConnection(ck)
	stmt.close()
	rs.close()	
	return acct

polmboset = mbo.getMboSet("POLINE")
polcount = polmboset.count()

for i in range(polcount):
	mbopoline = polmboset.getMbo(i)
	mbopoline.setValue("GLDEBITACCT", getGLacct(mbopoline.getString("DESCRIPTION")), MboConstants.NOACCESSCHECK)