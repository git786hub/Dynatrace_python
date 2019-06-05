# AUTOSCRIPT NAME: EX3ASSETSPECATTR
# CREATEDDATE: 2017-05-23 15:59:37
# CREATEDBY: U171
# CHANGEDATE: 2017-05-31 17:04:35
# CHANGEBY: UT76
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

if (mbo.getString('ASSETATTRID')=='ONCORPGM'):
 oncPgmset = mbo.getMboSet("EX3ONCORPGM")

 if oncPgmset.count() == 0 :
  global errorkey, errorgroup, params
  errorkey="invalidOncorPgmID"
  errorgroup="ex3_asset"
  params = [mbo.getString("alnvalue")]