# AUTOSCRIPT NAME: CG_ASCONSPEC
# CREATEDDATE: 2012-03-25 00:27:27
# CREATEDBY: UHD0
# CHANGEDATE: 2014-05-13 09:28:30
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.app.asset import AssetRemote
from psdi.mbo import MboConstants

assetmbo = mbo.getOwner()
mbosetattrid = None
mboCSAssetSpec = None
mboSetConsolid = None


if isinstance(assetmbo,AssetRemote):
    mboSetConsolid = assetmbo.getMboSet("CG_TRANSPOSECLASSSPEC")
    mboCSAssetSpec = mbo.getMboSet("CG_TRANSPOSECLASSSPEC")
    num = mboSetConsolid.count
    if num > 0  and mboCSAssetSpec.count > 0  :
        attrid = mbo.getString("ASSETATTRID")
        mboConsolid = mboSetConsolid.getMbo(0)
        mboAttrCfg = mboCSAssetSpec.getMbo(0)
        if mboConsolid and mboAttrCfg :
            attrvalue = mboConsolid.getString(attrid)
            mbosetattrid = mbo.getMboSet("ASSETATTRIBUTE")
            mboattrid = mbosetattrid.getMbo(0)
            if mboattrid.getString("DATATYPE") == "ALN" and attrvalue != ""  and attrvalue != None :
                mbo.setValue("ALNVALUE",attrvalue )
            if mboattrid.getString("DATATYPE") == "NUMERIC" and attrvalue != "" and attrvalue != None :
                mbo.setValueNull("NUMVALUE")
                mbo.setValue("NUMVALUE",attrvalue,2)
               

if (mbosetattrid is not None and not mbosetattrid.isEmpty()) :
   mbosetattrid.close()
   
if (mboCSAssetSpec is not None and not mboCSAssetSpec.isEmpty()) :   
   mboCSAssetSpec.close()

if (mboSetConsolid is not None and not mboSetConsolid.isEmpty()) :
   mboSetConsolid.close()