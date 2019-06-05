# AUTOSCRIPT NAME: CG_UPDASTMTRSEQ
# CREATEDDATE: 2014-10-12 09:28:32
# CREATEDBY: UVX3
# CHANGEDATE: 2014-10-13 03:06:27
# CHANGEBY: USZN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants
sequence = mbo.getInt("SEQUENCE")
routemeter = mbo.getMboSet("CG_ROUTEMETER")
numrec1 = routemeter.count()
if (numrec1 > 0) :
   for i in range (numrec1):
       routemeterrec = routemeter.getMbo(i)
       routemeterrec.setValue("CG_METSEQUENCE",sequence,MboConstants.NOACCESSCHECK)