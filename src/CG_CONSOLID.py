# AUTOSCRIPT NAME: CG_CONSOLID
# CREATEDDATE: 2012-03-24 13:16:14
# CREATEDBY: UHD0
# CHANGEDATE: 2014-10-12 10:08:12
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.app.asset import AssetRemote
from psdi.app.location import LocationRemote

ownermbo = mbo.getOwner()

if isinstance(ownermbo,AssetRemote):

    mboSetAssetSpec = ownermbo.getMboSet("CG_CSASSETSPEC")
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