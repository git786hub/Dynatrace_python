# AUTOSCRIPT NAME: EX2DISTSPEND1STSAVE
# CREATEDDATE: 2014-02-17 14:48:06
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-05-25 19:03:15
# CHANGEBY: UFQJ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.security import UserInfo
from psdi.mbo import MboConstants
from java.util import Calendar
from java.util import Date
import sys

# if spend quantity adjusted to less than the current spending, swap to the other vendor / contract
if (onadd) :

    # use sql to activate / deactivate contract lines - set status APPR / WAPPR (cannot use mbo, it does not allow WAPPR coz active PO exists)
    qry2 = "update contractline set linestatus = 'WAPPR' where itemnum = '" + mbo.getString("ex2itemnum")
    qry2 = qry2 + "' and (contractnum, revisionnum) in (select contractnum, revisionnum from contract where vendor = '"
    qry2 = qry2 + mbo.getString("ex2scndvendor") + "' and status = 'APPR')"
    ck = mbo.getUserInfo().getConnectionKey()
    conn = mbo.getMboServer().getDBConnection(ck)
    stmt = conn.createStatement()
    rs = stmt.executeQuery(qry2)
    mbo.getMboServer().freeDBConnection(ck)
    stmt.close()
    rs.close()