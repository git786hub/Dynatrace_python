# AUTOSCRIPT NAME: CG_ASCONSPECMS
# CREATEDDATE: 2014-01-11 13:30:31
# CREATEDBY: USZN
# CHANGEDATE: 2014-10-31 09:04:47
# CHANGEBY: UQRM
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.app.asset import AssetRemote

assetmbo = mbo.getOwner()
mbosetattrid = None
mboCSAssetSpec = None
mboSetConsolid = None

if isinstance(assetmbo,AssetRemote):
    mboSetConsolid = assetmbo.getMboSet("CG_MSTRANSPOSECLASSSPEC")
    mboCSAssetSpec = mbo.getMboSet("CG_MSTRANSPOSECLASSSPEC")
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

# assetmbo.setValue("CG_IMPORT","1")

if (mbosetattrid is not None and not mbosetattrid.isEmpty()) :
   mbosetattrid.close()
     
if (mboCSAssetSpec is not None and not mboCSAssetSpec.isEmpty()) :   
   mboCSAssetSpec.close()
  
if (mboSetConsolid is not None and not mboSetConsolid.isEmpty()) :
   mboSetConsolid.close()