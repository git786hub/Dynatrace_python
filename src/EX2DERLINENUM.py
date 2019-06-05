# AUTOSCRIPT NAME: EX2DERLINENUM
# CREATEDDATE: 2013-11-04 13:49:14
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-10-13 20:15:32
# CHANGEBY: UVD7
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

s_rem = "**derl** "
print s_rem
if onadd and mbo.getString("SITEID")=="TRN":
	prderln=0
	wpderln=0
	derlinenum = 1

	wpset = mbo.getMboSet("EX2WPSAMEDER")
	prset = mbo.getMboSet("EX2PRSAMEDER")
	if (wpset.count()>0):
	   wpderln = wpset.max("EX2DERLINENUM")
	if (prset.count()>0):
		prderln = prset.max("EX2DERLINENUM")
	if (wpderln>prderln):
	   derlinenum = wpderln
	else:
	   derlinenum = prderln
	print s_rem +"Largest "+ str(derlinenum)

	#mbo.setValue("EX2DERLINENUM",derlinenum,MboConstants.NOACCESSCHECK)

	cms = mbo.getThisMboSet() 
	curCount = cms.count()
	print s_rem +"Mbo count " + str(curCount)
	mbo.setValue("EX2DERLINENUM",derlinenum+curCount,MboConstants.NOACCESSCHECK)
	print s_rem + str(derlinenum+curCount)

print s_rem