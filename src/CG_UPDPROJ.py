# AUTOSCRIPT NAME: CG_UPDPROJ
# CREATEDDATE: 2013-10-01 02:31:58
# CREATEDBY: UFDA
# CHANGEDATE: 2013-11-19 10:21:23
# CHANGEBY: USZN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

parentrec = mbo.getMboSet("PARENT")

workordernum = mbo.getString("WONUM")
parentwo = parentrec.getMbo(0)
projectno = parentwo.getString("CG_PROJNO")
actfinish = parentwo.getString("ACTFINISH")
mbo.setValue("CG_PROJNO",projectno)