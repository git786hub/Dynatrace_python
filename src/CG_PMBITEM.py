# AUTOSCRIPT NAME: CG_PMBITEM
# CREATEDDATE: 2012-04-08 15:07:34
# CREATEDBY: UHD0
# CHANGEDATE: 2013-03-20 22:38:19
# CHANGEBY: MAXADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Draft

pmbuildset = mbo.getMboSet("CG_PMBUILD")
pnum = pmbuildset.count()

strPMBuildAssetSQL = ""
strPMBuildLocSQL = ""

print '*********Step 1'

manumboset = mbo.getMboSet("INVVENDOR")
if (manumboset.count() > 0) :
    strPMBuildAssetSQL = " and cg_manufacturer in ( select manufacturer from invvendor where itemnum = '" + mbo.getString("ITEMNUM") + "' and itemsetid = '"  + mbo.getString("ITEMSETID")  + "' ) "

print '***********In PMBITEM'

if pnum > 0 :
    pmbuild = pmbuildset.getMbo(0)
    if pmbuild :
        if pmbuild.getString("CG_ASSETOWNERSHIP") <> "" :
            strPMBuildAssetSQL = strPMBuildAssetSQL + " and cg_ownership  in (" + pmbuild.getString("CG_ASSETOWNERSHIP") + " ) "
        if pmbuild.getString("CG_ASSETVOLTAGECLASS") <> "" :
            strPMBuildAssetSQL = strPMBuildAssetSQL + " and cg_voltageclass in (" + pmbuild.getString("CG_ASSETVOLTAGECLASS") + ") "
        if pmbuild.getString("CG_ASSETMFGDATE1") <> "" :
            strPMBuildAssetSQL = strPMBuildAssetSQL + " and  cg_mfgdate >= ( select CG_ASSETMFGDATE1 from cg_pmbuild where itemnum ='" + mbo.getString("ITEMNUM") + "' ) "
        if pmbuild.getString("CG_ASSETMFGDATE2") <> "" :
            strPMBuildAssetSQL = strPMBuildAssetSQL + " and cg_mfgdate <= ( select CG_ASSETMFGDATE2 from cg_pmbuild where itemnum ='" + mbo.getString("ITEMNUM") + "' ) "
        if pmbuild.getString("CG_ASSETINSTALLDATE1") <> "" :
            strPMBuildAssetSQL = strPMBuildAssetSQL + " and  INSTALLDATE >= ( select CG_ASSETINSTALLDATE1 from cg_pmbuild where itemnum ='" + mbo.getString("ITEMNUM") + "' ) "
        if pmbuild.getString("CG_ASSETINSTALLDATE2") <> "" :
            strPMBuildAssetSQL = strPMBuildAssetSQL + " and INSTALLDATE <= ( select CG_ASSETINSTALLDATE2 from cg_pmbuild where itemnum ='" + mbo.getString("ITEMNUM") + "' ) "

        if pmbuild.getString("CG_LOCOWNERSHIP") <> "" :
            strPMBuildLocSQL = strPMBuildLocSQL + " and cg_ownership in (" + pmbuild.getString("CG_LOCOWNERSHIP") + ") "
        if pmbuild.getString("CG_LOCVOLTAGECLASS") <> "" :
            strPMBuildLocSQL = strPMBuildLocSQL + " and cg_voltageclass in (" + pmbuild.getString("CG_LOCVOLTAGECLASS") + ") "



itemspecmboset = mbo.getMboSet("ITEMSPECCLASS")
num = itemspecmboset.count()

strRecordFilterAssetSql = " classstructureid = '"+ mbo.getString("CLASSSTRUCTUREID") + "'" + strPMBuildAssetSQL 
strRecordFilterLocSql = " classstructureid = '"+ mbo.getString("CLASSSTRUCTUREID") + "'" + strPMBuildLocSQL 

