# AUTOSCRIPT NAME: EX2READONLY
# CREATEDDATE: 2017-05-09 06:30:44
# CREATEDBY: U171
# CHANGEDATE: 2017-06-09 15:59:52
# CHANGEBY: UYCR
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

FIRSTNAME =mbo.getString("FIRSTNAME") 
LASTNAME =mbo.getString("LASTNAME")
DISPLAYNAME =mbo.getString("DISPLAYNAME")

appName = mbo.getThisMboSet().getParentApp()

if not mbo.isNull("FIRSTNAME"):
	print  'INSIDE FIRSTNAME'
	mbo.setFieldFlag("FIRSTNAME", MboConstants.READONLY, True)

if not mbo.isNull("LASTNAME"):
	print  'INSIDE LASTNAME'
	mbo.setFieldFlag("LASTNAME", MboConstants.READONLY, True)

if not mbo.isNull("DISPLAYNAME"):
	print  'INSIDE DISPLAYNAME'
	mbo.setFieldFlag("DISPLAYNAME", MboConstants.READONLY, True)