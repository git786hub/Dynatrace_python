# AUTOSCRIPT NAME: CG_MEASUREMENT_ONLOAD
# CREATEDDATE: 2012-04-22 12:44:34
# CREATEDBY: UFQJ
# CHANGEDATE: 2018-11-29 23:40:34
# CHANGEBY: U1MZ
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.app.asset import AssetMeterRemote

oiladmboset = None

assetmeter = mbo.getOwner()
if isinstance(assetmeter,AssetMeterRemote):
    oiladmboset = assetmeter.getMboSet("CG_OILANALYSISDATA")
    num = oiladmboset.count()

  
    for i in range(num):
        oiladmbo = oiladmboset.getMbo(i)
        if oiladmbo :
            if oiladmbo.getString("OBSERVATION") <> "" and  oiladmbo.getString("OBSERVATION") is not None:
                mbo.setValue("OBSERVATION",oiladmbo.getString("OBSERVATION"))
            measurementoilmbo = oiladmbo.copy()
            measurementoilmbo.setValue("OWNERTABLE","MEASUREMENT")
            measurementoilmbo.setValue("RECORDID",mbo.getInt("MEASUREMENTID"))
            oiladmbo.setValue("LASTLABID",oiladmbo.getString("LABID"))
            oiladmbo.setValueNull("LABID")
            oiladmbo.setValueNull("SOURCE")
            oiladmbo.setValueNull("ANALYSISDATE")
            oiladmbo.setValueNull("OILTEMP")
            oiladmbo.setValueNull("H2")
            oiladmbo.setValueNull("CH4")
            oiladmbo.setValueNull("C2H6")
            oiladmbo.setValueNull("C2H4")
            oiladmbo.setValueNull("C2H2")
            oiladmbo.setValueNull("CO")
            oiladmbo.setValueNull("CO2")
            oiladmbo.setValueNull("N2")
            oiladmbo.setValueNull("O2")
            oiladmbo.setValueNull("TOTALGAS")
            oiladmbo.setValueNull("COMBUSTIBLEGAS")
            oiladmbo.setValueNull("TCG")
            oiladmbo.setValueNull("WATER")
            oiladmbo.setValueNull("WATERSAT")
            oiladmbo.setValueNull("IFT")
            oiladmbo.setValueNull("TAN")
            oiladmbo.setValueNull("D877")
            oiladmbo.setValueNull("D1816")
            oiladmbo.setValueNull("PF25")
            oiladmbo.setValueNull("PF100")
            oiladmbo.setValueNull("COLOR")
            oiladmbo.setValueNull("GRAVITY")
            oiladmbo.setValueNull("PCB")
            oiladmbo.setValueNull("AL")
            oiladmbo.setValueNull("FE")
            oiladmbo.setValueNull("CU")
            oiladmbo.setValueNull("PB")
            oiladmbo.setValueNull("SN")
            oiladmbo.setValueNull("ZINC")
            oiladmbo.setValueNull("BREAKERTEMP")
            oiladmbo.setValueNull("UM4")
            oiladmbo.setValueNull("UM14")
            oiladmbo.setValueNull("UM70")
            oiladmbo.setValueNull("UM6")
            oiladmbo.setValueNull("UM21")
            oiladmbo.setValueNull("UM10")
            oiladmbo.setValueNull("UM38")
            oiladmbo.setValueNull("ISOCODE")
            oiladmbo.setValueNull("ISOMETHOD")
            oiladmbo.setValueNull("CONCENTRATION")
            oiladmbo.setValueNull("SPILLNUM")
            oiladmbo.setValueNull("AROCLOR")
            oiladmbo.setValueNull("SAMPLETYPE")
            oiladmbo.setValueNull("SAMPLEDATE")
            oiladmbo.setValueNull("REMARKS")
            oiladmbo.setValueNull("OBSERVATION")
            oiladmbo.setValueNull("COMPARTMENT")
            oiladmbo.setValueNull("CONDITION")

if (oiladmboset is not None and not oiladmboset.isEmpty()) :
 oiladmboset.close()