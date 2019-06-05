# AUTOSCRIPT NAME: CDUIRESETPSW
# CREATEDDATE: 2014-10-30 02:24:34
# CREATEDBY: MAXADMIN
# CHANGEDATE: 2014-11-03 06:05:38
# CHANGEBY: MAXADMIN
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.server import MXServer
from psdi.mbo import SqlFormat
from psdi.mbo import MboConstants

try:
	#Set the headers to the default values before starting the processing
	responseHeaders.put("content-type","text/plain")
	responseHeaders.put("OPCODE","0")
	responseHeaders.put("OPMSG","Successful")
	print "CDUIRESETPSW: getting the signature service:"
	sigService =  MXServer.getMXServer().lookup("SIGNATURE")
	#Get the user Id as header parameter
	userID = request.getQueryParam("userid")
	print "CDUIRESETPSW: userid from request userID:", userID

	if(userID == None):
		responseHeaders.put("OPCODE","1")
		responseHeaders.put("OPMSG","Missing user ID")
		print "CDUIRESETPSW: missing userID"
	elif( sigService == None):
		responseHeaders.put("OPCODE","2")
		responseHeaders.put("OPMSG","Internal error")
		print "CDUIRESETPSW: missing signature service"
	else:
		uInfo = MXServer.getMXServer().getUserInfo(userID)
		set = MXServer.getMXServer().getMboSet("MAXUSER", uInfo)
		s = SqlFormat(uInfo, "userid = :1")
		s.setObject(1, "MAXUSER", "userid", userID)
		set.setWhere(s.format())
		set.reset()
		if(set.isEmpty()):
			responseHeaders.put("OPCODE","3")
			responseHeaders.put("OPMSG","User does not exist")
			print "CDUIRESETPSW: userid not matching any entry"
		else: 
			user = set.getMbo(0)
			setPSW = user.getMboSet("MYPROFILECHANGEPASSWORDS")
			pswMbo = setPSW.add()
			newPassword = sigService.generatePassword(userID, uInfo)
			print "CDUIRESETPSW: password generated"
			user.setValue("passwordinput",newPassword,MboConstants.NOACCESSCHECK | MboConstants.DELAYVALIDATION)
			user.setValue("passwordcheck", newPassword,MboConstants.NOACCESSCHECK | MboConstants.DELAYVALIDATION)
			user.setValue("passwordold", newPassword,MboConstants.NOACCESSCHECK | MboConstants.DELAYVALIDATION)
			pswMbo.setValue("passwordinput",newPassword,MboConstants.NOACCESSCHECK | MboConstants.DELAYVALIDATION)
			pswMbo.setValue("passwordcheck", newPassword,MboConstants.NOACCESSCHECK | MboConstants.DELAYVALIDATION)
			pswMbo.setValue("passwordold", newPassword,MboConstants.NOACCESSCHECK | MboConstants.DELAYVALIDATION)
			user.setValue("forceexpiration",1, MboConstants.NOACCESSCHECK | MboConstants.DELAYVALIDATION)
			user.setValue("emailpswd",1, MboConstants.NOACCESSCHECK | MboConstants.DELAYVALIDATION)
			print "CDUIRESETPSW: password set"
			set.save()
except Exception:
	responseHeaders.put("OPCODE","100")
	responseHeaders.put("OPMSG","Unhandled error")