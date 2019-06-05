# AUTOSCRIPT NAME: ADDTOCART
# CREATEDDATE: 2009-04-17 11:53:41
# CREATEDBY: PMSCADMUSR
# CHANGEDATE: 2009-04-17 15:30:32
# CHANGEBY: PMSCADMUSR
# SCRIPTLANGUAGE: jython
# STATUS: Active

rc = 1
errmsg = ''
installmq = offeringAttributes.getValue("INSTMQ");
mqdir = offeringAttributes.getValue("MQDIR");
if installmq == '1':
  if len(mqdir) == 0:
      rc = 0
      errmsg = 'If the Install MQ attribute is 1, then the MQ Directory Location attribute is required'
print rc
print errmsg