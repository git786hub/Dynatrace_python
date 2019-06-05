# AUTOSCRIPT NAME: CG_UPDACTFINISH
# CREATEDDATE: 2013-10-08 06:05:28
# CREATEDBY: UFDA
# CHANGEDATE: 2013-10-08 13:12:35
# CHANGEBY: USZN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

parentrec = mbo.getMboSet("PARENT")

workordernum = mbo.getString("WONUM")
parentwo = parentrec.getMbo(0)

actfinish = parentwo.getString("ACTFINISH")
if actfinish is not None and actfinish <> "" :
   mbo.setValue("ACTFINISH",actfinish)
   print ' ***** wonum to update with actfinish1 is,' + workordernum