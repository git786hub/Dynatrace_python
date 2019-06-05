# AUTOSCRIPT NAME: CG_LIMSATTRIBUTE
# CREATEDDATE: 2016-01-12 13:06:53
# CREATEDBY: UFAP
# CHANGEDATE: 2018-06-14 04:17:54
# CHANGEBY: U4B0
# SCRIPTLANGUAGE: jython
# STATUS: Draft

if (mbo.getString("ASSETATTRID")=="LIMS_DIELECT_KV"):
  mbo.save()
  cg_assetmeterset=mbo.getMboSet("CG_ASSETMETER")
  num1 = cg_assetmeterset.count()
  for i in range (num1):
    cg_assetmetermbo=cg_assetmeterset.getMbo(i)
    if ( cg_assetmetermbo.getString("METERNAME")=="DGALTC" or cg_assetmetermbo.getString("METERNAME")=="DGALTC2" ):
      assetmeterconsmboset =cg_assetmetermbo.getMboSet ("CG_METERCONDITIONS")
      meterconsmboset = cg_assetmetermbo.getMboSet("CG_CMTR_CONDITIONS")
      num = meterconsmboset.count()
      for k in range(num) :
          meterconmbo =  meterconsmboset.getMbo(k)
          print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
          print meterconmbo.getString("OBSERVATION")
          whereclause="OBSERVATION='DIELECTRIC_TRK'"
          assetmeterconsmboset.setWhere(whereclause)
          num2 = assetmeterconsmboset.count()
          print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
          if (meterconmbo.getString("OBSERVATION")=="DIELECTRIC_TRK"):
             if (num2==0):
                assetmeterconsmbo = assetmeterconsmboset.add()  
                assetmeterconsmbo.setValue("OWNERTABLE", "ASSET")
                assetmeterconsmbo.setValue("METERNAME", cg_assetmetermbo.getString("METERNAME"))
                assetmeterconsmbo.setValue("RECORDKEY", cg_assetmetermbo.getString("ASSETNUM"))
                assetmeterconsmbo.setValue("RECORDSITEID", cg_assetmetermbo.getString("SITEID"))
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