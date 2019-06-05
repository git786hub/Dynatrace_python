# AUTOSCRIPT NAME: CG_CMTR_ONLOAD_CON
# CREATEDDATE: 2012-04-21 04:40:03
# CREATEDBY: UFQJ
# CHANGEDATE: 2017-09-25 09:15:42
# CHANGEBY: UZHC
# SCRIPTLANGUAGE: jython
# STATUS: Draft

cg_assetspecset=mbo.getMboSet("CG_ASSETSPEC")
cg_assetspecset.save()
analysisdatamboset = mbo.getMboSet ("CG_OILANALYSISDATA")

print '$$$$$$$$$$$$$$$$'
print analysisdatamboset .count()
print '$$$$$$$$$$$$$$$$'

analysisdatambo = analysisdatamboset.add()
analysisdatambo.setValue("OWNERTABLE","ASSETMETER")
analysisdatambo.setValue("RECORDID",mbo.getInt("ASSETMETERID"))
analysisdatambo.setValue("RECORDSITEID", mbo.getString("SITEID"))
analysisdatambo.setValue("SOURCE", "MANUAL")

analysisdatamboset.save() 

assetmeterconsmboset = mbo.getMboSet ("CG_METERCONDITIONS")

meterconsmboset = mbo.getMboSet("CG_CMTR_CONDITIONS")
num = meterconsmboset.count()
print 'count of METER reading $$$$$$$$$$$$$$$$'
print num
print 'end of count of METER reading $$$$$$$$$$$$$$$$'

for k in range(num) :
    assetmeterconsmbo = assetmeterconsmboset.add()  
    meterconmbo =  meterconsmboset.getMbo(k)
    assetmeterconsmbo.setValue("OWNERTABLE", "ASSET")
    assetmeterconsmbo.setValue("METERNAME", mbo.getString("METERNAME"))
    assetmeterconsmbo.setValue("RECORDKEY", mbo.getString("ASSETNUM"))
    assetmeterconsmbo.setValue("RECORDSITEID", mbo.getString("SITEID"))
    assetmeterconsmbo.setValue("OBSERVATION",  meterconmbo.getString("OBSERVATION"))
    assetmeterconsmbo.setValue("VOLTAGECLASS",  meterconmbo.getString("VOLTAGECLASS"))
    assetmeterconsmbo.setValue("PRIORITY", meterconmbo.getString("PRIORITY"))
    assetmeterconsmbo.setValue("GENERATENOTIFICATION", meterconmbo.getString("GENERATENOTIFICATION"))
    assetmeterconsmbo.setValue("EXPOBJECT",  meterconmbo.getString("EXPOBJECT"))
    assetmeterconsmbo.setValue("CONDITION", meterconmbo.getString("CONDITION"))
    assetmeterconsmbo.setValue("RPTHEADING", meterconmbo.getString("RPTHEADING"))
    assetmeterconsmbo.setValue("ACTITEM", meterconmbo.getString("ACTITEM"))
    assetmeterconsmbo.setValue("TEMPID", meterconmbo.getString("TEMPID"))
    assetmeterconsmbo.setValue("DISP_CONDITION", meterconmbo.getString("DISP_CONDITION"))
    print '%%%%%%in for loop after add%%%%%%%%%%'
assetmeterconsmboset.save()