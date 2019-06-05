# AUTOSCRIPT NAME: CG_PROJNEW
# CREATEDDATE: 2014-01-29 06:30:37
# CREATEDBY: UVX3
# CHANGEDATE: 2014-09-05 02:11:44
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

childrec = None


childrec = mbo.getMboSet("CHILDTASK")
projectno = mbo.getString("CG_PROJNO")
glaccount =  mbo.getString("GLACCOUNT")
canapprove = mbo.getBoolean("CG_CANAPPROVELABOR")
num=childrec.count()
for i in range (num):
    childwo = childrec.getMbo(i)
    childwo.setValue("CG_PROJNO",projectno , MboConstants.NOACCESSCHECK)
    childwo.setValue("GLACCOUNT",glaccount , MboConstants.NOACCESSCHECK)
    childwo.setValue("CG_CANAPPROVELABOR",canapprove , MboConstants.NOACCESSCHECK)
	
if (childrec is not None and not childrec.isEmpty()) :
   childrec.close()