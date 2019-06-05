# AUTOSCRIPT NAME: EX2PO2INVC
# CREATEDDATE: 2013-12-03 18:34:48
# CREATEDBY: UFQJ
# CHANGEDATE: 2015-04-10 00:56:26
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

pomboset = mbo.getMboSet("EX2PO2INVC")
if pomboset.count() > 0:
    pombo = pomboset.getMbo(0)
    mbo .setValue("ex2invappr", pombo.getString("ex2invappr"), MboConstants.NOACCESSCHECK)
    mbo .setValue("paymentterms", pombo.getString("paymentterms"), MboConstants.NOACCESSCHECK)