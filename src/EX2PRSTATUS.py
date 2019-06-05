# AUTOSCRIPT NAME: EX2PRSTATUS
# CREATEDDATE: 2014-06-12 11:31:05
# CREATEDBY: UVX3
# CHANGEDATE: 2014-10-13 20:19:59
# CHANGEBY: UVD7
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants 

# if  mbo.getString("status") != "HOLD" :
#  # if mbo.getInitialValue("status") == "HOLD" :

if  mbo.getMboValue("status").getString()  != "HOLD" :
  if mbo.getMboValue("status").getPreviousValue().asString() == "HOLD" :
    prlset = mbo.getMboSet("prline")
    for i in range(prlset.count()) :
        prlmbo = prlset.getMbo(i)
        if prlmbo.getBoolean("ex2holdind") == True :
            prlmbo.setValue("ex2holdind",False,MboConstants.NOACCESSCHECK)