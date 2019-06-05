# AUTOSCRIPT NAME: EX2DISTSPCTRREVAPPR
# CREATEDDATE: 2014-04-27 08:58:22
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-10-13 20:15:55
# CHANGEBY: UVD7
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.security import UserInfo
from psdi.mbo import MboConstants
from java.util import Calendar
from java.util import Date
import sys

print "DDDDDDDDDDDDDDDDD "
# contract has been approved so that the inactive contract line is in APPR, change it back to WAPPR
if mbo.getBoolean("ex2primactive") :       # it is the secondary that needs to be deactivated
    print "DDDDDDDDDDDDDDDDD scnd "

    # use sql to deactivate contract line - set status WAPPR (cannot use mbo, it does not allow WAPPR coz active PO exists)
    qry2 = "update contractline set linestatus = 'WAPPR' where itemnum = '" + mbo.getString("ex2itemnum")
    qry2 = qry2 + "' and (contractnum, revisionnum) in (select contractnum, revisionnum from contract where vendor = '"
    qry2 = qry2 + mbo.getString("ex2scndvendor") + "' and status = 'APPR')"
    print "DDDDDDDDDDDDDDDDD " + qry2
    ck = mbo.getUserInfo().getConnectionKey()
    conn = mbo.getMboServer().getDBConnection(ck)
    stmt = conn.createStatement()
    rs = stmt.executeQuery(qry2)
    mbo.getMboServer().freeDBConnection(ck)
    stmt.close()
    rs.close()

if mbo.getBoolean("ex2scndactive") :       # it is the primary that needs to be deactivated
    print "DDDDDDDDDDDDDDDDD prim"

    # use sql to deactivate contract line - set status WAPPR (cannot use mbo, it does not allow WAPPR coz active PO exists)
    qry2 = "update contractline set linestatus = 'WAPPR' where itemnum = '" + mbo.getString("ex2itemnum")
    qry2 = qry2 + "' and (contractnum, revisionnum) in (select contractnum, revisionnum from contract where vendor = '"
    qry2 = qry2 + mbo.getString("ex2primvendor") + "' and status = 'APPR')"
    print "DDDDDDDDDDDDDDDDD " + qry2
    ck = mbo.getUserInfo().getConnectionKey()
    conn = mbo.getMboServer().getDBConnection(ck)
    stmt = conn.createStatement()
    rs = stmt.executeQuery(qry2)
    mbo.getMboServer().freeDBConnection(ck)
    stmt.close()
    rs.close()