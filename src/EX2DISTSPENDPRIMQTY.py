# AUTOSCRIPT NAME: EX2DISTSPENDPRIMQTY
# CREATEDDATE: 2014-02-17 13:48:37
# CREATEDBY: UFQJ
# CHANGEDATE: 2014-05-25 19:03:22
# CHANGEBY: UFQJ
# SCRIPTLANGUAGE: jython
# STATUS: Active

from psdi.security import UserInfo
from psdi.mbo import MboConstants
from java.util import Calendar
from java.util import Date
import sys

# if spend quantity adjusted to less than the current spending, swap to the other vendor / contract
if (mbo.getDouble("ex2primspendqty") < mbo.getDouble("ex2primcurrqty")) :

    # Use the Calendar to get the current Date/Time
    c = Calendar.getInstance()
    c.add(Calendar.SECOND,0)

    #mbo.setValue("ex2escalate", 1)   # flag for notification to contract buyer
    mbo.setValue("ex2primactive", 0)
    mbo.setValue("ex2scndactive", 1)
    mbo.setValue("ex2scndactdate", c.getTime())
    mbo.setValue("ex2primcurrqty", 0)

    # use sql to activate / deactivate contract lines - set status APPR / WAPPR (cannot use mbo, it does not allow WAPPR coz active PO exists)
    qry1 = "update contractline set linestatus = 'WAPPR' where itemnum = '" + mbo.getString("ex2itemnum")
    qry1 = qry1 + "' and (contractnum, revisionnum) in (select contractnum, revisionnum from contract where vendor = '"
    qry1 = qry1 + mbo.getString("ex2primvendor") + "' and status = 'APPR')"
    qry2 = "update contractline set linestatus = 'APPR' where itemnum = '" + mbo.getString("ex2itemnum")
    qry2 = qry2 + "' and (contractnum, revisionnum) in (select contractnum, revisionnum from contract where vendor = '"
    qry2 = qry2 + mbo.getString("ex2scndvendor") + "' and status = 'APPR')"
    ck = mbo.getUserInfo().getConnectionKey()
    conn = mbo.getMboServer().getDBConnection(ck)
    stmt = conn.createStatement()
    rs = stmt.executeQuery(qry1)
    rs = stmt.executeQuery(qry2)
    mbo.getMboServer().freeDBConnection(ck)
    stmt.close()
    rs.close()