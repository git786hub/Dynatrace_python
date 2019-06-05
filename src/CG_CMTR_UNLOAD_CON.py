# AUTOSCRIPT NAME: CG_CMTR_UNLOAD_CON
# CREATEDDATE: 2012-04-21 05:14:09
# CREATEDBY: UFQJ
# CHANGEDATE: 2013-08-28 08:20:11
# CHANGEBY: UFDA
# SCRIPTLANGUAGE: jython
# STATUS: Draft

assetmeterconsmboset = mbo.getMboSet ("CG_METERCONDITIONS")
num = assetmeterconsmboset.count()

for i in range(num) :
    assetmeterconsmbo = assetmeterconsmboset.getMbo(i)
    assetmeterconsmbo.delete()

analysisdatamboset = mbo.getMboSet ("CG_OILANALYSISDATA")
adnum = analysisdatamboset.count()

for j in range(adnum) :
    analysisdatambo = analysisdatamboset.getMbo(j)
    analysisdatambo.delete()