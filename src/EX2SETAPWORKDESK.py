# AUTOSCRIPT NAME: EX2SETAPWORKDESK
# CREATEDDATE: 2013-12-11 08:04:33
# CREATEDBY: UFQJ
# CHANGEDATE: 2017-06-05 03:07:56
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote

if launchPoint == "EX2CHANGESTATUS"  and (mbo.getString("status")== "ENTERED") and (mbo.getString("SOURCESYSID") in ["EPAY","EDI","W2MS","ACIS","EEPM","BROUSSARD"]):
	wkdeskset = mbo.getMboSet("ex2invcwkdeskextsys")
	if wkdeskset.count() > 0 :
		wdmbo = wkdeskset.getMbo(0)
		mbo.setValue("ex2apworkdesk", wdmbo.getString("ex2wkdskgroup"), MboConstants.NOACCESSCHECK)

if (launchPoint <> "EX2CHANGESTATUS") :
	if not mbo.isNull("vendor") :
		wkdeskset = mbo.getMboSet("ex2invcwkdeskvdrid")
		if wkdeskset.count() < 1:
			wkdeskset = mbo.getMboSet("ex2invcwkdesk")
	else :
		wkdeskset = mbo.getMboSet("ex2invcwkdeskctr")
	if wkdeskset.count() > 0 :
		wdmbo = wkdeskset.getMbo(0)
		mbo.setValue("ex2apworkdesk", wdmbo.getString("ex2wkdskgroup"), MboConstants.NOACCESSCHECK)