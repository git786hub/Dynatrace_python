# AUTOSCRIPT NAME: CGORGEMAIL
# CREATEDDATE: 2013-11-07 05:51:07
# CREATEDBY: UFQJ
# CHANGEDATE: 2013-11-07 06:04:20
# CHANGEBY: UFCV
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

wrkcntr = mbo.getString("WORKCENTER")

emailnotifymboset = mbo.getMboSet("CG_WORKEMAILNTFY")
cnt = emailnotifymboset.count()
for x in range(cnt):
    emailnotifymbo = emailnotifymboset.getMbo(x)
    emailnotify = emailnotifymbo.getString("EMAIL_CONTACT")
    emailnotifymbo.setValueNull("EMAIL_CONTACT")
    
newemailnotifymbo = emailnotifymboset.add()
newemailnotifymbo.setValue("WORKCENTER", wrkcntr)
newemailnotifymbo.setValue("EMAIL_CONTACT", emailnotify )