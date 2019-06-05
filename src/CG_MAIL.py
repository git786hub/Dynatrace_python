# AUTOSCRIPT NAME: CG_MAIL
# CREATEDDATE: 2017-02-16 00:20:54
# CREATEDBY: U171
# CHANGEDATE: 2017-02-16 00:20:54
# CHANGEBY: U171
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboConstants

userid = mbo.getString("PERSONID")
emailid = '@oncor.com'
emailaddress = userid+emailid
emailSet = mbo.getMboSet("PRIMARYEMAIL")
emailcnt = emailSet.count()
if emailcnt == 0:
	emailMbo = emailSet.add()
	emailMbo.setValue("PERSONID", userid, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION|MboConstants.NOACTION)
	emailMbo.setValue("EMAILADDRESS", emailaddress, MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION|MboConstants.NOACTION)
	emailMbo.setValue("ISPRIMARY", '1', MboConstants.NOACCESSCHECK|MboConstants.NOVALIDATION|MboConstants.NOACTION)