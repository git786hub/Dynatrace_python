# AUTOSCRIPT NAME: EX2POWFFLAG
# CREATEDDATE: 2015-07-09 06:09:27
# CREATEDBY: U047
# CHANGEDATE: 2016-02-15 04:40:50
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

ex2powf = mbo.getMboSet("EX2ASSIGNEE")
count=ex2powf.count()
if count>0 :
	mbo1 = ex2powf.getMbo(0)
	mbo1.setValue("ex2flag",1,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
	mbo1.setValue("ex2status","ACCEPT", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
ex2powf.save()