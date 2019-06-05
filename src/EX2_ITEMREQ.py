# AUTOSCRIPT NAME: EX2_ITEMREQ
# CREATEDDATE: 2013-09-16 13:47:17
# CREATEDBY: UFQJ
# CHANGEDATE: 2013-10-11 15:07:07
# CHANGEBY: UUYC
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.mbo import MboConstants

if app in ["SARITEM"]:

    if mbo.getString("EX2REQUESTTYPE") == "CHANGE ITEM":
        mbo.setValue("EX2NEWDESC",mbo.getString("DESCRIPTION"),MboConstants.NOACCESSCHECK)
        mbo.setValue("EX2NEWCOMMGROUP",mbo.getString("COMMODITYGROUP"),MboConstants.NOACCESSCHECK)
        mbo.setValue("EX2NEWCOMMODITY",mbo.getString("COMMODITY"),MboConstants.NOACCESSCHECK)
        mbo.setValue("EX2NEWISSUEUNIT",mbo.getString("ISSUEUNIT"),MboConstants.NOACCESSCHECK)
        mbo.setValue("EX2NEWORDERUNIT",mbo.getString("ORDERUNIT"),MboConstants.NOACCESSCHECK)
        mbo.setValue("EX2NEWSDS",mbo.getBoolean("EX2SDS"),MboConstants.NOACCESSCHECK)
        mbo.setValue("EX2NEWINSPREQ",mbo.getBoolean("INSPECTIONREQUIRED"),MboConstants.NOACCESSCHECK)
        mbo.setValue("EX2NEWSOFTWARE",mbo.getBoolean("TLOAMISSOFTWARE"),MboConstants.NOACCESSCHECK)
        
    if mbo.getString("EX2REQUESTTYPE") == "ADD/OBSOLETE PARTS" or mbo.getString("EX2REQUESTTYPE") == "OBSOLETE ITEM":
        mbo.setValueNull("EX2NEWDESC",MboConstants.NOACCESSCHECK)
        mbo.setValueNull("EX2NEWCOMMGROUP",MboConstants.NOACCESSCHECK)
        mbo.setValueNull("EX2NEWCOMMODITY",MboConstants.NOACCESSCHECK)
        mbo.setValueNull("EX2NEWISSUEUNIT",MboConstants.NOACCESSCHECK)
        mbo.setValueNull("EX2NEWORDERUNIT",MboConstants.NOACCESSCHECK)
        mbo.setFieldFlag("EX2NEWSDS", MboConstants.READONLY, False)
        mbo.setFieldFlag("EX2NEWINSPREQ", MboConstants.READONLY, False)
        mbo.setFieldFlag("EX2NEWSOFTWARE", MboConstants.READONLY, False)

    if mbo.getString("EX2REQUESTTYPE") == "CHANGE ITEM" and mbo.getBoolean("EX2NEWSDS") and mbo.getBoolean("EX2SDS") :
        mbo.setFieldFlag("EX2NEWSDS", MboConstants.READONLY, True)