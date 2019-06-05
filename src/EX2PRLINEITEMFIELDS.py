# AUTOSCRIPT NAME: EX2PRLINEITEMFIELDS
# CREATEDDATE: 2013-10-02 13:06:21
# CREATEDBY: UFQJ
# CHANGEDATE: 2013-11-05 11:47:53
# CHANGEBY: UT76
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants 

# Populate Manufacturer PO Min Amt Indicator from companies listed in the approved manufacturers for this item

if mbo.isNull("ITEMNUM"):
    mbo.setValue("EX2MINAMTIND",False, MboConstants.NOACCESSCHECK)
else:
    # EX2MINPOCOMPANY relationship finds company with largest min PO amount for this item
    mfgmbo = mbo.getMboSet("EX2MINPOCOMPANY")
    if mfgmbo.count() > 0:
        mbo.setValue("EX2MINAMTIND",True, MboConstants.NOACCESSCHECK)
    else:
        mbo.setValue("EX2MINAMTIND",False, MboConstants.NOACCESSCHECK)

# Populate Buyer from Item Commodity Person association
mbo.setValueNull("EX2BUYER", MboConstants.NOACCESSCHECK)
if not mbo.isNull("ITEMNUM"):
    itemmboset = mbo.getMboSet("ITEM")         # need to hop to item, since commodity not populated on PR Line yet
    if itemmboset.count() > 0:
        itemmbo = itemmboset.getMbo(0)
        commmboset = itemmbo.getMboSet("EX2PERSCOMMODITY")
        if commmboset.count() > 0:
            commmbo = commmboset.getMbo(0)
            mbo.setValue("EX2BUYER",commmbo.getString("PERSONID"), MboConstants.NOACCESSCHECK)