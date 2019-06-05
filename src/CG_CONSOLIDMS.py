# AUTOSCRIPT NAME: CG_CONSOLIDMS
# CREATEDDATE: 2014-01-11 13:26:22
# CREATEDBY: USZN
# CHANGEDATE: 2014-10-22 14:16:15
# CHANGEBY: UXHD
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.app.asset import AssetRemote
from psdi.app.location import LocationRemote

ownermbo = mbo.getOwner()

if isinstance(ownermbo,AssetRemote):

    mboSetAssetSpec = ownermbo.getMboSet("CG_CSASSETSPECMS")
    num = mboSetAssetSpec.count()

    for i in range(num):
        mbospec = mboSetAssetSpec.getMbo(i)
        attrid = mbospec.getString("ASSETATTRID")
        attrvalue = mbo.getString(attrid)
        mbosetattrid = mbospec.getMboSet("ASSETATTRIBUTE")
        mboattrid = mbosetattrid.getMbo(0)
        if mboattrid.getString("DATATYPE") == "ALN" and attrvalue != ""  and attrvalue != None :
            mbospec.setValue("ALNVALUE",attrvalue)
        if mboattrid.getString("DATATYPE") == "NUMERIC" and attrvalue != "" and attrvalue != None :
            mbospec.setValueNull("NUMVALUE")
            mbospec.setValue("NUMVALUE",attrvalue,2)

    mbo.delete()
ownermbo.setValue("CG_IMPORT","1")

# following line of code is for location attributes which are not in use currently
if isinstance(ownermbo,LocationRemote):

    mboSetLocationSpec = ownermbo.getMboSet("CG_CSLOCATIONSPEC")
    numloc = mboSetLocationSpec.count()
    
    for j in range(numloc):
        mbolocspec = mboSetLocationSpec.getMbo(j)
        locattrid = mbolocspec.getString("ASSETATTRID")
        attrvalue = mbo.getString(locattrid)
        mbosetattrid = mbolocspec.getMboSet("ASSETATTRIBUTE")
        mboattrid = mbosetattrid.getMbo(0)
        if mboattrid.getString("DATATYPE") == "ALN" and attrvalue != ""  and attrvalue != None :
            mbolocspec.setValue("ALNVALUE",attrvalue)
        if mboattrid.getString("DATATYPE") == "NUMERIC" and attrvalue != "" and attrvalue != None :
            mbolocspec.setValueNull("NUMVALUE")
            mbolocspec.setValue("NUMVALUE",attrvalue,2)

    mbo.delete()