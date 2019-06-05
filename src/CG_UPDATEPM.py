# AUTOSCRIPT NAME: CG_UPDATEPM
# CREATEDDATE: 2014-03-21 01:24:40
# CREATEDBY: USZN
# CHANGEDATE: 2014-03-21 01:24:40
# CHANGEBY: USZN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

#import time
from psdi.mbo import MboConstants
#prbrec = mbo.getMboSet("PMCORRECTION")
#prbrecno = prbrec.count()
#prbrecnochg = 100
#prbrecnochg = int(prbrecno)
#prbrecno1 = 100
#if (prbrec.count() > 0 ):
#if (prbrecnochg > 0 ):
   
#for i in range(prbrec.count()):
                
#problematicrec = prbrec.getMbo(i)
#lastwo = problematicrec.getMboSet("LASTWOANY")
lastwo = mbo.getMboSet("LASTWOANY")
if (lastwo.count() > 0 ):
   lastworec = lastwo.getMbo(0)
   mbo.setValue("LASTSTARTDATE",lastworec.getDate("REPORTDATE"),MboConstants.NOACCESSCHECK)
#time.sleep(0.5)