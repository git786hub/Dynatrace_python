# AUTOSCRIPT NAME: CG_LSCONSOLID
# CREATEDDATE: 2012-03-25 09:34:36
# CREATEDBY: UHD0
# CHANGEDATE: 2012-04-05 09:32:57
# CHANGEBY: UE7S
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.app.location import LocationRemote

locationmbo = mbo.getOwner()

if isinstance(locationmbo,LocationRemote):
    mboSetConsolid = locationmbo.getMboSet("CG_TRANSPOSECLASSSPEC")
    mboCSLocationSpec = mbo.getMboSet("CG_TRANSPOSECLASSSPEC")

    if mboSetConsolid.count > 0 and mboCSLocationSpec.count > 0  :
        attrid = mbo.getString("ASSETATTRID")
        mboConsolid = mboSetConsolid.getMbo(0)
        mboAttrCfg = mboCSLocationSpec.getMbo(0)
        if mboConsolid and mboAttrCfg :
            attrvalue = mboConsolid.getString(attrid)
            mbosetattrid = mbo.getMboSet("ASSETATTRIBUTE")
            mboattrid = mbosetattrid.getMbo(0)
            if mboattrid.getString("DATATYPE") == "ALN" and attrvalue != ""  and attrvalue != None :
                mbo.setValue("ALNVALUE",attrvalue)
            if mboattrid.getString("DATATYPE") == "NUMERIC" and attrvalue != "" and attrvalue != None :
                mbo.setValueNull("NUMVALUE")
                mbo.setValue("NUMVALUE",attrvalue,2)