# AUTOSCRIPT NAME: PREPOPEMAIL
# CREATEDDATE: 2011-09-03 08:33:59
# CREATEDBY: PMSCADMUSR
# CHANGEDATE: 2011-09-03 10:25:51
# CHANGEBY: PMSCADMUSR
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.security import UserInfo
displayName = scriptHome.getUserInfo().getEmail();
contact = offeringAttributes.getValue("USERID");
if len(contact) == 0:
   offeringAttributes.setNewValue("USERID", displayName);