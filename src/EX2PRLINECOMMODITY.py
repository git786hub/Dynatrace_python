# AUTOSCRIPT NAME: EX2PRLINECOMMODITY
# CREATEDDATE: 2013-11-12 15:33:35
# CREATEDBY: UFQJ
# CHANGEDATE: 2013-11-12 18:11:21
# CHANGEBY: UUYZ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants

# Populate Buyer from Commodity Person association
mbo.setValueNull("EX2BUYER", MboConstants.NOACCESSCHECK)

commmboset = mbo.getMboSet("EX2PERSCOMMODITY")
if commmboset.count() > 0:
    commmbo = commmboset.getMbo(0)
    mbo.setValue("EX2BUYER",commmbo.getString("PERSONID"), MboConstants.NOACCESSCHECK)