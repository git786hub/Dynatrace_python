# AUTOSCRIPT NAME: CG_DOCLINK
# CREATEDDATE: 2013-11-19 12:19:41
# CREATEDBY: UVX3
# CHANGEDATE: 2014-01-23 23:55:24
# CHANGEBY: UVX3
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.mbo import MboSetRemote
from psdi.server import MXServer
import java.util.Vector
from java.util import Date
from java.text import SimpleDateFormat

#print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'


s_secgroupset1 = "'TRNSYSPROT'"
s_secgroupset2 = "'TRNFIELD2','TRNFIELD1','TRNMANAGER','GENBILLADMIN'"
b_userInSecurityGroup1 = 0
b_userInSecurityGroup2 = 0

def setError(g, k, p):
    global errorgroup, errorkey, params
    errorgroup = g
    errorkey = k
    params = p

today= SimpleDateFormat("dd/MM/yyyy").format(Date())

doclinksmboSet= mbo.getThisMboSet()

mbosetMaxuser = MXServer.getMXServer().getMboSet("MAXUSER", mbo.getUserInfo())
mbosetMaxuser.setWhere("userid = '" + user + "'")
mbosetMaxuser.reset()
mboMaxuser = mbosetMaxuser.moveFirst()

if (mboMaxuser is not None):
	mbosetGroupUser1 = mboMaxuser.getMboSet("GROUPUSER")
	mbosetGroupUser1.setWhere("groupname in (" + s_secgroupset1 + ")")
	mbosetGroupUser1.reset()
	mboMaxGroup = mbosetGroupUser1.moveFirst()

if (not mbosetGroupUser1.isEmpty()):
		b_userInSecurityGroup1 = 1

if (mboMaxuser is not None):
	mbosetGroupUser2 = mboMaxuser.getMboSet("GROUPUSER")
	mbosetGroupUser2.setWhere("groupname in (" + s_secgroupset2 + ")")
	mbosetGroupUser2.reset()
	mboMaxGroup = mbosetGroupUser2.moveFirst()

if (not mbosetGroupUser2.isEmpty()):
		b_userInSecurityGroup2 = 1

if doclinksmboSet.getMbo().toBeDeleted() :
   doclinksmbo = doclinksmboSet.getMbo()
   createdby = doclinksmbo.getString("CREATEBY")
   createdate = SimpleDateFormat("dd/MM/yyyy").format(doclinksmbo.getDate("CREATEDATE"))
   #print '&&&&&&Create date is ' + str(createdate)
  # print '&&&&&&Today is ' + str(today)
   if  (today > createdate and b_userInSecurityGroup2 == 1 and b_userInSecurityGroup1 == 0 and createdby == user) :
      setError("doclink", "cannotdelete", None)
      doclinksmbo.undelete()
   elif (b_userInSecurityGroup2 == 1 and b_userInSecurityGroup1 == 0 and createdby != user) :
      setError("doclink", "cannotdelete", None)
      doclinksmbo.undelete()