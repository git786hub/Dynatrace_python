# AUTOSCRIPT NAME: EX2_RESTIPOLEADTIME
# CREATEDDATE: 2017-06-18 11:36:55
# CREATEDBY: U03V
# CHANGEDATE: 2017-06-18 11:36:55
# CHANGEBY: U0OT
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

if app not in ['INVENTOR'] and mbo.getThisMboSet().getParentApp() in ['SHIPREC'] :
  print "Parent is"+mbo.getThisMboSet().getParentApp()
  leadTime=mbo.getString("DELIVERYTIME")
  print "Lead Time After              = "+leadTime
  leadTime1= mbo.getMboValue("DELIVERYTIME").getPreviousValue().asString()
  print "Lead Time Before           = " +leadTime1
  mbo.setValue("DELIVERYTIME",leadTime1,MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION)
  print "Lead Time Final           = "+mbo.getString("DELIVERYTIME")
  print "End of loopppp----------------------------------------"