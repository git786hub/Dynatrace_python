# AUTOSCRIPT NAME: EX2POPOSTCAN
# CREATEDDATE: 2013-11-04 10:21:28
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-05-25 19:04:07
# CHANGEBY: UFQJ
# SCRIPTLANGUAGE: jython
# STATUS: Active

# set PR Line Hold indicators and Buyer as part of action group from escalation following status change to CAN.
#
from psdi.mbo import MboConstants
 
polset = mbo.getMboSet("POLINE")    # get lines for cancelled PO
num = polset.count()
for i in range(num):
    polmbo = polset.getMbo(i)
    prlset = polmbo.getMboSet("EX2PRLINEEX2")    # get corresponding PR lines using our EX2 link fields
    if prlset.count() > 0 :
        prlmbo = prlset.getMbo(0)
        # set hold indicator
        prlmbo.setValue("ex2holdind",True,MboConstants.NOACCESSCHECK)

        # now set buyer (or requestor on contract release)
        if mbo.getBoolean("ex2servicepo") == True and mbo.getString("potype") == "REL" and not mbo.isNull("contractrefnum") :
            prlmbo.setValue("requestedby", mbo.getString("ex2revowner"), MboConstants.NOACCESSCHECK)
        else :
            prlmbo.setValue("ex2buyer", mbo.getString("ex2revbuyer"), MboConstants.NOACCESSCHECK)