for i in range(num) :
    itemspecmbo = itemspecmboset.getMbo(i)
    if itemspecmbo :
        pmbspecmboset = itemspecmbo.getMboSet("CG_PMBUILDSPEC")
        pmbspecmbo = pmbspecmboset.getMbo(0)

        if pmbspecmboset.count() > 0 and ( pmbspecmbo.getString("VALUE") <> "" or pmbspecmbo.getString("MINNUMERICVALUE") <> "" or pmbspecmbo.getString("MAXNUMERICVALUE") <> "" )   :
            strRecordFilterAssetSql = strRecordFilterAssetSql + " and exists (select assetnum from assetspec where asset.assetnum = assetspec.assetnum and assetspec.siteid = asset.siteid and assetattrid = '"
            strRecordFilterAssetSql = strRecordFilterAssetSql + itemspecmbo.getString("ASSETATTRID") + "'" 

            strRecordFilterLocSql = strRecordFilterLocSql + " and exists (select location from locationspec where locations.location = locationspec.location and locationspec.siteid = locations.siteid and assetattrid = '"
            strRecordFilterLocSql = strRecordFilterLocSql + itemspecmbo.getString("ASSETATTRID") + "'" 

        if pmbspecmbo and pmbspecmbo.getString("VALUE") is not None and pmbspecmbo.getString("VALUE") <> "" :
            strRecordFilterAssetSql = strRecordFilterAssetSql + " and alnvalue in (" + pmbspecmbo.getString("VALUE") + ") )"
            strRecordFilterLocSql = strRecordFilterLocSql + " and alnvalue in (" + pmbspecmbo.getString("VALUE") + ") )"

        if  pmbspecmbo and pmbspecmbo.getString("MINNUMERICVALUE") is not None and pmbspecmbo.getString("MAXNUMERICVALUE") is not None and pmbspecmbo.getString("MINNUMERICVALUE") <> "" and pmbspecmbo.getString("MAXNUMERICVALUE") <> "" :
            lMinValue =  pmbspecmbo.getString("MINNUMERICVALUE")
            lMaxValue =  pmbspecmbo.getString("MAXNUMERICVALUE")
            lMinValue = lMinValue.replace(',', '')
            lMaxValue = lMaxValue.replace(',', '')
            strRecordFilterAssetSql = strRecordFilterAssetSql + " and numvalue between " + lMinValue + " and " + lMaxValue +" )"
            strRecordFilterLocSql = strRecordFilterLocSql + " and numvalue between " + lMinValue + " and " +  lMaxValue +" )"

print '***********all good 1'

strNewRecordAssetSql = strRecordFilterAssetSql  + " and not exists ( select recordkey from cg_pmbuilditemrecords where itemnum = "
strNewRecordAssetSql = strNewRecordAssetSql + "'" + mbo.getString("ITEMNUM") + "' and ownertable= 'ASSET' and recordkey = asset.assetnum)"

strNewRecordLocSql = strRecordFilterLocSql  + " and not exists ( select recordkey from cg_pmbuilditemrecords where itemnum = "
strNewRecordLocSql = strNewRecordLocSql + "'" + mbo.getString("ITEMNUM") + "' and ownertable= 'LOCATIONS' and recordkey = locations.location)"

print '**********all good 2'
mbo.setValue("DESCRIPTION_LONGDESCRIPTION", strNewRecordAssetSql + "\n\n" + strNewRecordLocSql )

strNotExistSql = " not exists ( select assetnum from asset where asset.assetnum = cg_pmbuilditemrecords.recordkey and cg_pmbuilditemrecords.ownertable = 'ASSET' and "
strNotExistSql = strNotExistSql + strRecordFilterAssetSql + " )"

strNotExistSql = strNotExistSql + " and not exists ( select location from locations where locations.location = cg_pmbuilditemrecords.recordkey and cg_pmbuilditemrecords.ownertable = 'LOCATIONS' and " 
strNotExistSql = strNotExistSql + strRecordFilterLocSql + " )"

mbo.setValue("DESCRIPTION_LONGDESCRIPTION", strNewRecordAssetSql + "\n\n" + strNewRecordLocSql  + "\n\n" + strNotExistSql)

print '**********After desc set'

assetmboset = mbo.getMboSet ("CG_PMBASSET")
assetmboset.setWhere (strNewRecordAssetSql)

print strNewRecordAssetSql
print '*********OTHER'

locmboset = mbo.getMboSet ("CG_PMBLOCATIONS")
locmboset.setWhere (strNewRecordLocSql)

print strNewRecordLocSql
print '***********AND'

pmbitemrecmboset = mbo.getMboSet ("CG_PMBUILDITEMRECORDS")
pmbitemrecmboset.setWhere(strNotExistSql)

print strNotExistSql

pbmitemcount = pmbitemrecmboset.count()

for k in range(pbmitemcount) :
    pbmitemrecmbo = pmbitemrecmboset.getMbo(k)
    pbmitemrecmbo.delete()

astnum = assetmboset.count()

for j in range(astnum) :
    assetmbo = assetmboset.getMbo(j)
    if assetmbo :
        itemrecmbo = pmbitemrecmboset.add()
        itemrecmbo.setValue("OWNERTABLE", "ASSET")
        itemrecmbo.setValue("ITEMNUM", mbo.getString("ITEMNUM"))
        itemrecmbo.setValue("RECORDKEY", assetmbo.getString("ASSETNUM"))

locnum = locmboset.count()

for l in range(locnum) :
    locmbo = locmboset.getMbo(l)
    if locmbo :
        itemrecmbo = pmbitemrecmboset.add()
        itemrecmbo.setValue("OWNERTABLE", "LOCATIONS")
        itemrecmbo.setValue("ITEMNUM", mbo.getString("ITEMNUM"))
        itemrecmbo.setValue("RECORDKEY", locmbo.getString("LOCATION"))