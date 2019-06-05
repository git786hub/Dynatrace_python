# AUTOSCRIPT NAME: EX2POWFFMESC1
# CREATEDDATE: 2015-09-16 04:20:39
# CREATEDBY: U047
# CHANGEDATE: 2016-02-15 04:40:32
# CHANGEBY: U03V
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

ex2powf = mbo.getMboSet("EX2ASSIGNEE")
count=ex2powf.count()
if count>0 :
	mbo1 = ex2powf.getMbo(0)
	mbo1.setValue("ex2flag",1,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
	mbo1.setValue("ex2status","Timed Out", MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
ex2powf .save()