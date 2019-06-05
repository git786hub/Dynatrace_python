# AUTOSCRIPT NAME: EX2_SETPMTYPE
# CREATEDDATE: 2018-01-17 03:49:59
# CREATEDBY: U171
# CHANGEDATE: 2018-03-11 11:01:13
# CHANGEBY: U171
# SCRIPTLANGUAGE: python
# STATUS: Draft

from psdi.mbo import MboConstants

if mbo.getThisMboSet().getParentApp() in ['ASSETS_TRN', 'LOCATS_TRN']:
 frequency = mbo.getInt("FREQUENCY")
 if(frequency==0 or frequency==999):
  mbo.setValue("EX2SETPMTYPE","On-demand")
 else:
  mbo.setValue("EX2SETPMTYPE","Scheduled")