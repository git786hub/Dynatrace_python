# AUTOSCRIPT NAME: CG_FAILUREREPORTOBJ
# CREATEDDATE: 2012-06-22 02:50:13
# CREATEDBY: UHD0
# CHANGEDATE: 2012-07-23 15:28:27
# CHANGEBY: UHD0
# SCRIPTLANGUAGE: jython
# STATUS: Draft

ownermbo = mbo.getOwner()

frdataset = mbo.getMboSet("CG_FAILUREREPORTDATA")
frdata = frdataset.add()
frdata.setValue("WONUM",mbo.getString("WONUM"))
frdata.setValue("WO_DESCRIPTION",ownermbo.getString("DESCRIPTION"))
frdata.setValue("FAILURECLASS",ownermbo.getString("FAILURECODE"))
frdata.setValue("SITEID",mbo.getString("SITEID"))
frdata.setValue("FAILUREREPORTID",mbo.getString("FAILUREREPORTID"))
frdata.setValue("ASSETNUM",mbo.getString("ASSETNUM"))
frdata.setValue("SIMILAR_ASSET",mbo.getString("ASSETNUM"))

assetset = mbo.getMboSet("ASSET")
acount = assetset.count()
if acount > 0 :
    asset = assetset.getMbo(0)
    frdata.setValue("ASSET_DESCRIPTION",asset.getString("DESCRIPTION"))
    frdata.setValue("CG_MFGDATE",asset.getString("CG_MFGDATE"))
    frdata.setValue("CG_VOLTAGECLASS",asset.getString("CG_VOLTAGECLASS"))
    frdata.setValue("CG_OWNERSHIP",asset.getString("CG_OWNERSHIP"))
    frdata.setValue("CHANGEBY",asset.getString("CHANGEBY"))
    frdata.setValue("CHANGEDATE",asset.getDate("CHANGEDATE"))
    frdata.setValue("INSTALLDATE",asset.getString("INSTALLDATE"))

locationset = ownermbo.getMboSet("LOCATION")
lcount = locationset.count()
if lcount > 0 :
    location = locationset.getMbo(0)
    frdata.setValue("LOCATION",location.getString("LOCATION"))
    frdata.setValue("LOC_DESCRIPTION",location.getString("DESCRIPTION"))
    frdata.setValue("LOC_VOLTAGECLASS",location.getString("CG_VOLTAGECLASS"))
    frdata.setValue("CG_LOCLEGACYID",location.getString("CG_LOCLEGACYID"))

jpset = mbo.getMboSet("JOBPLAN")
jcount = jpset.count()
if jcount > 0 :
    jp = jpset.getMbo(0)
    frdata.setValue("JP_DESCRIPTION",jp.getString("DESCRIPTION"))