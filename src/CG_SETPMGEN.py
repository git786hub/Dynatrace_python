# AUTOSCRIPT NAME: CG_SETPMGEN
# CREATEDDATE: 2012-11-08 02:56:16
# CREATEDBY: UHD0
# CHANGEDATE: 2012-11-08 02:56:16
# CHANGEBY: UFQJ
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

if mbo.getBoolean("CG_AUTOGEN") :
 mbo.setValue("CG_PMGEN",1,MboConstants.NOACCESSCHECK)
else :
 mbo.setValue("CG_PMGEN",0,MboConstants.NOACCESSCHECK)