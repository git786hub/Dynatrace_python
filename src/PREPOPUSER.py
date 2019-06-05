# AUTOSCRIPT NAME: PREPOPUSER
# CREATEDDATE: 2009-04-17 11:46:11
# CREATEDBY: PMSCADMUSR
# CHANGEDATE: 2009-04-17 13:04:03
# CHANGEBY: PMSCADMUSR
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.security import UserInfo
displayName = scriptHome.getUserInfo().getDisplayName();
contact = offeringAttributes.getValue("CONTACT");
if len(contact) == 0:
   offeringAttributes.setNewValue("CONTACT", displayName);